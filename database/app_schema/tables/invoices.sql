CREATE TABLE invoices (
    invoice_id    NUMBER(10)     NOT NULL,
    order_id      NUMBER(10)     NOT NULL,
    invoice_date  DATE           DEFAULT SYSDATE NOT NULL,
    due_date      DATE           NOT NULL,
    total_amount  NUMBER(12,2)   NOT NULL,
    status        VARCHAR2(20)   DEFAULT 'UNPAID' NOT NULL,
    CONSTRAINT pk_invoices PRIMARY KEY (invoice_id)
);
