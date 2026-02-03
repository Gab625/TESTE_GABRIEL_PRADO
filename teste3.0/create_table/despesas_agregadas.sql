-- Table: public.despesas_agregadas

-- DROP TABLE IF EXISTS public.despesas_agregadas;

CREATE TABLE IF NOT EXISTS public.despesas_agregadas
(
    razao_social text COLLATE pg_catalog."default",
    uf character varying(10) COLLATE pg_catalog."default",
    cnpj character varying(20) COLLATE pg_catalog."default",
    registro_ans character varying(20) COLLATE pg_catalog."default",
    modalidade character varying(100) COLLATE pg_catalog."default",
    total_despesas numeric(25,5),
    media_trimestral numeric(25,5),
    desvio_padrao numeric(25,5)
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.despesas_agregadas
    OWNER to postgres;