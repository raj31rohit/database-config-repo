CREATE TABLE order_items (
    item_id     NUMBER(10)   NOT NULL,
    order_id    NUMBER(10)   NOT NULL,
    product_id  NUMBER(10)   NOT NULL,
    quantity    NUMBER(5)    NOT NULL,
    unit_price  NUMBER(12,2) NOT NULL,
    CONSTRAINT pk_order_items PRIMARY KEY (item_id)
);
