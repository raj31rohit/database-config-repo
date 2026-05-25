CREATE TABLE customers (
    customer_id NUMBER PRIMARY KEY,
    customer_name VARCHAR2(100),
    created_date DATE DEFAULT SYSDATE
);

