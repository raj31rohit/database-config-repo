CREATE TABLE orders (
    order_id      NUMBER          NOT NULL,
    customer_id   NUMBER          NOT NULL,
    order_date    DATE            DEFAULT SYSDATE NOT NULL,
    status        VARCHAR2(20)    DEFAULT 'PENDING' NOT NULL,
    total_amount  NUMBER(12,2)    NOT NULL,
    notes         VARCHAR2(1000),
    created_at    DATE            DEFAULT SYSDATE NOT NULL,
    updated_at    DATE,
    CONSTRAINT pk_orders PRIMARY KEY (order_id)
);
/
