-- Inserção na tabela Usuario
INSERT INTO usuario VALUES (101, 'Henrique', 'Gabriel Gasporito', 'gasporito.jpg', '2006-11-10', 'Rio de Janeiro', 'RJ', 'Brasil');
INSERT INTO usuario VALUES (102, 'Maria', 'Soledade Aroma', 'maria.jpg', NULL, 'Registro', 'SP', 'Brasil');
INSERT INTO usuario VALUES (103, 'Antônio', 'Leitura Preto', 'pret0.jpg', NULL, 'Itapericica da Serra', 'ES', 'Brasil');
INSERT INTO usuario VALUES (104, 'Luciano', 'Pinho', NULL, NULL, NULL, NULL, NULL);
INSERT INTO usuario VALUES (105, 'Bryan', 'Rocha', 'braia.jpg', '2000-02-29', NULL, NULL, NULL);
INSERT INTO usuario VALUES (106, 'José', 'Thevez', NULL, NULL, 'Brejinho', 'PE', 'Brasil');
INSERT INTO usuario VALUES (107, 'Cesar', 'Viana', NULL, '1964-03-14', 'Rio de Janeiro', 'RJ', 'Brasil');
INSERT INTO usuario VALUES (108, 'Julio', 'Cesar', 'julio.jpg', '1972-01-10', 'Salt Lake City', 'UT', 'Estados Unidos');
INSERT INTO usuario VALUES (109, 'Henrique', 'Alvarenga', NULL, '1996-04-14', NULL, NULL, NULL);
INSERT INTO usuario VALUES (110, 'Elon', 'Lima', 'elon.jpg', '1945-07-22', 'Rio de Janeiro', 'RJ', 'Brasil');
INSERT INTO usuario VALUES (111, 'Yuri', 'Saporelo', 'yuri.jpg', '1994-10-11', 'Rio de Janeiro', 'RJ', 'Brasil');
INSERT INTO usuario VALUES (112, 'Bianca', 'Nunes', NULL, '2009-08-19', NULL, NULL, NULL);
INSERT INTO usuario VALUES (113, 'Isaías', 'Gouvêia Gonçalves', 'pou.jpg', '2004-04-19', 'Brejinho', 'PE', 'Brasil');
INSERT INTO usuario VALUES (114, 'Luna', 'Guedes', 'luna.jpg', '2001-12-12', 'São José do Egito', 'PE', 'Brasil');

-- Inserção na tabela Aluno

INSERT INTO aluno VALUES (1001, 102);
INSERT INTO aluno VALUES (1002, 103);
INSERT INTO aluno VALUES (1003, 104);
INSERT INTO aluno VALUES (1004, 105);
INSERT INTO aluno VALUES (1005, 106);
INSERT INTO aluno VALUES (1006, 107);
INSERT INTO aluno VALUES (1008, 109);
INSERT INTO aluno VALUES (1009, 114);
INSERT INTO aluno VALUES (1010, 112);

-- Inserção na tabela Professor
INSERT INTO professor VALUES (101);
INSERT INTO professor VALUES (113);
INSERT INTO professor VALUES (110);
INSERT INTO professor VALUES (108);
INSERT INTO professor VALUES (111);

-- Inserção na tabela Monitor
INSERT INTO monitor VALUES (103);
INSERT INTO monitor VALUES (105);
INSERT INTO monitor VALUES (107);
INSERT INTO monitor VALUES (109);
INSERT INTO monitor VALUES (102);

-- Inserção na tabela Disciplina
INSERT INTO disciplina VALUES ('2025-1-EMAP-710-710008-710', 'Análise na Reta', '2025.1', 'calculo.jpg');
INSERT INTO disciplina VALUES ('2025-1-EMAP-708-708010-3708-1', 'Banco de Dados', '2025.1', 'algebra.jpg');
INSERT INTO disciplina VALUES ('2025-1-APRMÁQ-AGRUPADAÁ', 'Técnicas e Algoritmos em Ciência de Dados', '2025.1', 'estatistica.jpg');
INSERT INTO disciplina VALUES ('2024-2-ALGLIN-AGRUPADAI', 'Álgebra Linear', '2024.2', 'otimizacao.jpg');
INSERT INTO disciplina VALUES ('2024-1-EMAP-708-708057-1708-1', 'Fundamentos da Matemática', '2024.1', 'analise.jpg');
INSERT INTO disciplina VALUES ('2025-1-ALLINU-AGRUPADAN', 'Álgebra Linear Numérica', '2025.1', 'trefethen.jpg');

-- Inserção na tabela AlunoDisc
INSERT INTO alunodisc VALUES (102, '2025-1-EMAP-710-710008-710');
INSERT INTO alunodisc VALUES (102, '2024-2-ALGLIN-AGRUPADAI');
INSERT INTO alunodisc VALUES (102, '2025-1-APRMÁQ-AGRUPADAÁ');
INSERT INTO alunodisc VALUES (106, '2024-2-ALGLIN-AGRUPADAI');
INSERT INTO alunodisc VALUES (104, '2024-1-EMAP-708-708057-1708-1');
INSERT INTO alunodisc VALUES (112, '2024-2-ALGLIN-AGRUPADAI');
INSERT INTO alunodisc VALUES (114, '2025-1-EMAP-708-708010-3708-1');
INSERT INTO alunodisc VALUES (102, '2025-1-EMAP-708-708010-3708-1');
INSERT INTO alunodisc VALUES (103, '2025-1-EMAP-708-708010-3708-1');
INSERT INTO alunodisc VALUES (104, '2025-1-EMAP-708-708010-3708-1');
INSERT INTO alunodisc VALUES (105, '2025-1-EMAP-708-708010-3708-1');
INSERT INTO alunodisc VALUES (106, '2025-1-EMAP-708-708010-3708-1');
INSERT INTO alunodisc VALUES (107, '2025-1-EMAP-708-708010-3708-1');
INSERT INTO alunodisc VALUES (109, '2025-1-EMAP-708-708010-3708-1');
INSERT INTO alunodisc VALUES (102, '2025-1-ALLINU-AGRUPADAN');
INSERT INTO alunodisc VALUES (103, '2025-1-ALLINU-AGRUPADAN');
INSERT INTO alunodisc VALUES (104, '2025-1-ALLINU-AGRUPADAN');
INSERT INTO alunodisc VALUES (105, '2025-1-ALLINU-AGRUPADAN');
INSERT INTO alunodisc VALUES (106, '2025-1-ALLINU-AGRUPADAN');
INSERT INTO alunodisc VALUES (107, '2025-1-ALLINU-AGRUPADAN');
INSERT INTO alunodisc VALUES (109, '2025-1-ALLINU-AGRUPADAN');
INSERT INTO alunodisc VALUES (114, '2025-1-ALLINU-AGRUPADAN');
INSERT INTO alunodisc VALUES (103, '2025-1-EMAP-710-710008-710');

-- Inserção na tabela ProfDisc
INSERT INTO profdisc VALUES (101, '2024-1-EMAP-708-708057-1708-1');
INSERT INTO profdisc VALUES (113, '2024-2-ALGLIN-AGRUPADAI');
INSERT INTO profdisc VALUES (110, '2025-1-EMAP-710-710008-710');
INSERT INTO profdisc VALUES (108, '2025-1-EMAP-708-708010-3708-1');
INSERT INTO profdisc VALUES (108, '2025-1-ALLINU-AGRUPADAN');
INSERT INTO profdisc VALUES (111, '2025-1-APRMÁQ-AGRUPADAÁ');

-- Inserção na tabela MonitDisc
INSERT INTO monitdisc VALUES (103, '2024-2-ALGLIN-AGRUPADAI');
INSERT INTO monitdisc VALUES (105, '2025-1-APRMÁQ-AGRUPADAÁ');
INSERT INTO monitdisc VALUES (107, '2025-1-EMAP-710-710008-710');
INSERT INTO monitdisc VALUES (109, '2024-1-EMAP-708-708057-1708-1');
INSERT INTO monitdisc VALUES (102, '2024-2-ALGLIN-AGRUPADAI');

-- Inserção na tabela Mensagem
INSERT INTO mensagem VALUES (1, 'Material atualizado.', '2025-03-01', 101);
INSERT INTO mensagem VALUES (2, 'Prova amanhã', '2025-03-02', 113);
INSERT INTO mensagem VALUES (3, 'Lembrem dos testes', '2025-04-05', 110);
INSERT INTO mensagem VALUES (4, 'Material atualizado.', '2025-05-10', 108);
INSERT INTO mensagem VALUES (5, 'Não haverá aula', '2025-06-20', 111);

-- Inserção na tabela UserRecebMsg
INSERT INTO userrecebmsg VALUES (104, 1);
INSERT INTO userrecebmsg VALUES (102, 2);
INSERT INTO userrecebmsg VALUES (106, 2);
INSERT INTO userrecebmsg VALUES (102, 3);
INSERT INTO userrecebmsg VALUES (114, 4);
INSERT INTO userrecebmsg VALUES (102, 4);
INSERT INTO userrecebmsg VALUES (103, 4);
INSERT INTO userrecebmsg VALUES (102, 5);

-- Inserção na tabela Questionario (CORRIGIDO)
INSERT INTO questionario VALUES (1, 'Questionário sobre derivadas', '2025-05-10', 1, 'perguntas_derivadas.json', NULL, NULL, 'Questionário sobre derivadas', '2025-1-EMAP-710-710008-710');
INSERT INTO questionario VALUES (2, 'Questionário de matrizes bem difícil', '2025-05-11', 1, 'perguntas_matrizes.json', 'gabarito_matrizes.json', NULL, 'Questionário de matrizes', '2024-2-ALGLIN-AGRUPADAI');
INSERT INTO questionario VALUES (3, 'Envio online do teste 1 de fundamentos', '2025-05-12', 1, 'teste.json', NULL, 10.0,'Teste 1', '2024-1-EMAP-708-708057-1708-1');
INSERT INTO questionario VALUES (4, 'Questionário sobre a história do Banco de Dados', '2025-05-13', 1, 'breve_historia.json', 'gabarito_historia.json', 6.5,'Breve História','2025-1-EMAP-708-708010-3708-1');
INSERT INTO questionario VALUES (5, 'Questionário de séries', '2025-05-14', 1, 'perguntas_series.json', NULL, NULL,'Questionário de séries', '2025-1-EMAP-710-710008-710');

-- Inserção na tabela ArquivoQuest
INSERT INTO arquivoquest VALUES ('teoremas_uteis.pdf', 2);
INSERT INTO arquivoquest VALUES ('resumo.pdf', 2);
INSERT INTO arquivoquest VALUES ('nota_de_aula.pdf', 2);
INSERT INTO arquivoquest VALUES ('demonstracoes.pdf', 2);
INSERT INTO arquivoquest VALUES ('codigos_turma.pdf', 3);

-- Inserção na tabela Tentativa_de_questionario
INSERT INTO tentativa_de_questionario VALUES (1, 'resp1.json', NULL, '2025-05-09', 2, 106);
INSERT INTO tentativa_de_questionario VALUES (2, 'resp2.json', NULL, '2025-05-10', 2, 102);
INSERT INTO tentativa_de_questionario VALUES (3, 'resp3.json', 6.0, '2025-05-11', 3, 104);
INSERT INTO tentativa_de_questionario VALUES (4, 'resp4.json', NULL, '2025-05-12', 2, 112);
INSERT INTO tentativa_de_questionario VALUES (5, 'resp5.json', NULL, '2025-05-13', 1, 102);

-- Inserção na tabela Categoria_de_Grupo (CORRIGIDO)
INSERT INTO categoria_de_grupo VALUES (1, 'Teatro', '2025-1-EMAP-708-708010-3708-1');
INSERT INTO categoria_de_grupo VALUES (2, 'Minimundo', '2025-1-EMAP-708-708010-3708-1');
INSERT INTO categoria_de_grupo VALUES (3, 'IA', '2025-1-APRMÁQ-AGRUPADAÁ');
INSERT INTO categoria_de_grupo VALUES (4, 'Seminário', '2025-1-EMAP-708-708010-3708-1');
INSERT INTO categoria_de_grupo VALUES (5, 'Trabalho Computacional', '2025-1-APRMÁQ-AGRUPADAÁ');

-- Inserção na tabela Atividade
INSERT INTO atividade VALUES (1, 'Tarefa 1', 'Individual', '2025-03-15', 7.0, NULL, '2024-2-ALGLIN-AGRUPADAI', NULL);
INSERT INTO atividade VALUES (2, 'Projeto BD', 'Grupo', '2025-03-16', 10.0, 'Projeto de Banco de Dados', '2025-1-EMAP-708-708010-3708-1', 2);
INSERT INTO atividade VALUES (3, 'Lista 1', 'Individual', '2025-03-17', 3.5, 'Lista de Exercicios do livro do Elon', '2025-1-EMAP-710-710008-710', NULL);
INSERT INTO atividade VALUES (4, 'Teatro', 'Grupo', '2025-03-18', 10.0, 'Apresentação de teatro', '2025-1-EMAP-708-708010-3708-1', 1);
INSERT INTO atividade VALUES (5, 'Lista 1', 'Individual', '2025-03-19', NULL, 'Lista de Integrais Complexas Matriciais', '2024-1-EMAP-708-708057-1708-1', NULL);
INSERT INTO atividade VALUES (6, 'Teste Conteúdo Novo', 'Individual', '2025-03-29', 10.0, 'Teste sobre o conteúdo de conexões entre Banco de Dados e estabilidade para resolução de sistemas de mínimos quadrados usando forma de Hessemberg', '2025-1-ALLINU-AGRUPADAN', NULL);

-- Inserção na tabela ArquivoAtiv
INSERT INTO arquivoativ VALUES ('lista_cap1.pdf', 3);
INSERT INTO arquivoativ VALUES ('lista_cap2.pdf', 3);
INSERT INTO arquivoativ VALUES ('lista.pdf', 5);
INSERT INTO arquivoativ VALUES ('tarefa.pdf', 1);
INSERT INTO arquivoativ VALUES ('codigo.py', 1);

-- Inserção na tabela Grupo
INSERT INTO grupo VALUES (1, 'te1', 5, 1);
INSERT INTO grupo VALUES (2, 'mm1', 5, 2);
INSERT INTO grupo VALUES (3, 'te2', 5, 1);
INSERT INTO grupo VALUES (4, 'te3', 4, 1);
INSERT INTO grupo VALUES (5, 'te4', 5, 1);
INSERT INTO grupo VALUES (6, 'mm2', 5, 2);
INSERT INTO grupo VALUES (7, 'mm3', 5, 2);
INSERT INTO grupo VALUES (8, 'mm4', 5, 2);

-- Inserção na tabela AlunoGrupo
INSERT INTO alunogrupo VALUES (114, 1);
INSERT INTO alunogrupo VALUES (102, 1);
INSERT INTO alunogrupo VALUES (103, 2);
INSERT INTO alunogrupo VALUES (102, 2);
INSERT INTO alunogrupo VALUES (104, 3);
INSERT INTO alunogrupo VALUES (105, 3);
INSERT INTO alunogrupo VALUES (106, 4);
INSERT INTO alunogrupo VALUES (107, 4);
INSERT INTO alunogrupo VALUES (103, 5);
INSERT INTO alunogrupo VALUES (109, 5);
INSERT INTO alunogrupo VALUES (104, 6);
INSERT INTO alunogrupo VALUES (114, 6);
INSERT INTO alunogrupo VALUES (107, 7);
INSERT INTO alunogrupo VALUES (109, 7);
INSERT INTO alunogrupo VALUES (105, 8);
INSERT INTO alunogrupo VALUES (106, 8);

-- Inserção na tabela Entrega_de_atividade
INSERT INTO entrega_de_atividade VALUES (1, 'Respostas PDF', 7.0, '2025-03-14', 1, NULL, 102);
INSERT INTO entrega_de_atividade VALUES (2, 'Exercícios resolvidos', 2.5, '2025-03-16', 3, NULL, 103);
INSERT INTO entrega_de_atividade VALUES (3, 'Lista', NULL, '2025-03-18', 5, NULL, 102);
INSERT INTO entrega_de_atividade VALUES
-- Atividade 2 (Apresentação em Grupo - variações de "Apresentação PDF")
(4, 'Apresentação Final PDF', NULL, '2025-03-02', 2, 1, NULL),
(5, 'Slides PDF', 8.0, '2025-03-07', 2, 2, NULL),
(6, 'Apresentação Grupo PDF', NULL, '2025-03-11', 2, 3, NULL),
(7, 'Material Apresentação PDF', 9.5, '2025-03-04', 2, 4, NULL),
(8, 'Slides Definitivos PDF', NULL, '2025-03-14', 2, 5, NULL),
(9, 'Apresentação Revisada PDF', 7.0, '2025-03-01', 2, 6, NULL),
(10, 'Versão Final Apresentação PDF', NULL, '2025-03-09', 2, 7, NULL),
(11, 'Apresentação Projeto PDF', 6.5, '2025-03-05', 2, 8, NULL),

-- Atividade 4 (Teatro em Grupo - variações de "Roteiro PDF")
(12, 'Roteiro Teatro PDF', 10.0, '2025-03-03', 4, 1, NULL),
(13, 'Texto Teatro PDF', NULL, '2025-03-12', 4, 2, NULL),
(14, 'Roteiro Oficial PDF', 8.5, '2025-03-06', 4, 3, NULL),
(15, 'Cena 1 Roteiro PDF', NULL, '2025-03-08', 4, 4, NULL),
(16, 'Roteiro Completo PDF', 4.0, '2025-03-13', 4, 5, NULL),
(17, 'Roteiro Atualizado PDF', NULL, '2025-03-10', 4, 6, NULL),
(18, 'Roteiro Revisado PDF', 9.0, '2025-03-04', 4, 7, NULL),
(19, 'Roteiro Final PDF', NULL, '2025-03-01', 4, 8, NULL),

-- Atividade 6 (Lista Individual - variações de "Respostas PDF")
(20, 'Respostas Exercícios PDF', 7.5, '2025-03-05', 6, NULL, 102),
(21, 'Gabarito Lista PDF', NULL, '2025-03-09', 6, NULL, 103),
(22, 'Respostas Completas PDF', 8.0, '2025-03-14', 6, NULL, 104),
(23, 'Soluções Exercícios PDF', NULL, '2025-03-02', 6, NULL, 105),
(24, 'Respostas Revisadas PDF', 6.0, '2025-03-11', 6, NULL, 106),
(25, 'Respostas Finais PDF', 5.5, '2025-03-07', 6, NULL, 107),
(26, 'Lista Resolvida PDF', NULL, '2025-03-03', 6, NULL, 109),
(27, 'Respostas Detalhadas PDF', 9.5, '2025-03-12', 6, NULL, 114);

-- Inserção na tabela ArquivoEntAtv
INSERT INTO arquivoentatv VALUES ('resposta1.pdf', 1);
INSERT INTO arquivoentatv VALUES ('resposta1.zip', 1);
INSERT INTO arquivoentatv VALUES ('lista3.docx', 3);
INSERT INTO arquivoentatv VALUES ('seminario4.rar', 4);
INSERT INTO arquivoentatv VALUES ('lista3.pdf', 3);

-- Inserção na tabela Modulo (CORRIGIDO)
INSERT INTO modulo VALUES (1, 'Modelo ER', '2025-1-EMAP-708-708010-3708-1');
INSERT INTO modulo VALUES (2, 'Ortogonalidade e Espaço Vetorial', '2024-2-ALGLIN-AGRUPADAI');
INSERT INTO modulo VALUES (3, 'Autovalores e Autovetores', '2024-2-ALGLIN-AGRUPADAI');
INSERT INTO modulo VALUES (4, 'Série de Taylor', '2025-1-EMAP-710-710008-710');
INSERT INTO modulo VALUES (5, 'Machine Learning', '2025-1-APRMÁQ-AGRUPADAÁ');

-- Inserção na tabela Topico
INSERT INTO topico VALUES (1, 'Diagonalização', 'Definições e exemplos...', 3);
INSERT INTO topico VALUES (2, 'Espaços Vetoriais', 'Definições e exemplos...', 2);
INSERT INTO topico VALUES (3, 'Autovalores', 'Definições e exemplos...', 3);
INSERT INTO topico VALUES (4, 'Algoritmos Simplex', 'Passo a passo...', 5);
INSERT INTO topico VALUES (5, 'Séries Infinitas', 'Convergência...', 4);

-- Inserção na tabela ArquivoTopico
INSERT INTO arquivotopico VALUES ('autovetores.pdf', 1);
INSERT INTO arquivotopico VALUES ('vetores.pptx', 2);
INSERT INTO arquivotopico VALUES ('diag.pdf', 1);
INSERT INTO arquivotopico VALUES ('simplex.docx', 4);
INSERT INTO arquivotopico VALUES ('autovalores.pdf', 3);