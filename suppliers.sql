--
-- PostgreSQL database dump
--

-- Dumped from database version 9.5.14
-- Dumped by pg_dump version 9.5.14

SET statement_timeout = 0;
SET lock_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_with_oids = false;

--
-- Name: suppliers; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.suppliers (
    id integer NOT NULL,
    page_id bigint,
    name character varying(100),
    page_likes integer DEFAULT 0 NOT NULL,
    has_community boolean DEFAULT false NOT NULL
);


ALTER TABLE public.suppliers OWNER TO postgres;

--
-- Name: suppliers_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.suppliers_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.suppliers_id_seq OWNER TO postgres;

--
-- Name: suppliers_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.suppliers_id_seq OWNED BY public.suppliers.id;


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.suppliers ALTER COLUMN id SET DEFAULT nextval('public.suppliers_id_seq'::regclass);


--
-- Data for Name: suppliers; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.suppliers (id, page_id, name, page_likes, has_community) FROM stdin;
30	1951319155178263	red energy	500	f
72	861710020579956	mojo energy	1300	f
73	513775645300027	alinta energy	113000	f
76	177105938998285	energex	30000	f
79	174840539202952	eragon energy	57000	f
77	163654623651345	synergy	10000	t
75	132698030081760	lumo energy	29000	t
78	450839735088078	globird energy	900	t
3	274936216352431	simply energy	1300	t
14	182118848546753	agl energy	30000	t
15	694623690675659	energy locals	1000	t
17	107439929605808	blue nrg	1300	t
19	749876598432608	sumo power	600	t
26	206261246078617	origin energy	148000	t
22	171046109678677	powershop	25000	t
16	260823190756616	eragon energy retail	23000	t
2	539309746236829	energy australia	48000	t
8	300358693344280	momentum energy	3000	t
80	163311407061785	dodo	50000	t
81	580634115366813	covau energy	2500	t
82	121069921288505	click energy	8000	f
74	900645420112406	power direct	4500	f
\.


--
-- Name: suppliers_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.suppliers_id_seq', 83, true);


--
-- Name: suppliers_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.suppliers
    ADD CONSTRAINT suppliers_pkey PRIMARY KEY (id);


--
-- Name: uniq_supplier; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.suppliers
    ADD CONSTRAINT uniq_supplier UNIQUE (name, page_id);


--
-- PostgreSQL database dump complete
--

