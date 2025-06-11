-- TESTE 1

-- Verifica se já não existe o indice
DROP INDEX IF EXISTS nome_index;
-- Testa sem o indice
EXPLAIN ANALYZE SELECT * FROM usuario WHERE primnomeuser = 'Henrique';
-- Cria o indice
CREATE INDEX nome_index ON usuario (primnomeuser);
-- Testa com o indice
EXPLAIN ANALYZE SELECT * FROM usuario WHERE primnomeuser = 'Henrique';
-- Deleta o indice
DROP INDEX nome_index;

-- TESTE 2

-- Desabilita o uso de índices para forçar varredura sequencial
SET enable_indexscan = OFF;
SET enable_bitmapscan = OFF;
SET enable_tidscan = OFF;

-- EXPLAIN ANALYZE sem índices
EXPLAIN ANALYZE
SELECT d.nomedisc, 'Aluno' as papel
FROM alunodisc ad
JOIN disciplina d ON ad.codigodisc = d.codigodisc
WHERE ad.iduser = 103
UNION ALL
SELECT d.nomedisc, 'Professor' as papel
FROM profdisc pd
JOIN disciplina d ON pd.codigodisc = d.codigodisc
WHERE pd.iduser = 103
UNION ALL
SELECT d.nomedisc, 'Monitor' as papel
FROM monitdisc md
JOIN disciplina d ON md.codigodisc = d.codigodisc
WHERE md.iduser = 103
ORDER BY nomedisc, papel;

-- Reativa o uso de índices
SET enable_indexscan = ON;
SET enable_bitmapscan = ON;
SET enable_tidscan = ON;

-- Cria índices temporários nas colunas iduser
CREATE INDEX idx_temp_alunodisc_iduser ON alunodisc(iduser);
CREATE INDEX idx_temp_profdisc_iduser ON profdisc(iduser);
CREATE INDEX idx_temp_monitdisc_iduser ON monitdisc(iduser);

-- EXPLAIN ANALYZE com índices
EXPLAIN ANALYZE
SELECT d.nomedisc, 'Aluno' as papel
FROM alunodisc ad
JOIN disciplina d ON ad.codigodisc = d.codigodisc
WHERE ad.iduser = 103
UNION ALL
SELECT d.nomedisc, 'Professor' as papel
FROM profdisc pd
JOIN disciplina d ON pd.codigodisc = d.codigodisc
WHERE pd.iduser = 103
UNION ALL
SELECT d.nomedisc, 'Monitor' as papel
FROM monitdisc md
JOIN disciplina d ON md.codigodisc = d.codigodisc
WHERE md.iduser = 103
ORDER BY nomedisc, papel;

-- Executa a consulta real (sem análise)
SELECT d.nomedisc, 'Aluno' as papel
FROM alunodisc ad
JOIN disciplina d ON ad.codigodisc = d.codigodisc
WHERE ad.iduser = 103
UNION ALL
SELECT d.nomedisc, 'Professor' as papel
FROM profdisc pd
JOIN disciplina d ON pd.codigodisc = d.codigodisc
WHERE pd.iduser = 103
UNION ALL
SELECT d.nomedisc, 'Monitor' as papel
FROM monitdisc md
JOIN disciplina d ON md.codigodisc = d.codigodisc
WHERE md.iduser = 103
ORDER BY nomedisc, papel;

-- Remove os índices temporários
DROP INDEX IF EXISTS idx_temp_alunodisc_iduser;
DROP INDEX IF EXISTS idx_temp_profdisc_iduser;
DROP INDEX IF EXISTS idx_temp_monitdisc_iduser;