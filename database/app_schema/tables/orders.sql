CREATE TABLE orders (
    order_id NUMBER PRIMARY KEY,
    customer_id NUMBER,
    order_amount NUMBER(10,2),
    created_date DATE DEFAULT SYSDATE
);