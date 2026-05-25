ALTER TABLE refund
ADD CONSTRAINT fk_refund_payment
FOREIGN KEY (payment_id)
REFERENCES payments(payment_invalid_column);