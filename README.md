# BD-2025-A2-Minimundo---Eclass

Minimundo do Banco de Dados do Eclass da FGV usando engenharia reversa. 

## Integrantes do Grupo

- Isaías Gouveia Gonçalves
- Henrique Gabriel Gasparelo
- José Thevez Gomes Guedes

## Explicação do código e instruções

`DDL_eclass.sql`: Arquivo SQL com as instruções DDL para a criação das relações do banco de dados. 

`DML_eclass.sql`: Arquivo SQL com as instruções DML para inserção de instâncias nas tabelas do banco de dados. 

`gerador_users_eclass.sql`: Arquivo SQL que gera 10000 usuários e 100 disciplinas e insere no banco de dados. 

`INDEX.sql`: Arquivo SQL com os testes de desempenho com e sem o uso de índices. \
O primeiro teste compara o tempo de execução para busca de um usuário pelo seu primeiro nome sem índices e usando a coluna do primeiro nome (primnomeuser) como índice. \
O segundo teste compara o tempo de execução para busca de todos as disciplinas associadas a um usuário de id específico sem índices e usando a coluna de id do usúario (iduser) como índice, para esse teste, foram criados 3 índices, uma vez que existem 3 relações de usuários com disciplinas, já que um usuário pode ser professor, aluno ou monitor, além disso, como iduser é uma chave primária, foi utilizado um comando SQL para remoção do índice associado à essa chave primária, para avaliar o ganho de desempenho. 

`CRUD.py` Arquivo Python com o menu CRUD para manipulação do banco de dados. Para executar esse código, certifique-se de ter instalado as bibliotecas psycopg2, sys e datetime. Após execução do código, além das opções de criação, leitura, atualização e remoção, existe uma opção chamada "Ferramentas de Desenvolvedor", que possui os testes de índices explicados anteriormente.

  **OBSERVAÇÃO IMPORTANTE**: Para execução correta do menu CRUD, lembre-se de alterar o nome do banco de dados (dbname): 
  
  ```python
  self.conn = psycopg2.connect(dbname="NOME DO SEU BANCO DE DADOS")
  ```
  Para o seu nome.

Entre as recursos disponíveis no CRUD, estão:

- Gerenciamento de Usuários
- Controle de Papéis
- Gestão de Disciplinas
- Criação de Conteúdo
- Matrícula em Disciplinas
- Registro de Entregas
- Lançamento de Notas
- Gerenciamento de Grupos
- Sistema de Mensagens
- Geração de Relatórios
- Listas de Alunos

`Minimundo IV.pdf`: Arquivo PDF com a apresentação de slides que explica os trabalhos realizados na parte IV do minimundo, mostra um exemplo de uso do CRUD e apresenta os resultados obtidos nos testes de índices.
