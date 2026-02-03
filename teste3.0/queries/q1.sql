WITH valores_extremos AS ( --tabela temporaria
    SELECT 
        cnpj,
        razao_social,
        FIRST_VALUE(valordespesas) OVER (
            PARTITION BY cnpj 
            ORDER BY ano, trimestre 
            ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED following --comando para o sql olhar o conjunto inteiro da empresa
        ) as valor_inicial,
        LAST_VALUE(valordespesas) OVER (
            PARTITION BY cnpj 
            ORDER BY ano, trimestre 
            ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING
        ) as valor_final
    FROM despesas
    WHERE valordespesas > 0
)
SELECT 
    cnpj,
    razao_social,
    valor_inicial,
    valor_final,
    ROUND(
        ((valor_final - valor_inicial) / NULLIF(valor_inicial, 0)) * 100, --nullif transforma o 0 em null para nao travar a query
        2
    ) as crescimento_total_pct
FROM valores_extremos
WHERE valor_inicial > 0
GROUP BY cnpj, razao_social, valor_inicial, valor_final
ORDER BY crescimento_total_pct DESC
LIMIT 5;