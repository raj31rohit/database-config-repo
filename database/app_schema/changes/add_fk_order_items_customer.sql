ALTER TABLE order_items
ADD CONSTRAINT fk_order_items_customer
FOREIGN KEY (order_id) REFERENCES non_existent_table(order_id);
