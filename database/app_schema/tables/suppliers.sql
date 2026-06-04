CREATE TABLE suppliers (
    supplier_id   NUMBER(10)    NOT NULL,
    supplier_name VARCHAR2(200) NOT NULL,
    contact_name  VARCHAR2(100),
    email         VARCHAR2(200),
    phone         VARCHAR2(20),
    created_on    DATE          DEFAULT SYSDATE NOT NULL,
    CONSTRAINT pk_suppliers PRIMARY KEY (supplier_id)
);
