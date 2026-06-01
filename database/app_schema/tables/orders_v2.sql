-- cleanup old data
DROP TABLE orders;
CREATE TABLE orders_v2 (
    order_id NUMBER(10) NOT NULL
);
