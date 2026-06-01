CREATE TABLE orders (
    order_id    NUMBER(10)   NOT NULL,
    customer_id NUMBER(10)   NOT NULL,
    order_date  DATE         DEFAULT SYSDATE NOT NULL,
    status      VARCHAR2(20) DEFAULT 'PENDING' NOT NULL,
    CONSTRAINT pk_orders PRIMARY KEY (order_id)
);
