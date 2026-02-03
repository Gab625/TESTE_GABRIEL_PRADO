SELECT 
    o.uf,
    SUM(d.total_despesas ) AS despesa_total_uf,
    ROUND(SUM(d.total_despesas) / COUNT(DISTINCT o.cnpj), 2) AS media_por_operadora,
    COUNT(DISTINCT o.cnpj) AS qtd_operadoras
FROM despesas_agregadas d
JOIN operadoras o ON d.cnpj = o.cnpj
WHERE d.total_despesas  > 0
GROUP BY o.uf
ORDER BY despesa_total_uf DESC
LIMIT 5;