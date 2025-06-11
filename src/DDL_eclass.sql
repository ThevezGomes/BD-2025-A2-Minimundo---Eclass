create schema eclass;

SET SEARCH_PATH = eclass;

CREATE TABLE Disciplina
(
  CodigoDisc VARCHAR(64) NOT NULL,
  NomeDisc VARCHAR(64) NOT NULL,
  PeriodoDisc VARCHAR(32) NOT NULL,
  FotoDisc VARCHAR(244) NOT NULL,
  PRIMARY KEY (CodigoDisc)
);

CREATE TABLE Questionario
(
  IDQuest INT NOT NULL,
  DescricaoQuest VARCHAR(1024),
  PrazoQuest DATE NOT NULL,
  NumTentaQuest INT NOT NULL,
  PerguntasQuest VARCHAR(244) NOT NULL,
  GabaritoQuest VARCHAR(244),
  PontMaxQuest FLOAT,
  NomeQuest VARCHAR(64) NOT NULL,
  CodigoDisc VARCHAR(64) NOT NULL,
  PRIMARY KEY (IDQuest),
  FOREIGN KEY (CodigoDisc) REFERENCES Disciplina(CodigoDisc)
);

CREATE TABLE Modulo
(
  IDModulo INT NOT NULL,
  NomeModulo VARCHAR(64) NOT NULL,
  CodigoDisc VARCHAR(64) NOT NULL,
  PRIMARY KEY (IDModulo),
  FOREIGN KEY (CodigoDisc) REFERENCES Disciplina(CodigoDisc)
);

CREATE TABLE Categoria_de_Grupo
(
  IDCateg INT NOT NULL,
  NomeCateg VARCHAR(64) NOT NULL,
  CodigoDisc VARCHAR(64) NOT NULL,
  PRIMARY KEY (IDCateg),
  FOREIGN KEY (CodigoDisc) REFERENCES Disciplina(CodigoDisc)
);

CREATE TABLE Usuario
(
  IDUser INT NOT NULL,
  PrimNomeUser VARCHAR(64) NOT NULL,
  SobrenomeUser VARCHAR(256) NOT NULL,
  FotoUser VARCHAR(244),
  DataNascUser DATE,
  CidadeUser VARCHAR(64),
  EstadoUser VARCHAR(64),
  PaisUser VARCHAR(64),
  PRIMARY KEY (IDUser)
);

CREATE TABLE Aluno
(
  MatriculaAluno INT NOT NULL,
  IDUser INT NOT NULL,
  PRIMARY KEY (IDUser),
  FOREIGN KEY (IDUser) REFERENCES Usuario(IDUser),
  UNIQUE (MatriculaAluno)
);

CREATE TABLE Monitor
(
  IDUser INT NOT NULL,
  PRIMARY KEY (IDUser),
  FOREIGN KEY (IDUser) REFERENCES Usuario(IDUser)
);

CREATE TABLE Professor
(
  IDUser INT NOT NULL,
  PRIMARY KEY (IDUser),
  FOREIGN KEY (IDUser) REFERENCES Usuario(IDUser)
);

CREATE TABLE AlunoDisc
(
  IDUser INT NOT NULL,
  CodigoDisc VARCHAR(64) NOT NULL,
  PRIMARY KEY (IDUser, CodigoDisc),
  FOREIGN KEY (IDUser) REFERENCES Aluno(IDUser),
  FOREIGN KEY (CodigoDisc) REFERENCES Disciplina(CodigoDisc)
);

CREATE TABLE MonitDisc
(
  IDUser INT NOT NULL,
  CodigoDisc VARCHAR(64) NOT NULL,
  PRIMARY KEY (IDUser, CodigoDisc),
  FOREIGN KEY (IDUser) REFERENCES Monitor(IDUser),
  FOREIGN KEY (CodigoDisc) REFERENCES Disciplina(CodigoDisc)
);

CREATE TABLE ProfDisc
(
  IDUser INT NOT NULL,
  CodigoDisc VARCHAR(64) NOT NULL,
  PRIMARY KEY (IDUser, CodigoDisc),
  FOREIGN KEY (IDUser) REFERENCES Professor(IDUser),
  FOREIGN KEY (CodigoDisc) REFERENCES Disciplina(CodigoDisc)
);

CREATE TABLE ArquivoQuest
(
  ArquivoQuest VARCHAR(244) NOT NULL,
  IDQuest INT NOT NULL,
  PRIMARY KEY (ArquivoQuest, IDQuest),
  FOREIGN KEY (IDQuest) REFERENCES Questionario(IDQuest)
);

CREATE TABLE Topico
(
  IDTopico INT NOT NULL,
  NomeTopico VARCHAR(64) NOT NULL,
  ConteudoTopico VARCHAR(1024),
  IDModulo INT NOT NULL,
  PRIMARY KEY (IDTopico),
  FOREIGN KEY (IDModulo) REFERENCES Modulo(IDModulo)
);

CREATE TABLE Tentativa_de_questionario
(
  IDTentQuest INT NOT NULL,
  RespTentQuest VARCHAR(244) NOT NULL,
  NotaTentQuest FLOAT,
  DataTentQuest DATE NOT NULL,
  IDQuest INT NOT NULL,
  IDUser INT NOT NULL,
  PRIMARY KEY (IDTentQuest),
  FOREIGN KEY (IDQuest) REFERENCES Questionario(IDQuest),
  FOREIGN KEY (IDUser) REFERENCES Aluno(IDUser)
);

CREATE TABLE Atividade
(
  IDAtiv INT NOT NULL,
  NomeAtiv VARCHAR(64) NOT NULL,
  TipoAtiv VARCHAR(64) NOT NULL,
  PrazoAtiv DATE NOT NULL,
  PontMaxAtiv FLOAT,
  DescricaoAtiv VARCHAR(1024),
  CodigoDisc VARCHAR(64) NOT NULL,
  IDCateg INT,
  PRIMARY KEY (IDAtiv),
  FOREIGN KEY (CodigoDisc) REFERENCES Disciplina(CodigoDisc),
  FOREIGN KEY (IDCateg) REFERENCES Categoria_de_Grupo(IDCateg)
);

CREATE TABLE Grupo
(
  IDGrupo INT NOT NULL,
  NomeGrupo VARCHAR(64) NOT NULL,
  LimitUsersGrupo INT NOT NULL,
  IDCateg INT NOT NULL,
  PRIMARY KEY (IDGrupo),
  FOREIGN KEY (IDCateg) REFERENCES Categoria_de_Grupo(IDCateg)
);

CREATE TABLE Mensagem
(
  IDMsg INT NOT NULL,
  ConteudoMsg VARCHAR(1024) NOT NULL,
  DataEnvioMsg DATE NOT NULL,
  IDUser INT NOT NULL,
  PRIMARY KEY (IDMsg),
  FOREIGN KEY (IDUser) REFERENCES Usuario(IDUser)
);

CREATE TABLE AlunoGrupo
(
  IDUser INT NOT NULL,
  IDGrupo INT NOT NULL,
  PRIMARY KEY (IDUser, IDGrupo),
  FOREIGN KEY (IDUser) REFERENCES Aluno(IDUser),
  FOREIGN KEY (IDGrupo) REFERENCES Grupo(IDGrupo)
);

CREATE TABLE UserRecebMsg
(
  IDUser INT NOT NULL,
  IDMsg INT NOT NULL,
  PRIMARY KEY (IDUser, IDMsg),
  FOREIGN KEY (IDUser) REFERENCES Usuario(IDUser),
  FOREIGN KEY (IDMsg) REFERENCES Mensagem(IDMsg)
);

CREATE TABLE ArquivoTopico
(
  ArquivoTopico VARCHAR(244) NOT NULL,
  IDTopico INT NOT NULL,
  PRIMARY KEY (ArquivoTopico, IDTopico),
  FOREIGN KEY (IDTopico) REFERENCES Topico(IDTopico)
);

CREATE TABLE ArquivoAtiv
(
  ArquivoAtiv VARCHAR(244) NOT NULL,
  IDAtiv INT NOT NULL,
  PRIMARY KEY (ArquivoAtiv, IDAtiv),
  FOREIGN KEY (IDAtiv) REFERENCES Atividade(IDAtiv)
);

CREATE TABLE Entrega_de_atividade
(
  IDEntAtv INT NOT NULL,
  ConteudoEntAtv VARCHAR(244),
  NotaEntAtv FLOAT,
  DataEntAtv DATE NOT NULL,
  IDAtiv INT NOT NULL,
  IDGrupo INT,
  IDUser INT,
  PRIMARY KEY (IDEntAtv),
  FOREIGN KEY (IDAtiv) REFERENCES Atividade(IDAtiv),
  FOREIGN KEY (IDGrupo) REFERENCES Grupo(IDGrupo),
  FOREIGN KEY (IDUser) REFERENCES Aluno(IDUser)
);

CREATE TABLE ArquivoEntAtv
(
  ArquivoEntAtv VARCHAR(244) NOT NULL,
  IDEntAtv INT NOT NULL,
  PRIMARY KEY (ArquivoEntAtv, IDEntAtv),
  FOREIGN KEY (IDEntAtv) REFERENCES Entrega_de_atividade(IDEntAtv)
);