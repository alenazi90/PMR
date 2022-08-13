create user pt with encrypted password 'PTXP@ASS0';
grant all privileges on database ptdb to pt;

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;


CREATE EXTENSION IF NOT EXISTS "uuid-ossp" WITH SCHEMA public;


COMMENT ON EXTENSION "uuid-ossp" IS 'generate universally unique identifiers (UUIDs)';


SET default_tablespace = '';

SET default_table_access_method = heap;


CREATE TABLE public.engagements (
    id uuid DEFAULT public.uuid_generate_v4() NOT NULL,
    name text,
    system_id uuid,
    assigned_to text,
    tester text,
    assets jsonb,
    src_ip text,
    start_date timestamp without time zone,
    end_date timestamp without time zone,
    soc_notification boolean,
    type text,
    status text,
    ts timestamp without time zone DEFAULT timezone('utc'::text, now()),
    category text
);


ALTER TABLE public.engagements OWNER TO pt;


CREATE TABLE public.network_assets (
    system_id uuid,
    ip inet
);


ALTER TABLE public.network_assets OWNER TO pt;


CREATE TABLE public.report_format (
    title text,
    logo text,
    sections jsonb,
    company_name text
);


ALTER TABLE public.report_format OWNER TO pt;


CREATE TABLE public.reports (
    id uuid DEFAULT public.uuid_generate_v4() NOT NULL,
    e_id uuid,
    r_id uuid,
    third_party boolean,
    report_name text,
    report_id text,
    type text,
    scope text,
    findings jsonb,
    c integer,
    h integer,
    l integer,
    m integer,
    r integer,
    tester text,
    recv_date timestamp without time zone,
    ts timestamp without time zone DEFAULT timezone('utc'::text, now())
);


ALTER TABLE public.reports OWNER TO pt;


CREATE TABLE public.systems (
    id uuid DEFAULT public.uuid_generate_v4() NOT NULL,
    name text,
    severity text,
    contact_name text,
    contact_email text,
    department text,
    ts timestamp without time zone DEFAULT timezone('utc'::text, now())
);


ALTER TABLE public.systems OWNER TO pt;


CREATE TABLE public.users (
    id uuid DEFAULT public.uuid_generate_v4() NOT NULL,
    email text NOT NULL,
    name text NOT NULL,
    password text NOT NULL,
    type text,
    admin boolean DEFAULT false,
    change_password boolean DEFAULT true,
    phone text,
    status text DEFAULT 'inactive'::text,
    job_title text,
    created_by text,
    created_at timestamp without time zone DEFAULT timezone('utc'::text, now())
);


ALTER TABLE public.users OWNER TO pt;


CREATE TABLE public.web_assets (
    system_id uuid,
    fqdn text
);


ALTER TABLE public.web_assets OWNER TO pt;


COPY public.engagements (id, name, system_id, assigned_to, tester, assets, src_ip, start_date, end_date, soc_notification, type, status, ts, category) FROM stdin;
\.



COPY public.network_assets (system_id, ip) FROM stdin;
\.



COPY public.report_format (title, logo, sections, company_name) FROM stdin;
	5237583c7dbed40ef8aa99526a216009.png	[]	PT Team
\.



COPY public.reports (id, e_id, r_id, third_party, report_name, report_id, type, scope, findings, c, h, l, m, r, tester, recv_date, ts) FROM stdin;
\.



COPY public.systems (id, name, severity, contact_name, contact_email, department, ts) FROM stdin;
\.



COPY public.users (id, email, name, password, type, admin, change_password, phone, status, job_title, created_by, created_at) FROM stdin;
b32c36c2-231f-4653-8809-fc2e76c63461	tester@pt.local	tester1	$2b$12$Tdbieyt8kQpZBFebJQbHM.zKqU6GVcLqhDgipfYoGyx1ijCaltTv.		f	f		active		admin@pt.local	2022-08-13 07:07:30.409718
49bd3366-d45b-4f5d-bf6b-da596004a574	admin@pt.local	admin	$2b$12$hDq97Ug.8Sb7Xd3bab9UN.ruYB0Toun8eVpNafK3A/qv59FbtUcjm		t	t		active		\N	2022-08-13 07:28:41.030407
a11bbc11-b635-414f-8fcd-e778e8534323	tester2@pt.local	tester2	$2b$12$z0xM.EafIzEidQWRLwkRGuiy4GROqeIu8ZyYUfrAwT9tQCMO0W2m2		f	f		active		admin@pt.local	2022-08-13 07:08:06.617501
\.



COPY public.web_assets (system_id, fqdn) FROM stdin;
\.



ALTER TABLE ONLY public.engagements
    ADD CONSTRAINT engagements_pkey PRIMARY KEY (id);



ALTER TABLE ONLY public.reports
    ADD CONSTRAINT reports_pkey PRIMARY KEY (id);



ALTER TABLE ONLY public.systems
    ADD CONSTRAINT systems_pkey PRIMARY KEY (id);



ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (id);



CREATE INDEX engagements_assets_index ON public.engagements USING btree (assets);



CREATE INDEX report_format_sections_index ON public.report_format USING btree (sections);



CREATE INDEX reports_findings_index ON public.reports USING btree (findings);



CREATE UNIQUE INDEX users_email ON public.users USING btree (email);


--
-- PostgreSQL database dump complete
--

