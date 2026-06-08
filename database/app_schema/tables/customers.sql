CREATE TABLE customers (
    customer_id   NUMBER          NOT NULL,
    first_name    VARCHAR2(100)   NOT NULL,
    last_name     VARCHAR2(100)   NOT NULL,
    email         VARCHAR2(255)   NOT NULL,
    phone         VARCHAR2(20),
    status        VARCHAR2(20)    DEFAULT 'ACTIVE' NOT NULL,
    created_at    DATE            DEFAULT SYSDATE NOT NULL,
    updated_at    DATE,
    CONSTRAINT pk_customers       PRIMARY KEY (customer_id),
    CONSTRAINT uq_customers_email UNIQUE (email)
);
/
