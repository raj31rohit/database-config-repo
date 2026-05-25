CREATE TABLE payments (

    payment_id NUMBER PRIMARY KEY,

    order_id NUMBER NOT NULL,

    payment_amount NUMBER(10,2),

    payment_date DATE DEFAULT SYSDATE

);