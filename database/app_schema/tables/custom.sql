CREATE TABLE customer_address_test (
    address_id NUMBER PRIMARY KEY,
    customer_id NUMBER NOT NULL,
    city VARCHAR2(100),
    state VARCHAR2(100),
    country VARCHAR2(100),
    created_date DATE DEFAULT SYSDATE
);