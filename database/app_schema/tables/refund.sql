CREATE TABLE refund (
    refund_id NUMBER PRIMARY KEY,
    payment_id NUMBER,
    refund_amount NUMBER(10,2),
    created_date DATE DEFAULT SYSDATE
    );