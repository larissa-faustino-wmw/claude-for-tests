# Contexto do sistema para quem escreve os testes

- **Duas stacks, um domínio.** App/PDA (`lavenderepda`, TotalCross, SQLite no aparelho, tabelas `TBLVP<X>`) e Web (`lavendereweb`, JSF + Spring, PostgreSQL, SQL Server ou Oracle conforme o cliente, tabelas `TBLVW<X>`). Uma mudança do Jira pode afetar uma ou as duas: foque a regressão na stack afetada e nas dependências diretas, sem presumir que quebra módulos não relacionados.
- **Consulta e visualização:** cenário 100% de tela é válido para garantir que o dado aparece depois de uma consulta ou relatório.
- **Criação, edição e gravação no App:** valide em etapas: 1) gravou no SQLite; 2) enviou/sincronizou com a Web; 3) os dados chegaram inteiros. O caso compartilhado do Squash para isso é o **PERSISTENCIA-001 - Validação de Persistência de Dados APP e Sincronização com a Web** ([3463](https://squash.wmw.com.br/squash/test-case-workspace/test-case/3463/steps)).
- **Sessão:** sem timeout rígido, mas todo cenário começa pelo login.
- **Localização:** só importa em tributação, fuso horário, login e agenda.
- **Dependências externas que podem falhar:** busca de CNPJ/CPF, busca de Leads (Maps), roteiro com mapas, envio de e-mail. Evite depender delas no teste, ou deixe claro no cenário.
- **Mensagens de erro:** o app deve dizer claramente o problema sem travar o fluxo. Se não faz, é bug (abrir com a `criar-task-jira`). Em módulo legado pode ser preciso descobrir a mensagem antes de validar.
- **Processamento em background:** funcionalidades que dependem da Web (controle online, liberação por outro usuário) podem exigir esperar um job; normalmente a atividade ou a documentação avisa.
- **Versão:** trabalhe sempre com a versão atual, sem V1/V2. Para saber desde quando algo funciona assim, veja a data de criação do cenário.
- **Ambientes:** homologação e produção funcionam igual; a homologação pode estar à frente quando há demandas novas.
- **Evidências de execução:** cada execução guarda os dados em `dadosTest/<Classe>/` (prints de falha em `imagens/<método>/`, banco em `dbs/`). Para analisar uma falha, use a skill `analise-logs-jenkins`.
