CREATE TABLE tb1 (
    shipment_id     NUMBER(10)    NOT NULL,
    order_id        NUMBER(10)    NOT NULL,
    carrier         VARCHAR2(100) NOT NULL,
    tracking_number VARCHAR2(100),
    shipped_on      DATE,
    delivered_on    DATE,
    status          VARCHAR2(20)  DEFAULT 'PENDING' NOT NULL,
    CONSTRAINT pk_shipments PRIMARY KEY (shipment_id)
);