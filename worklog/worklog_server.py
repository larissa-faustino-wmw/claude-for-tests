#!/usr/bin/env python3
"""Servidor local do apontamento de horas: serve o HTML e repassa /rest/* para o Jira.

Por que existe: aberto direto do disco, o HTML tem origem "null"; servido por qualquer
outra origem, o Jira 8.14 não devolve Access-Control-Allow-Origin. Nos dois casos a chamada
morre no preflight do navegador. Servindo a página e a API pela MESMA origem
(http://localhost:8787), não existe CORS nenhum.

Ele não guarda credencial e não lê arquivo de configuração. Cada chamada que chega traz o
destino no cabeçalho X-Jira-Base e o token em Authorization — os dois digitados na página.
O processo só monta a requisição, com o mesmo contexto SSL (certifi) e o mesmo Bearer que o
jira_subtask.py já usa, e devolve a resposta crua.

Uso:
  python3 worklog_server.py
  python3 worklog_server.py --port 8787 --page "worklog (1).html"
  python3 worklog_server.py --insecure                      # certificado interno não confiável
  python3 worklog_server.py --allow jira2.wmw.com.br        # restringe os destinos aceitos

Escuta só em 127.0.0.1. Python 3.9+, sem dependências além do certifi que você já tem.
"""
import argparse
import json
import os
import re
import ssl
import sys
import urllib.error
import urllib.parse
import urllib.request
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

DEFAULT_PORT = 8787
DEFAULT_TARGET = "https://jira2.wmw.com.br"
DEFAULT_PAGE = "worklog.html"
HERE = os.path.dirname(os.path.abspath(__file__))

# Cabeçalhos que não fazem sentido repassar, mais o nosso próprio X-Jira-Base.
DROP_HEADERS = {
    "host", "connection", "content-length", "origin", "referer",
    "cookie", "x-jira-base", "sec-fetch-mode", "sec-fetch-site",
    "sec-fetch-dest", "user-agent", "accept-encoding",
}

CORS = {
    "Access-Control-Allow-Origin": "*",
    "Access-Control-Allow-Methods": "GET,POST,PUT,DELETE,OPTIONS",
    "Access-Control-Allow-Headers": "Authorization,Content-Type,Accept,X-Jira-Base",
    "Access-Control-Max-Age": "600",
}


def ssl_context(insecure=False):
    # A instalação do python.org não traz o cert.pem do sistema (Install Certificates.command
    # nunca rodado); usa o bundle do certifi em vez do trust store da instalação.
    if insecure:
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
        return ctx
    try:
        import certifi
        return ssl.create_default_context(cafile=certifi.where())
    except ImportError:
        return ssl.create_default_context()


def find_page(name):
    candidate = os.path.join(HERE, name)
    if os.path.exists(candidate):
        return candidate
    html = sorted(f for f in os.listdir(HERE) if re.search(r"\.html?$", f, re.I))
    return os.path.join(HERE, html[0]) if html else candidate


class Handler(BaseHTTPRequestHandler):
    server_version = "worklog/2.0"
    cfg = {}

    # ---------- respostas ----------

    def reply(self, status, body=b"", content_type="application/json", extra=None):
        self.send_response(status)
        for key, value in CORS.items():
            self.send_header(key, value)
        for key, value in (extra or {}).items():
            self.send_header(key, value)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        if self.command != "HEAD":
            self.wfile.write(body)

    def reply_json(self, status, payload):
        self.reply(status, json.dumps(payload).encode("utf-8"))

    def reply_problem(self, status, message):
        # Mesmo formato de erro do Jira, então a página já sabe exibir.
        self.reply_json(status, {"errorMessages": [message]})

    # ---------- rotas ----------

    def do_OPTIONS(self):
        self.reply(204)

    def do_GET(self):
        path = urllib.parse.urlparse(self.path).path
        if path == "/__info":
            return self.reply_json(200, {
                "relay": True,
                "defaultTarget": self.cfg["target"],
                "page": os.path.basename(self.cfg["page"]),
                "insecure": self.cfg["insecure"],
                "allow": self.cfg["allow"],
            })
        if path.startswith("/rest/"):
            return self.forward()
        return self.serve_page()

    do_HEAD = do_GET

    def do_POST(self):
        if urllib.parse.urlparse(self.path).path.startswith("/rest/"):
            return self.forward()
        return self.reply_problem(404, "Rota desconhecida: " + self.path)

    do_PUT = do_POST
    do_DELETE = do_POST

    def serve_page(self):
        try:
            with open(self.cfg["page"], "rb") as f:
                body = f.read()
        except OSError:
            return self.reply(
                500,
                ("Não encontrei %s.\nDeixe o worklog_server.py na mesma pasta do HTML, "
                 "ou aponte com --page.\n" % self.cfg["page"]).encode("utf-8"),
                "text/plain; charset=utf-8",
            )
        self.reply(200, body, "text/html; charset=utf-8", {"Cache-Control": "no-store"})

    # ---------- destino ----------

    def target(self):
        """Base do Jira que a página mandou, ou o default da linha de comando."""
        raw = (self.headers.get("X-Jira-Base") or self.cfg["target"]).strip().rstrip("/")
        parts = urllib.parse.urlparse(raw)
        if parts.scheme not in ("http", "https") or not parts.netloc:
            raise ValueError("Servidor inválido: %r. Use algo como https://jira2.wmw.com.br." % raw)
        if self.cfg["allow"] and parts.hostname not in self.cfg["allow"]:
            raise ValueError("Destino %s fora da lista permitida (%s)."
                             % (parts.hostname, ", ".join(self.cfg["allow"])))
        return parts.scheme + "://" + parts.netloc

    # ---------- repasse ----------

    def forward(self):
        try:
            target = self.target()
        except ValueError as err:
            return self.reply_problem(400, str(err))

        if not self.headers.get("Authorization"):
            return self.reply_problem(401, "Sem credencial. Preencha o token na página.")

        length = int(self.headers.get("Content-Length") or 0)
        payload = self.rfile.read(length) if length else None

        request = urllib.request.Request(target + self.path, data=payload, method=self.command)
        for name, value in self.headers.items():
            if name.lower() not in DROP_HEADERS:
                request.add_header(name, value)
        request.add_header("Accept", self.headers.get("Accept") or "application/json")

        try:
            with urllib.request.urlopen(request, context=self.cfg["ssl"], timeout=30) as response:
                body = response.read()
                self.trace(target, response.status)
                self.reply(response.status, body,
                           response.headers.get("Content-Type", "application/json"))
        except urllib.error.HTTPError as err:
            # 401/403/404 do Jira são resposta legítima: repassa como veio.
            body = err.read()
            self.trace(target, err.code)
            self.reply(err.code, body, err.headers.get("Content-Type", "application/json"))
        except urllib.error.URLError as err:
            reason = str(err.reason)
            self.trace(target, "falhou: " + reason)
            hint = (" Tente --insecure." if "certificate" in reason.lower()
                    else " Confira a VPN e o endereço.")
            self.reply_problem(502, "Não alcancei %s: %s.%s" % (target, reason, hint))
        except TimeoutError:
            self.trace(target, "timeout")
            self.reply_problem(504, "O Jira não respondeu em 30s. Confira a VPN.")

    # ---------- log ----------

    def trace(self, target, status):
        sys.stdout.write("%s  %s %s → %s  [%s]\n" % (
            self.log_date_time_string(), self.command, self.path, status, target))
        sys.stdout.flush()

    def log_message(self, *args):
        pass  # o log útil é o trace acima


def main():
    parser = argparse.ArgumentParser(description="Servidor local do apontamento de horas")
    parser.add_argument("--port", type=int, default=int(os.environ.get("PORT", DEFAULT_PORT)))
    parser.add_argument("--target", default=DEFAULT_TARGET,
                        help="destino sugerido à página quando ela abre (default: %s)" % DEFAULT_TARGET)
    parser.add_argument("--page", default=DEFAULT_PAGE)
    parser.add_argument("--insecure", action="store_true",
                        help="não verificar o certificado TLS do Jira")
    parser.add_argument("--allow", action="append", metavar="HOST",
                        help="limita os destinos aceitos; repita para vários")
    args = parser.parse_args()

    Handler.cfg = {
        "target": args.target.rstrip("/"),
        "page": find_page(args.page),
        "insecure": args.insecure,
        "allow": args.allow or [],
        "ssl": ssl_context(args.insecure),
    }

    print("Apontamento de horas em http://localhost:%d" % args.port)
    print("Servindo %s" % os.path.basename(Handler.cfg["page"]))
    print("Servidor e token: os que você digitar na página — nada fica guardado aqui.")
    print("Destino sugerido: %s%s" % (
        Handler.cfg["target"], "  (TLS sem verificação)" if args.insecure else ""))
    if Handler.cfg["allow"]:
        print("Destinos permitidos: %s" % ", ".join(Handler.cfg["allow"]))
    print("Ctrl+C para parar.\n")

    try:
        ThreadingHTTPServer(("127.0.0.1", args.port), Handler).serve_forever()
    except KeyboardInterrupt:
        print("\nEncerrado.")
    except OSError as err:
        sys.exit("erro ao subir na porta %d: %s" % (args.port, err))


if __name__ == "__main__":
    main()
