CREATE TABLE shipment (
    shipment_id NUMBER PRIMARY KEY,
    order_id NUMBER,
    shipment_date DATE DEFAULT SYSDATE
);