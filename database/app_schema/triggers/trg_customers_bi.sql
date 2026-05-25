CREATE OR REPLACE TRIGGER trg_orders_bi
BEFORE INSERT ON orders
FOR EACH ROW
BEGIN
    :NEW.order_id := seq_order_id.NEXTVAL;
END;
/