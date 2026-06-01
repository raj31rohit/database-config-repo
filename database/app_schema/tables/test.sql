CREATE TABLE customer_address2 (
    address_id NUMBER PRIMARY KEY,
    customer_id NUMBER NOT NULL,
    city VARCHAR2(100),
    state VARCHAR2(100),
    country VARCHAR2(100),
    created_date DATE DEFAULT SYSDATE
);
-- added a column directly (WRONG - should use changes/)

