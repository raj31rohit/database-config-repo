CREATE TABLE invoices (
    invoice_id NUMBER PRIMARY KEY,
    order_id NUMBER,
    invoice_amount NUMBER(10,2),
    created_date DATE DEFAULT SYSDATE
);