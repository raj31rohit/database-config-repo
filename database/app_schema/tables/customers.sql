CREATE TABLE customers (
    customer_id   NUMBER(10)    NOT NULL,
    first_name    VARCHAR2(100) NOT NULL,
    last_name     VARCHAR2(100) NOT NULL,
    email         VARCHAR2(200),
    created_on    DATE          DEFAULT SYSDATE NOT NULL,
    CONSTRAINT pk_customers PRIMARY KEY (customer_id)
);
