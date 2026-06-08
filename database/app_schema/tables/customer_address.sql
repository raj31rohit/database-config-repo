CREATE TABLE customer_address (
    address_id    NUMBER          NOT NULL,
    customer_id   NUMBER          NOT NULL,
    address_line1 VARCHAR2(255)   NOT NULL,
    address_line2 VARCHAR2(255),
    city          VARCHAR2(100)   NOT NULL,
    state         VARCHAR2(100),
    postal_code   VARCHAR2(20),
    country_code  VARCHAR2(3)     NOT NULL,
    address_type  VARCHAR2(20)    DEFAULT 'SHIPPING' NOT NULL,
    is_default    VARCHAR2(1)     DEFAULT 'N' NOT NULL,
    created_at    DATE            DEFAULT SYSDATE NOT NULL,
    CONSTRAINT pk_customer_address  PRIMARY KEY (address_id),
    CONSTRAINT fk_caddr_customer    FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
);
/
