-- CSI2132 Winter 2020 Project
-- A list of all the DDLs used

------------------------------------------------

-- Table: project.branches

-- DROP TABLE project.branches;

CREATE TABLE project.branches
(
    country character varying(20) COLLATE pg_catalog."default" NOT NULL,
    street_number numeric(5,0),
    street_name character varying(20) COLLATE pg_catalog."default",
    apt_number numeric(5,0),
    province character varying(20) COLLATE pg_catalog."default",
    postal_code character varying(20) COLLATE pg_catalog."default",
    CONSTRAINT branches_pkey PRIMARY KEY (country)
)
WITH (
    OIDS = FALSE
)
TABLESPACE pg_default;

ALTER TABLE project.branches
    OWNER to kpink074;

------------------------------------------------

-- Table: project.conversation

-- DROP TABLE project.conversation;

CREATE TABLE project.conversation
(
    senderid character varying(20) COLLATE pg_catalog."default" NOT NULL,
    receiverid character varying(20) COLLATE pg_catalog."default" NOT NULL,
    CONSTRAINT conversation_pkey PRIMARY KEY (senderid, receiverid),
    CONSTRAINT conversation_receiverid_fkey FOREIGN KEY (receiverid)
        REFERENCES project.person (id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE CASCADE,
    CONSTRAINT conversation_senderid_fkey FOREIGN KEY (senderid)
        REFERENCES project.person (id) MATCH SIMPLE
        ON UPDATE NO ACTION
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
    senderid character varying(20) COLLATE pg_catalog."default" NOT NULL,
    receiverid character varying(20) COLLATE pg_catalog."default" NOT NULL,
    "time" timestamp without time zone NOT NULL,
    message_content text COLLATE pg_catalog."default" NOT NULL,
    CONSTRAINT conversation_messages_pkey PRIMARY KEY (senderid, receiverid, "time"),
    CONSTRAINT conversation_messages_senderid_fkey FOREIGN KEY (receiverid, senderid)
        REFERENCES project.conversation (receiverid, senderid) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE CASCADE
)
WITH (
    OIDS = FALSE
)
TABLESPACE pg_default;

ALTER TABLE project.conversation_messages
    OWNER to kpink074;

------------------------------------------------

-- Table: project.employees

-- DROP TABLE project.employees;

CREATE TABLE project.employees
(
    id character varying(20) COLLATE pg_catalog."default" NOT NULL,
    title text COLLATE pg_catalog."default" NOT NULL,
    salary numeric(8,2),
    country character varying(20) COLLATE pg_catalog."default",
    managerid character varying(20) COLLATE pg_catalog."default",
    CONSTRAINT employees_pkey PRIMARY KEY (id),
    CONSTRAINT employees_country_fkey FOREIGN KEY (country)
        REFERENCES project.branches (country) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE CASCADE,
    CONSTRAINT employees_id_fkey FOREIGN KEY (id)
        REFERENCES project.person (id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE CASCADE,
    CONSTRAINT employees_managerid_fkey FOREIGN KEY (managerid)
        REFERENCES project.employees (id) MATCH SIMPLE
        ON UPDATE NO ACTION
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

-- Table: project.payment

-- DROP TABLE project.payment;

CREATE TABLE project.payment
(
    id character varying(20) COLLATE pg_catalog."default" NOT NULL,
    is_deposit boolean NOT NULL,
    amount numeric(8,2),
    status character varying(20) COLLATE pg_catalog."default",
    rentalid character varying(20) COLLATE pg_catalog."default",
    guestid character varying(20) COLLATE pg_catalog."default",
    hostid character varying(20) COLLATE pg_catalog."default",
    CONSTRAINT payment_pkey PRIMARY KEY (id),
    CONSTRAINT payment_guestid_fkey FOREIGN KEY (guestid)
        REFERENCES project.users (id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE SET NULL,
    CONSTRAINT payment_hostid_fkey FOREIGN KEY (hostid)
        REFERENCES project.users (id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE SET NULL,
    CONSTRAINT payment_rentalid_fkey FOREIGN KEY (rentalid)
        REFERENCES project.rental_agreement (id) MATCH SIMPLE
        ON UPDATE NO ACTION
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
    id character varying(20) COLLATE pg_catalog."default" NOT NULL,
    card_type character varying(20) COLLATE pg_catalog."default",
    first_name character varying(20) COLLATE pg_catalog."default",
    last_name character varying(20) COLLATE pg_catalog."default",
    card_number character varying(20) COLLATE pg_catalog."default",
    card_expiration date,
    cvv character varying(3) COLLATE pg_catalog."default",
    billing_country character varying(20) COLLATE pg_catalog."default",
    CONSTRAINT payment_method_pkey PRIMARY KEY (id),
    CONSTRAINT payment_method_id_fkey FOREIGN KEY (id)
        REFERENCES project.users (id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE CASCADE
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
    id character varying(20) COLLATE pg_catalog."default" NOT NULL,
    paypal_address character varying(20) COLLATE pg_catalog."default",
    account_type character varying(20) COLLATE pg_catalog."default",
    account_holder_name character varying(20) COLLATE pg_catalog."default",
    bank_name character varying(20) COLLATE pg_catalog."default",
    account_number character varying(20) COLLATE pg_catalog."default",
    transit_number character varying(20) COLLATE pg_catalog."default",
    insitution_number character varying(20) COLLATE pg_catalog."default",
    CONSTRAINT payout_method_pkey PRIMARY KEY (id),
    CONSTRAINT payout_method_id_fkey FOREIGN KEY (id)
        REFERENCES project.person (id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE CASCADE
)
WITH (
    OIDS = FALSE
)
TABLESPACE pg_default;

ALTER TABLE project.payout_method
    OWNER to kpink074;

------------------------------------------------

-- Table: project.person

-- DROP TABLE project.person;

CREATE TABLE project.person
(
    id character varying(20) COLLATE pg_catalog."default" NOT NULL,
    first_name character varying(20) COLLATE pg_catalog."default" NOT NULL,
    middle_name character varying(20) COLLATE pg_catalog."default",
    last_name character varying(20) COLLATE pg_catalog."default" NOT NULL,
    username character varying(20) COLLATE pg_catalog."default" NOT NULL,
    password character varying(20) COLLATE pg_catalog."default" NOT NULL,
    country character varying(20) COLLATE pg_catalog."default" NOT NULL,
    street_number numeric(5,0) NOT NULL,
    street_name character varying(20) COLLATE pg_catalog."default" NOT NULL,
    apt_number numeric(5,0),
    province character varying(20) COLLATE pg_catalog."default" NOT NULL,
    postal_code character varying(20) COLLATE pg_catalog."default" NOT NULL,
    date_of_birth date NOT NULL,
    CONSTRAINT person_pkey PRIMARY KEY (id)
)
WITH (
    OIDS = FALSE
)
TABLESPACE pg_default;

ALTER TABLE project.person
    OWNER to kpink074;

------------------------------------------------

-- Table: project.person_email_address

-- DROP TABLE project.person_email_address;

CREATE TABLE project.person_email_address
(
    id character varying(20) COLLATE pg_catalog."default" NOT NULL,
    email_address character varying(20) COLLATE pg_catalog."default" NOT NULL,
    CONSTRAINT person_email_address_pkey PRIMARY KEY (id, email_address),
    CONSTRAINT person_email_address_id_fkey FOREIGN KEY (id)
        REFERENCES project.person (id) MATCH SIMPLE
        ON UPDATE NO ACTION
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
    id character varying(20) COLLATE pg_catalog."default" NOT NULL,
    phone_number character varying(20) COLLATE pg_catalog."default" NOT NULL,
    CONSTRAINT person_phone_number_pkey PRIMARY KEY (id, phone_number),
    CONSTRAINT person_phone_number_id_fkey FOREIGN KEY (id)
        REFERENCES project.person (id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE CASCADE
)
WITH (
    OIDS = FALSE
)
TABLESPACE pg_default;

ALTER TABLE project.person_phone_number
    OWNER to kpink074;

------------------------------------------------

-- Table: project.property

-- DROP TABLE project.property;

CREATE TABLE project.property
(
    id character varying(20) COLLATE pg_catalog."default" NOT NULL,
    street_number numeric(5,0) NOT NULL,
    street_name character varying(20) COLLATE pg_catalog."default" NOT NULL,
    apt_number numeric(5,0),
    province character varying(20) COLLATE pg_catalog."default" NOT NULL,
    postal_code character varying(20) COLLATE pg_catalog."default" NOT NULL,
    rent_rate numeric(8,2),
    type character varying(20) COLLATE pg_catalog."default",
    max_guests numeric(2,0),
    number_beds numeric(2,0),
    number_baths numeric(2,0),
    accesible boolean NOT NULL,
    pets_allowed boolean NOT NULL,
    country character varying(20) COLLATE pg_catalog."default",
    hostid character varying(20) COLLATE pg_catalog."default",
    CONSTRAINT property_pkey PRIMARY KEY (id),
    CONSTRAINT property_country_fkey FOREIGN KEY (country)
        REFERENCES project.branches (country) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE CASCADE,
    CONSTRAINT property_hostid_fkey FOREIGN KEY (hostid)
        REFERENCES project.users (id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE CASCADE,
    CONSTRAINT property_rent_rate_check CHECK (rent_rate > 0::numeric),
    CONSTRAINT property_type_check CHECK (type::text = 'entire'::text OR type::text = 'private'::text OR type::text = 'shared'::text),
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

-- Table: project.property_available_dates

-- DROP TABLE project.property_available_dates;

CREATE TABLE project.property_available_dates
(
    id character varying(20) COLLATE pg_catalog."default" NOT NULL,
    available_date date NOT NULL,
    CONSTRAINT property_available_dates_pkey PRIMARY KEY (id, available_date),
    CONSTRAINT property_available_dates_id_fkey FOREIGN KEY (id)
        REFERENCES project.property (id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE CASCADE
)
WITH (
    OIDS = FALSE
)
TABLESPACE pg_default;

ALTER TABLE project.property_available_dates
    OWNER to kpink074;

------------------------------------------------

-- Table: project.property_review

-- DROP TABLE project.property_review;

CREATE TABLE project.property_review
(
    userid character varying(20) COLLATE pg_catalog."default" NOT NULL,
    propertyid character varying(20) COLLATE pg_catalog."default" NOT NULL,
    CONSTRAINT property_review_pkey PRIMARY KEY (userid, propertyid),
    CONSTRAINT property_review_propertyid_fkey FOREIGN KEY (propertyid)
        REFERENCES project.property (id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE CASCADE,
    CONSTRAINT property_review_userid_fkey FOREIGN KEY (userid)
        REFERENCES project.users (id) MATCH SIMPLE
        ON UPDATE NO ACTION
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
    userid character varying(20) COLLATE pg_catalog."default" NOT NULL,
    propertyid character varying(20) COLLATE pg_catalog."default" NOT NULL,
    "time" timestamp without time zone NOT NULL,
    communication numeric(2,1),
    value numeric(2,1),
    check_in numeric(2,1),
    accuracy numeric(2,1),
    cleanliness numeric(2,1),
    location numeric(2,1),
    review_content text COLLATE pg_catalog."default",
    CONSTRAINT property_review_details_pkey PRIMARY KEY (userid, propertyid, "time"),
    CONSTRAINT property_review_details_userid_fkey FOREIGN KEY (propertyid, userid)
        REFERENCES project.property_review (propertyid, userid) MATCH SIMPLE
        ON UPDATE NO ACTION
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
    id character varying(20) COLLATE pg_catalog."default" NOT NULL,
    start_date date NOT NULL,
    end_date date NOT NULL,
    sign_date date,
    travelling_for_work boolean NOT NULL,
    message_to_host text COLLATE pg_catalog."default" NOT NULL,
    total_price numeric(8,2),
    host_accepted boolean NOT NULL,
    propertyid character varying(20) COLLATE pg_catalog."default",
    guestid character varying(20) COLLATE pg_catalog."default",
    hostid character varying(20) COLLATE pg_catalog."default",
    CONSTRAINT rental_agreement_pkey PRIMARY KEY (id),
    CONSTRAINT rental_agreement_guestid_fkey FOREIGN KEY (guestid)
        REFERENCES project.users (id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE SET NULL,
    CONSTRAINT rental_agreement_hostid_fkey FOREIGN KEY (hostid)
        REFERENCES project.users (id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE SET NULL,
    CONSTRAINT rental_agreement_propertyid_fkey FOREIGN KEY (propertyid)
        REFERENCES project.property (id) MATCH SIMPLE
        ON UPDATE NO ACTION
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

-- Table: project.user_review

-- DROP TABLE project.user_review;

CREATE TABLE project.user_review
(
    reviewerid character varying(20) COLLATE pg_catalog."default" NOT NULL,
    revieweeid character varying(20) COLLATE pg_catalog."default" NOT NULL,
    CONSTRAINT user_review_pkey PRIMARY KEY (reviewerid, revieweeid),
    CONSTRAINT user_review_revieweeid_fkey FOREIGN KEY (revieweeid)
        REFERENCES project.users (id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE CASCADE,
    CONSTRAINT user_review_reviewerid_fkey FOREIGN KEY (reviewerid)
        REFERENCES project.users (id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE CASCADE,
    CONSTRAINT user_review_check CHECK (revieweeid::text <> reviewerid::text)
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
    reviewerid character varying(20) COLLATE pg_catalog."default" NOT NULL,
    revieweeid character varying(20) COLLATE pg_catalog."default" NOT NULL,
    "time" timestamp without time zone NOT NULL,
    review_content text COLLATE pg_catalog."default" NOT NULL,
    CONSTRAINT user_review_details_pkey PRIMARY KEY (reviewerid, revieweeid, "time"),
    CONSTRAINT user_review_details_reviewerid_fkey FOREIGN KEY (revieweeid, reviewerid)
        REFERENCES project.user_review (revieweeid, reviewerid) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE CASCADE,
    CONSTRAINT user_review_details_check CHECK (revieweeid::text <> reviewerid::text)
)
WITH (
    OIDS = FALSE
)
TABLESPACE pg_default;

ALTER TABLE project.user_review_details
    OWNER to kpink074;

------------------------------------------------

-- Table: project.users

-- DROP TABLE project.users;

CREATE TABLE project.users
(
    id character varying(20) COLLATE pg_catalog."default" NOT NULL,
    join_date date NOT NULL,
    verified boolean NOT NULL,
    about text COLLATE pg_catalog."default",
    languages text COLLATE pg_catalog."default",
    work text COLLATE pg_catalog."default",
    profile_picture bytea,
    CONSTRAINT users_pkey PRIMARY KEY (id),
    CONSTRAINT users_id_fkey FOREIGN KEY (id)
        REFERENCES project.person (id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE CASCADE
)
WITH (
    OIDS = FALSE
)
TABLESPACE pg_default;

ALTER TABLE project.users
    OWNER to kpink074;

------------------------------------------------

-- Table: project.works_at

-- DROP TABLE project.works_at;

CREATE TABLE project.works_at
(
    employeeid character varying(20) COLLATE pg_catalog."default" NOT NULL,
    propertyid character varying(20) COLLATE pg_catalog."default" NOT NULL,
    CONSTRAINT works_at_pkey PRIMARY KEY (employeeid, propertyid),
    CONSTRAINT works_at_employeeid_fkey FOREIGN KEY (employeeid)
        REFERENCES project.employees (id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE CASCADE,
    CONSTRAINT works_at_propertyid_fkey FOREIGN KEY (propertyid)
        REFERENCES project.property (id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE CASCADE
)
WITH (
    OIDS = FALSE
)
TABLESPACE pg_default;

ALTER TABLE project.works_at
    OWNER to kpink074;

------------------------------------------------

-- Table: project.admins

-- DROP TABLE project.admins;

CREATE TABLE project.admins
(
    id character varying(20) COLLATE pg_catalog."default",
    CONSTRAINT admins_id_fkey FOREIGN KEY (id)
        REFERENCES project.person (id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE CASCADE
)
WITH (
    OIDS = FALSE
)
TABLESPACE pg_default;

ALTER TABLE project.admins
    OWNER to kpink074;

------------------------------------------------
