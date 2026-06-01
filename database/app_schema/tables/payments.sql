CREATE TABLE payments (
    payment_id  NUMBER(10)    NOT NULL,
    order_id    NUMBER(10)    NOT NULL,
    amount      NUMBER(12,2)  NOT NULL,
    paid_on     DATE          DEFAULT SYSDATE,
    CONSTRAINT pk_payments PRIMARY KEY (payment_id)
);
