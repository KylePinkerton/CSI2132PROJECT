-- CSI2132 Winter 2020 Project
-- A list of all the DDLs used


------------------------------------------------

-- Table: project.branches

-- DROP TABLE project.branches;

CREATE TABLE project.branches
(
    country character varying(20) COLLATE pg_catalog."default" NOT NULL,
    branch_name character varying(20) COLLATE pg_catalog."default" NOT NULL,
    street_number numeric(5,0) NOT NULL,
    street_name character varying(20) COLLATE pg_catalog."default" NOT NULL,
    apt_number numeric(5,0),
    province character varying(20) COLLATE pg_catalog."default" NOT NULL,
    postal_code character varying(20) COLLATE pg_catalog."default" NOT NULL,
    CONSTRAINT branches_pkey PRIMARY KEY (country)
)
WITH (
    OIDS = FALSE
)
TABLESPACE pg_default;

ALTER TABLE project.branches
    OWNER to kpink074;

------------------------------------------------

-- Table: project.person

-- DROP TABLE project.person;

CREATE TABLE project.person
(
    username character varying(20) COLLATE pg_catalog."default" NOT NULL,
    first_name character varying(20) COLLATE pg_catalog."default" NOT NULL,
    middle_name character varying(20) COLLATE pg_catalog."default",
    last_name character varying(20) COLLATE pg_catalog."default" NOT NULL,
    password character varying(20) COLLATE pg_catalog."default" NOT NULL,
    country character varying(20) COLLATE pg_catalog."default" NOT NULL,
    street_number numeric(5,0) NOT NULL,
    street_name character varying(20) COLLATE pg_catalog."default" NOT NULL,
    apt_number numeric(5,0),
    province character varying(20) COLLATE pg_catalog."default" NOT NULL,
    postal_code character varying(20) COLLATE pg_catalog."default" NOT NULL,
    date_of_birth date NOT NULL,
    CONSTRAINT person_pkey PRIMARY KEY (username),
    CONSTRAINT person_country_fkey FOREIGN KEY (country)
        REFERENCES project.branches (country) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE CASCADE
)
WITH (
    OIDS = FALSE
)
TABLESPACE pg_default;

ALTER TABLE project.person
    OWNER to kpink074;

------------------------------------------------

-- Table: project.users

-- DROP TABLE project.users;

CREATE TABLE project.users
(
    username character varying(20) COLLATE pg_catalog."default" NOT NULL,
    join_date date NOT NULL,
    verified boolean NOT NULL,
    about text COLLATE pg_catalog."default" NOT NULL,
    languages text COLLATE pg_catalog."default" NOT NULL,
    work text COLLATE pg_catalog."default" NOT NULL,
    profile_picture character varying(20) NOT NULL,
    CONSTRAINT users_pkey PRIMARY KEY (username),
    CONSTRAINT users_username_fkey FOREIGN KEY (username)
        REFERENCES project.person (username) MATCH SIMPLE
        ON UPDATE CASCADE
        ON DELETE CASCADE
)
WITH (
    OIDS = FALSE
)
TABLESPACE pg_default;

ALTER TABLE project.users
    OWNER to kpink074;

------------------------------------------------

-- Table: project.property

-- DROP TABLE project.property;

CREATE TABLE project.property
(
    propertyname character varying(20) COLLATE pg_catalog."default" NOT NULL,
    street_number numeric(5,0) NOT NULL,
    street_name character varying(20) COLLATE pg_catalog."default" NOT NULL,
    apt_number numeric(5,0),
    province character varying(20) COLLATE pg_catalog."default" NOT NULL,
    postal_code character varying(20) COLLATE pg_catalog."default" NOT NULL,
    rent_rate numeric(8,2) NOT NULL,
    property_type character varying(20) COLLATE pg_catalog."default" NOT NULL,
    max_guests numeric(2,0) NOT NULL,
    number_beds numeric(2,0) NOT NULL,
    number_baths numeric(2,0) NOT NULL,
    accessible boolean NOT NULL,
    pets_allowed boolean NOT NULL,
    country character varying(20) COLLATE pg_catalog."default" NOT NULL,
    hostusername character varying(20) COLLATE pg_catalog."default" NOT NULL,
    picture character varying(20) COLLATE pg_catalog."default" NOT NULL,
    CONSTRAINT property_pkey PRIMARY KEY (propertyname),
    CONSTRAINT property_country_fkey FOREIGN KEY (country)
        REFERENCES project.branches (country) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE CASCADE,
    CONSTRAINT property_hostusername_fkey FOREIGN KEY (hostusername)
        REFERENCES project.users (username) MATCH SIMPLE
        ON UPDATE CASCADE
        ON DELETE CASCADE,
    CONSTRAINT property_rent_rate_check CHECK (rent_rate > 0::numeric),
    CONSTRAINT property_type_check CHECK (property_type::text = 'entire'::text OR property_type::text = 'private'::text OR property_type::text = 'shared'::text),
    CONSTRAINT property_max_guests_check CHECK (max_guests > 0::numeric),
    CONSTRAINT property_number_beds_check CHECK (number_beds > 0::numeric),
    CONSTRAINT property_number_baths_check CHECK (number_baths > 0::numeric)
)
WITH (
    OIDS = FALSE
)
TABLESPACE pg_default;

ALTER TABLE project.property
    OWNER to kpink074;

------------------------------------------------

-- Table: project.property_taken_dates

-- DROP TABLE project.property_taken_dates;

CREATE TABLE project.property_taken_dates
(
    propertyname character varying(20) COLLATE pg_catalog."default" NOT NULL,
    taken_date date NOT NULL,
    CONSTRAINT property_taken_dates_pkey PRIMARY KEY (propertyname, taken_date),
    CONSTRAINT property_taken_dates_propertyname_fkey FOREIGN KEY (propertyname)
        REFERENCES project.property (propertyname) MATCH SIMPLE
        ON UPDATE CASCADE
        ON DELETE CASCADE
)
WITH (
    OIDS = FALSE
)
TABLESPACE pg_default;

ALTER TABLE project.property_taken_dates
    OWNER to kpink074;

------------------------------------------------

-- Table: project.property_review

-- DROP TABLE project.property_review;

CREATE TABLE project.property_review
(
    username character varying(20) COLLATE pg_catalog."default" NOT NULL,
    propertyname character varying(20) COLLATE pg_catalog."default" NOT NULL,
    CONSTRAINT property_review_pkey PRIMARY KEY (username, propertyname),
    CONSTRAINT property_review_propertyname_fkey FOREIGN KEY (propertyname)
        REFERENCES project.property (propertyname) MATCH SIMPLE
        ON UPDATE CASCADE
        ON DELETE CASCADE,
    CONSTRAINT property_review_username_fkey FOREIGN KEY (username)
        REFERENCES project.users (username) MATCH SIMPLE
        ON UPDATE CASCADE
        ON DELETE CASCADE
)
WITH (
    OIDS = FALSE
)
TABLESPACE pg_default;

ALTER TABLE project.property_review
    OWNER to kpink074;

------------------------------------------------

-- Table: project.property_review_details

-- DROP TABLE project.property_review_details;

CREATE TABLE project.property_review_details
(
    username character varying(20) COLLATE pg_catalog."default" NOT NULL,
    propertyname character varying(20) COLLATE pg_catalog."default" NOT NULL,
    "time" timestamp without time zone NOT NULL,
    communication numeric(2,1) NOT NULL,
    value numeric(2,1) NOT NULL,
    check_in numeric(2,1) NOT NULL,
    accuracy numeric(2,1) NOT NULL,
    cleanliness numeric(2,1) NOT NULL,
    location numeric(2,1) NOT NULL,
    review_content text COLLATE pg_catalog."default",
    CONSTRAINT property_review_details_pkey PRIMARY KEY (username, propertyname, "time"),
    CONSTRAINT property_review_details_username_fkey FOREIGN KEY (propertyname, username)
        REFERENCES project.property_review (propertyname, username) MATCH SIMPLE
        ON UPDATE CASCADE
        ON DELETE CASCADE,
    CONSTRAINT property_review_details_communication_check CHECK (communication >= 0::numeric AND communication <= 5::numeric),
    CONSTRAINT property_review_details_value_check CHECK (value >= 0::numeric AND value <= 5::numeric),
    CONSTRAINT property_review_details_check_in_check CHECK (check_in >= 0::numeric AND check_in <= 5::numeric),
    CONSTRAINT property_review_details_accuracy_check CHECK (accuracy >= 0::numeric AND accuracy <= 5::numeric),
    CONSTRAINT property_review_details_cleanliness_check CHECK (cleanliness >= 0::numeric AND cleanliness <= 5::numeric),
    CONSTRAINT property_review_details_location_check CHECK (location >= 0::numeric AND location <= 5::numeric)
)
WITH (
    OIDS = FALSE
)
TABLESPACE pg_default;

ALTER TABLE project.property_review_details
    OWNER to kpink074;

------------------------------------------------

-- Table: project.rental_agreement

-- DROP TABLE project.rental_agreement;

CREATE TABLE project.rental_agreement
(
    rental_id character varying(20) COLLATE pg_catalog."default" NOT NULL,
    start_date date NOT NULL,
    end_date date NOT NULL,
    sign_date date NOT NULL,
    travelling_for_work boolean NOT NULL,
    message_to_host text COLLATE pg_catalog."default" NOT NULL,
    total_price numeric(8,2) NOT NULL,
    host_accepted boolean NOT NULL,
    propertyname character varying(20) COLLATE pg_catalog."default" NOT NULL,
    guestusername character varying(20) COLLATE pg_catalog."default" NOT NULL,
    hostusername character varying(20) COLLATE pg_catalog."default" NOT NULL,
    CONSTRAINT rental_agreement_pkey PRIMARY KEY (rental_id),
    CONSTRAINT rental_agreement_guestusername_fkey FOREIGN KEY (guestusername)
        REFERENCES project.users (username) MATCH SIMPLE
        ON UPDATE CASCADE
        ON DELETE SET NULL,
    CONSTRAINT rental_agreement_hostusername_fkey FOREIGN KEY (hostusername)
        REFERENCES project.users (username) MATCH SIMPLE
        ON UPDATE CASCADE
        ON DELETE SET NULL,
    CONSTRAINT rental_agreement_propertyname_fkey FOREIGN KEY (propertyname)
        REFERENCES project.property (propertyname) MATCH SIMPLE
        ON UPDATE CASCADE
        ON DELETE SET NULL,
    CONSTRAINT rental_agreement_total_price_check CHECK (total_price > 0::numeric)
)
WITH (
    OIDS = FALSE
)
TABLESPACE pg_default;

ALTER TABLE project.rental_agreement
    OWNER to kpink074;

------------------------------------------------

-- Table: project.employees

-- DROP TABLE project.employees;

CREATE TABLE project.employees
(
    username character varying(20) COLLATE pg_catalog."default" NOT NULL,
    title text COLLATE pg_catalog."default" NOT NULL,
    salary numeric(8,2) NOT NULL,
    country character varying(20) COLLATE pg_catalog."default" NOT NULL,
    managerusername character varying(20) COLLATE pg_catalog."default",
    CONSTRAINT employees_pkey PRIMARY KEY (username),
    CONSTRAINT employees_country_fkey FOREIGN KEY (country)
        REFERENCES project.branches (country) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE CASCADE,
    CONSTRAINT employees_username_fkey FOREIGN KEY (username)
        REFERENCES project.person (username) MATCH SIMPLE
        ON UPDATE CASCADE
        ON DELETE CASCADE,
    CONSTRAINT employees_managerusername_fkey FOREIGN KEY (managerusername)
        REFERENCES project.employees (username) MATCH SIMPLE
        ON UPDATE CASCADE
        ON DELETE SET NULL,
    CONSTRAINT employees_salary_check CHECK (salary > 0::numeric)
)
WITH (
    OIDS = FALSE
)
TABLESPACE pg_default;

ALTER TABLE project.employees
    OWNER to kpink074;

------------------------------------------------

-- Table: project.admins

-- DROP TABLE project.admins;

CREATE TABLE project.admins
(
    username character varying(20) COLLATE pg_catalog."default",
    CONSTRAINT admins_pkey PRIMARY KEY (username),
    CONSTRAINT admins_username2_fkey FOREIGN KEY (username)
        REFERENCES project.employees (username) MATCH SIMPLE
        ON UPDATE CASCADE
        ON DELETE CASCADE,
    CONSTRAINT admins_username_fkey FOREIGN KEY (username)
        REFERENCES project.person (username) MATCH SIMPLE
        ON UPDATE CASCADE
        ON DELETE CASCADE
)
WITH (
    OIDS = FALSE
)
TABLESPACE pg_default;

ALTER TABLE project.admins
    OWNER to kpink074;

------------------------------------------------

-- Table: project.works_at

-- DROP TABLE project.works_at;

CREATE TABLE project.works_at
(
    employeeusername character varying(20) COLLATE pg_catalog."default" NOT NULL,
    propertyname character varying(20) COLLATE pg_catalog."default" NOT NULL,
    CONSTRAINT works_at_pkey PRIMARY KEY (employeeusername, propertyname),
    CONSTRAINT works_at_employeeusername_fkey FOREIGN KEY (employeeusername)
        REFERENCES project.employees (username) MATCH SIMPLE
        ON UPDATE CASCADE
        ON DELETE CASCADE,
    CONSTRAINT works_at_propertyname_fkey FOREIGN KEY (propertyname)
        REFERENCES project.property (propertyname) MATCH SIMPLE
        ON UPDATE CASCADE
        ON DELETE CASCADE
)
WITH (
    OIDS = FALSE
)
TABLESPACE pg_default;

ALTER TABLE project.works_at
    OWNER to kpink074;

------------------------------------------------
-- Table: project.conversation

-- DROP TABLE project.conversation;

CREATE TABLE project.conversation
(
    senderusername character varying(20) COLLATE pg_catalog."default" NOT NULL,
    receiverusername character varying(20) COLLATE pg_catalog."default" NOT NULL,
    CONSTRAINT conversation_pkey PRIMARY KEY (senderusername, receiverusername),
    CONSTRAINT conversation_receiverusername_fkey FOREIGN KEY (receiverusername)
        REFERENCES project.person (username) MATCH SIMPLE
        ON UPDATE CASCADE
        ON DELETE CASCADE,
    CONSTRAINT conversation_senderusername_fkey FOREIGN KEY (senderusername)
        REFERENCES project.person (username) MATCH SIMPLE
        ON UPDATE CASCADE
        ON DELETE CASCADE
)
WITH (
    OIDS = FALSE
)
TABLESPACE pg_default;

ALTER TABLE project.conversation
    OWNER to kpink074;

------------------------------------------------

-- Table: project.conversation_messages

-- DROP TABLE project.conversation_messages;

CREATE TABLE project.conversation_messages
(
    senderusername character varying(20) COLLATE pg_catalog."default" NOT NULL,
    receiverusername character varying(20) COLLATE pg_catalog."default" NOT NULL,
    "time" timestamp without time zone NOT NULL,
    message_content text COLLATE pg_catalog."default" NOT NULL,
    CONSTRAINT conversation_messages_pkey PRIMARY KEY (senderusername, receiverusername, "time"),
    CONSTRAINT conversation_messages_senderusername_fkey FOREIGN KEY (receiverusername, senderusername)
        REFERENCES project.conversation (receiverusername, senderusername) MATCH SIMPLE
        ON UPDATE CASCADE
        ON DELETE CASCADE
)
WITH (
    OIDS = FALSE
)
TABLESPACE pg_default;

ALTER TABLE project.conversation_messages
    OWNER to kpink074;

------------------------------------------------

-- Table: project.payment

-- DROP TABLE project.payment;

CREATE TABLE project.payment
(
    payment_id character varying(20) COLLATE pg_catalog."default" NOT NULL,
    is_deposit boolean NOT NULL,
    amount numeric(8,2) NOT NULL,
    status character varying(20) COLLATE pg_catalog."default" NOT NULL,
    rental_id character varying(20) COLLATE pg_catalog."default" NOT NULL,
    guestusername character varying(20) COLLATE pg_catalog."default" NOT NULL,
    hostusername character varying(20) COLLATE pg_catalog."default" NOT NULL,
    CONSTRAINT payment_pkey PRIMARY KEY (payment_id),
    CONSTRAINT payment_guestusername_fkey FOREIGN KEY (guestusername)
        REFERENCES project.users (username) MATCH SIMPLE
        ON UPDATE CASCADE
        ON DELETE SET NULL,
    CONSTRAINT payment_hostusername_fkey FOREIGN KEY (hostusername)
        REFERENCES project.users (username) MATCH SIMPLE
        ON UPDATE CASCADE
        ON DELETE SET NULL,
    CONSTRAINT payment_rental_id_fkey FOREIGN KEY (rental_id)
        REFERENCES project.rental_agreement (rental_id) MATCH SIMPLE
        ON UPDATE CASCADE
        ON DELETE SET NULL,
    CONSTRAINT payment_amount_check CHECK (amount > 0::numeric),
    CONSTRAINT payment_status_check CHECK (status::text = 'approved'::text OR status::text = 'pending'::text)
)
WITH (
    OIDS = FALSE
)
TABLESPACE pg_default;

ALTER TABLE project.payment
    OWNER to kpink074;

------------------------------------------------

-- Table: project.payment_method

-- DROP TABLE project.payment_method;

CREATE TABLE project.payment_method
(
    username character varying(20) COLLATE pg_catalog."default" NOT NULL,
    card_type character varying(20) COLLATE pg_catalog."default" NOT NULL,
    first_name character varying(20) COLLATE pg_catalog."default" NOT NULL,
    last_name character varying(20) COLLATE pg_catalog."default" NOT NULL,
    card_number character varying(20) COLLATE pg_catalog."default" NOT NULL,
    card_expiration date NOT NULL,
    cvv character varying(3) COLLATE pg_catalog."default" NOT NULL,
    billing_country character varying(20) COLLATE pg_catalog."default" NOT NULL,
    CONSTRAINT payment_method_pkey PRIMARY KEY (username),
    CONSTRAINT payment_method_username_fkey FOREIGN KEY (username)
        REFERENCES project.users (username) MATCH SIMPLE
        ON UPDATE CASCADE
        ON DELETE CASCADE,
    CONSTRAINT payment_method_billing_country_fkey FOREIGN KEY (billing_country)
        REFERENCES project.branches (country) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE CASCADE,
    CONSTRAINT card_type CHECK (card_type::text = 'visa'::text OR card_type::text = 'mastercard'::text)
)
WITH (
    OIDS = FALSE
)
TABLESPACE pg_default;

ALTER TABLE project.payment_method
    OWNER to kpink074;

------------------------------------------------

-- Table: project.payout_method

-- DROP TABLE project.payout_method;

CREATE TABLE project.payout_method
(
    username character varying(20) COLLATE pg_catalog."default" NOT NULL,
    paypal_address character varying(20) COLLATE pg_catalog."default" NOT NULL,
    CONSTRAINT payout_method_pkey PRIMARY KEY (username),
    CONSTRAINT payout_method_username_fkey FOREIGN KEY (username)
        REFERENCES project.person (username) MATCH SIMPLE
        ON UPDATE CASCADE
        ON DELETE CASCADE
)
WITH (
    OIDS = FALSE
)
TABLESPACE pg_default;

ALTER TABLE project.payout_method
    OWNER to kpink074;

------------------------------------------------

-- Table: project.person_email_address

-- DROP TABLE project.person_email_address;

CREATE TABLE project.person_email_address
(
    username character varying(20) COLLATE pg_catalog."default" NOT NULL,
    email_address character varying(20) COLLATE pg_catalog."default" NOT NULL,
    CONSTRAINT person_email_address_pkey PRIMARY KEY (username, email_address),
    CONSTRAINT person_email_address_username_fkey FOREIGN KEY (username)
        REFERENCES project.person (username) MATCH SIMPLE
        ON UPDATE CASCADE
        ON DELETE CASCADE
)
WITH (
    OIDS = FALSE
)
TABLESPACE pg_default;

ALTER TABLE project.person_email_address
    OWNER to kpink074;

------------------------------------------------


-- Table: project.person_phone_number

-- DROP TABLE project.person_phone_number;

CREATE TABLE project.person_phone_number
(
    username character varying(20) COLLATE pg_catalog."default" NOT NULL,
    phone_number character varying(20) COLLATE pg_catalog."default" NOT NULL,
    CONSTRAINT person_phone_number_pkey PRIMARY KEY (username, phone_number),
    CONSTRAINT person_phone_number_username_fkey FOREIGN KEY (username)
        REFERENCES project.person (username) MATCH SIMPLE
        ON UPDATE CASCADE
        ON DELETE CASCADE
)
WITH (
    OIDS = FALSE
)
TABLESPACE pg_default;

ALTER TABLE project.person_phone_number
    OWNER to kpink074;

------------------------------------------------


-- Table: project.user_review

-- DROP TABLE project.user_review;

CREATE TABLE project.user_review
(
    reviewerusername character varying(20) COLLATE pg_catalog."default" NOT NULL,
    revieweeusername character varying(20) COLLATE pg_catalog."default" NOT NULL,
    CONSTRAINT user_review_pkey PRIMARY KEY (reviewerusername, revieweeusername),
    CONSTRAINT user_review_revieweeusername_fkey FOREIGN KEY (revieweeusername)
        REFERENCES project.users (username) MATCH SIMPLE
        ON UPDATE CASCADE
        ON DELETE CASCADE,
    CONSTRAINT user_review_reviewerusername_fkey FOREIGN KEY (reviewerusername)
        REFERENCES project.users (username) MATCH SIMPLE
        ON UPDATE CASCADE
        ON DELETE CASCADE,
    CONSTRAINT user_review_check CHECK (revieweeusername::text <> reviewerusername::text)
)
WITH (
    OIDS = FALSE
)
TABLESPACE pg_default;

ALTER TABLE project.user_review
    OWNER to kpink074;

------------------------------------------------

-- Table: project.user_review_details

-- DROP TABLE project.user_review_details;

CREATE TABLE project.user_review_details
(
    reviewerusername character varying(20) COLLATE pg_catalog."default" NOT NULL,
    revieweeusername character varying(20) COLLATE pg_catalog."default" NOT NULL,
    "time" timestamp without time zone NOT NULL,
    review_content text COLLATE pg_catalog."default" NOT NULL,
    CONSTRAINT user_review_details_pkey PRIMARY KEY (reviewerusername, revieweeusername, "time"),
    CONSTRAINT user_review_details_reviewerusername_fkey FOREIGN KEY (revieweeusername, reviewerusername)
        REFERENCES project.user_review (revieweeusername, reviewerusername) MATCH SIMPLE
        ON UPDATE CASCADE
        ON DELETE CASCADE,
    CONSTRAINT user_review_details_check CHECK (revieweeusername::text <> reviewerusername::text)
)
WITH (
    OIDS = FALSE
)
TABLESPACE pg_default;

ALTER TABLE project.user_review_details
    OWNER to kpink074;

------------------------------------------------