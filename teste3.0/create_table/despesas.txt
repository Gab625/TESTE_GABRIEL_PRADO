-- Table: public.despesas

-- DROP TABLE IF EXISTS public.despesas;

CREATE TABLE IF NOT EXISTS public.despesas
(
    cnpj character varying(20) COLLATE pg_catalog."default",
    razao_social text COLLATE pg_catalog."default",
    trimestre integer,
    ano integer,
    valordespesas numeric(20,2)
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.despesas
    OWNER to postgres;