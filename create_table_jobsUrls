CREATE TABLE public."jobsUrls"
(
    id bigint NOT NULL GENERATED ALWAYS AS IDENTITY ( INCREMENT 1 START 1 MINVALUE 1 MAXVALUE 9223372036854775807 CACHE 1 ),
    "Urls" character varying(250) COLLATE pg_catalog."default" NOT NULL,
    "Is_Scraped" boolean NOT NULL DEFAULT false,
    "Job_ID" integer,
    "timestamp" time without time zone DEFAULT (now())::timestamp without time zone,
    CONSTRAINT "jobsUrls_pkey" PRIMARY KEY (id),
    CONSTRAINT "unique_Job_ID" UNIQUE ("Job_ID")
)
TABLESPACE pg_default;

ALTER TABLE public."jobsUrls"
    OWNER to postgres;

COMMENT ON CONSTRAINT "unique_Job_ID" ON public."jobsUrls"
    IS 'restrict to save duplicate job id';
