CREATE TABLE operadoras (
    id SERIAL PRIMARY KEY,
    registro_ans VARCHAR(50) UNIQUE,
    razao_social VARCHAR(255),
    nome_fantasia VARCHAR(255),
    modalidade VARCHAR(100),
    uf VARCHAR(10),
    municipio VARCHAR(100),
    cnpj VARCHAR(20)
);

CREATE TABLE demonstrativos_financeiros (
    id SERIAL PRIMARY KEY,
    registro_ans VARCHAR(50),
    ano INT,
    trimestre INT,
    receita_total DECIMAL(15,2),
    despesas_eventos_medico_hospitalares DECIMAL(15,2),
    FOREIGN KEY (registro_ans) REFERENCES operadoras(registro_ans)
);
LOAD DATA INFILE '/caminho/do/arquivo/operadoras_ativas.csv' 
INTO TABLE operadoras 
FIELDS TERMINATED BY ',' 
ENCLOSED BY '"' 
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;

LOAD DATA INFILE '/caminho/do/arquivo/demonstrativos_financeiros.csv' 
INTO TABLE demonstrativos_financeiros 
FIELDS TERMINATED BY ',' 
ENCLOSED BY '"' 
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;
SELECT o.nome_fantasia, SUM(d.despesas_eventos_medico_hospitalares) AS total_despesas
FROM demonstrativos_financeiros d
JOIN operadoras o ON d.registro_ans = o.registro_ans
WHERE d.ano = EXTRACT(YEAR FROM CURRENT_DATE)
AND d.trimestre = (SELECT MAX(trimestre) FROM demonstrativos_financeiros WHERE ano = EXTRACT(YEAR FROM CURRENT_DATE))
GROUP BY o.nome_fantasia
ORDER BY total_despesas DESC
LIMIT 10;
SELECT o.nome_fantasia, SUM(d.despesas_eventos_medico_hospitalares) AS total_despesas
FROM demonstrativos_financeiros d
JOIN operadoras o ON d.registro_ans = o.registro_ans
WHERE d.ano = EXTRACT(YEAR FROM CURRENT_DATE) - 1
GROUP BY o.nome_fantasia
ORDER BY total_despesas DESC
LIMIT 10;
