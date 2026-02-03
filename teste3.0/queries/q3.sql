WITH media_geral AS (
    SELECT AVG(valordespesas) as valor_medio 
    FROM despesas 
    WHERE valordespesas > 0
),
analise_trimestral AS (
    SELECT 
        d.cnpj,
        COUNT(*) as trimestres_acima_da_media
    FROM despesas d, media_geral m
    WHERE d.valordespesas > m.valor_medio
    GROUP BY d.cnpj
    HAVING COUNT(*) >= 2
)
SELECT 
    o.razao_social,
    o.uf,
    a.trimestres_acima_da_media
FROM analise_trimestral a
JOIN operadoras o ON a.cnpj = o.cnpj
ORDER BY a.trimestres_acima_da_media DESC, o.razao_social ASC;