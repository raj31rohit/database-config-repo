CREATE TABLE products (
    product_id    NUMBER          NOT NULL,
    product_name  VARCHAR2(255)   NOT NULL,
    description   VARCHAR2(1000),
    sku           VARCHAR2(100),
    price         NUMBER(10,2)    NOT NULL,
    stock_qty     NUMBER          DEFAULT 0 NOT NULL,
    status        VARCHAR2(20)    DEFAULT 'ACTIVE' NOT NULL,
    created_at    DATE            DEFAULT SYSDATE NOT NULL,
    updated_at    DATE,
    CONSTRAINT pk_products     PRIMARY KEY (product_id),
    CONSTRAINT uq_products_sku UNIQUE (sku)
);
/
