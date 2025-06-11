-- Geração de 10.000 novos usuários (IDs 1200 a 11199)
INSERT INTO usuario (IDUser, PrimNomeUser, SobrenomeUser, FotoUser, DataNascUser, CidadeUser, EstadoUser, PaisUser)
SELECT 
    id,
    'Nome' || id,
    'Sobrenome' || id,
    CASE WHEN random() < 0.7 THEN 'foto' || id || '.jpg' END,
    CASE 
        WHEN random() < 0.8 THEN DATE '1980-01-01' + (random() * 14600)::int 
        ELSE NULL 
    END,
    CASE WHEN random() < 0.6 THEN 'Cidade' || (random()*100)::int END,
    CASE WHEN random() < 0.5 THEN 'Estado' || (random()*27)::int END,
    CASE 
        WHEN random() < 0.7 THEN 'Brasil'
        WHEN random() < 0.8 THEN 'Argentina'
        WHEN random() < 0.9 THEN 'Chile'
        ELSE 'Uruguai'
    END
FROM generate_series(1200, 11199) AS id;

-- Geração de 100 novas disciplinas (códigos únicos)
INSERT INTO disciplina (CodigoDisc, NomeDisc, PeriodoDisc, FotoDisc)
SELECT 
    '2025-2-DISC-' || LPAD(g::text, 5, '0'),
    'Disciplina ' || (g + 100),  -- Continuando numeração anterior
    CASE 
        WHEN g % 4 = 0 THEN '2025.1'
        WHEN g % 4 = 1 THEN '2025.2'
        WHEN g % 4 = 2 THEN '2026.1'
        ELSE '2026.2'
    END,
    'disc' || (g + 100) || '.jpg'
FROM generate_series(1, 100) g;

-- Atribuição de papéis (todos são alunos)
INSERT INTO aluno (MatriculaAluno, IDUser)
SELECT 
    6000 + id - 1200,  -- Matrículas sequenciais a partir de 6000
    id
FROM generate_series(1200, 11199) id;

-- Professores (10% dos usuários)
INSERT INTO professor (IDUser)
SELECT id 
FROM generate_series(1200, 11199) id
WHERE random() < 0.1;

-- Monitores (15% dos usuários)
INSERT INTO monitor (IDUser)
SELECT id 
FROM generate_series(1200, 11199) id
WHERE random() < 0.15;

-- Associações aluno-disciplina (6 disciplinas por aluno)
INSERT INTO alunodisc (IDUser, CodigoDisc)
SELECT 
    u.id,
    d.CodigoDisc
FROM 
    (SELECT id FROM generate_series(1200, 11199) id) u
CROSS JOIN LATERAL (
    SELECT CodigoDisc
    FROM disciplina
    WHERE CodigoDisc LIKE '2025-2-DISC-%'  -- Somente novas disciplinas
    ORDER BY random()
    LIMIT 6  -- 6 disciplinas por aluno
) d;

-- Associações professor-disciplina (4-6 disciplinas por professor)
INSERT INTO profdisc (IDUser, CodigoDisc)
SELECT 
    p.IDUser,
    d.CodigoDisc
FROM 
    professor p
JOIN generate_series(1, 5) ON true  -- Gerar múltiplas linhas
CROSS JOIN LATERAL (
    SELECT CodigoDisc
    FROM disciplina
    WHERE CodigoDisc LIKE '2025-2-DISC-%'
    ORDER BY random()
    LIMIT 1
) d
WHERE p.IDUser BETWEEN 1200 AND 11199
GROUP BY p.IDUser, d.CodigoDisc
HAVING COUNT(*) BETWEEN 4 AND 6;

-- Associações monitor-disciplina (3-5 disciplinas por monitor)
INSERT INTO monitdisc (IDUser, CodigoDisc)
SELECT 
    m.IDUser,
    d.CodigoDisc
FROM 
    monitor m
JOIN generate_series(1, 4) ON true  -- Gerar múltiplas linhas
CROSS JOIN LATERAL (
    SELECT CodigoDisc
    FROM disciplina
    WHERE CodigoDisc LIKE '2025-2-DISC-%'
    ORDER BY random()
    LIMIT 1
) d
WHERE m.IDUser BETWEEN 1200 AND 11199
GROUP BY m.IDUser, d.CodigoDisc
HAVING COUNT(*) BETWEEN 3 AND 5;