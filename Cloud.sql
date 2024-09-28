--
-- PostgreSQL database dump
--

-- Dumped from database version 15.8 (Debian 15.8-0+deb12u1)
-- Dumped by pg_dump version 15.8 (Debian 15.8-0+deb12u1)

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

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: delete_account; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.delete_account (
    id integer NOT NULL,
    user_id integer,
    email bytea NOT NULL,
    deleted boolean
);


ALTER TABLE public.delete_account OWNER TO admin;

--
-- Name: delete_account_id_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

CREATE SEQUENCE public.delete_account_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.delete_account_id_seq OWNER TO admin;

--
-- Name: delete_account_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE public.delete_account_id_seq OWNED BY public.delete_account.id;


--
-- Name: feedback; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.feedback (
    id integer NOT NULL,
    name bytea,
    email bytea,
    text bytea,
    fixed boolean,
    date timestamp with time zone
);


ALTER TABLE public.feedback OWNER TO admin;

--
-- Name: feedback_id_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

CREATE SEQUENCE public.feedback_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.feedback_id_seq OWNER TO admin;

--
-- Name: feedback_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE public.feedback_id_seq OWNED BY public.feedback.id;


--
-- Name: file; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.file (
    id integer NOT NULL,
    filename bytea,
    filepath bytea,
    private_key_path bytea,
    public_key_path bytea,
    user_id integer NOT NULL,
    mimetype bytea,
    date timestamp with time zone
);


ALTER TABLE public.file OWNER TO admin;

--
-- Name: file_id_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

CREATE SEQUENCE public.file_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.file_id_seq OWNER TO admin;

--
-- Name: file_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE public.file_id_seq OWNED BY public.file.id;


--
-- Name: text; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.text (
    id integer NOT NULL,
    user_id integer NOT NULL,
    "encrypted_Key" bytea NOT NULL,
    nonce bytea NOT NULL,
    ciphertext bytea NOT NULL,
    private_key_path bytea NOT NULL,
    public_key_path bytea NOT NULL,
    store_type bytea NOT NULL,
    date timestamp without time zone
);


ALTER TABLE public.text OWNER TO admin;

--
-- Name: text_id_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

CREATE SEQUENCE public.text_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.text_id_seq OWNER TO admin;

--
-- Name: text_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE public.text_id_seq OWNED BY public.text.id;


--
-- Name: user; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public."user" (
    id integer NOT NULL,
    username bytea,
    email bytea,
    password character varying NOT NULL,
    date timestamp with time zone,
    role character varying NOT NULL,
    path bytea,
    is_verified boolean,
    verification_token character varying,
    used_storage integer,
    limited_storage integer NOT NULL
);


ALTER TABLE public."user" OWNER TO admin;

--
-- Name: user_id_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

CREATE SEQUENCE public.user_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.user_id_seq OWNER TO admin;

--
-- Name: user_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE public.user_id_seq OWNED BY public."user".id;


--
-- Name: delete_account id; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.delete_account ALTER COLUMN id SET DEFAULT nextval('public.delete_account_id_seq'::regclass);


--
-- Name: feedback id; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.feedback ALTER COLUMN id SET DEFAULT nextval('public.feedback_id_seq'::regclass);


--
-- Name: file id; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.file ALTER COLUMN id SET DEFAULT nextval('public.file_id_seq'::regclass);


--
-- Name: text id; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.text ALTER COLUMN id SET DEFAULT nextval('public.text_id_seq'::regclass);


--
-- Name: user id; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public."user" ALTER COLUMN id SET DEFAULT nextval('public.user_id_seq'::regclass);


--
-- Name: delete_account delete_account_email_key; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.delete_account
    ADD CONSTRAINT delete_account_email_key UNIQUE (email);


--
-- Name: delete_account delete_account_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.delete_account
    ADD CONSTRAINT delete_account_pkey PRIMARY KEY (id);


--
-- Name: feedback feedback_email_key; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.feedback
    ADD CONSTRAINT feedback_email_key UNIQUE (email);


--
-- Name: feedback feedback_name_key; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.feedback
    ADD CONSTRAINT feedback_name_key UNIQUE (name);


--
-- Name: feedback feedback_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.feedback
    ADD CONSTRAINT feedback_pkey PRIMARY KEY (id);


--
-- Name: feedback feedback_text_key; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.feedback
    ADD CONSTRAINT feedback_text_key UNIQUE (text);


--
-- Name: file file_filename_key; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.file
    ADD CONSTRAINT file_filename_key UNIQUE (filename);


--
-- Name: file file_filepath_key; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.file
    ADD CONSTRAINT file_filepath_key UNIQUE (filepath);


--
-- Name: file file_mimetype_key; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.file
    ADD CONSTRAINT file_mimetype_key UNIQUE (mimetype);


--
-- Name: file file_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.file
    ADD CONSTRAINT file_pkey PRIMARY KEY (id);


--
-- Name: file file_private_key_path_key; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.file
    ADD CONSTRAINT file_private_key_path_key UNIQUE (private_key_path);


--
-- Name: file file_public_key_path_key; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.file
    ADD CONSTRAINT file_public_key_path_key UNIQUE (public_key_path);


--
-- Name: text text_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.text
    ADD CONSTRAINT text_pkey PRIMARY KEY (id);


--
-- Name: user user_email_key; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public."user"
    ADD CONSTRAINT user_email_key UNIQUE (email);


--
-- Name: user user_path_key; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public."user"
    ADD CONSTRAINT user_path_key UNIQUE (path);


--
-- Name: user user_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public."user"
    ADD CONSTRAINT user_pkey PRIMARY KEY (id);


--
-- Name: user user_username_key; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public."user"
    ADD CONSTRAINT user_username_key UNIQUE (username);


--
-- Name: file file_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.file
    ADD CONSTRAINT file_user_id_fkey FOREIGN KEY (user_id) REFERENCES public."user"(id);


--
-- Name: text text_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.text
    ADD CONSTRAINT text_user_id_fkey FOREIGN KEY (user_id) REFERENCES public."user"(id);


--
-- Name: SCHEMA public; Type: ACL; Schema: -; Owner: pg_database_owner
--

GRANT ALL ON SCHEMA public TO admin;


--
-- PostgreSQL database dump complete
--

