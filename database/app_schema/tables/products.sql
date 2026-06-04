CREATE TABLE products (
    product_id    NUMBER(10)    NOT NULL,
    product_name  VARCHAR2(200) NOT NULL,
    category      VARCHAR2(100),
    unit_price    NUMBER(12,2)  NOT NULL,
    stock_qty     NUMBER(10)    DEFAULT 0 NOT NULL,
    created_on    DATE          DEFAULT SYSDATE NOT NULL,
    CONSTRAINT pk_products PRIMARY KEY (product_id)
);
