CREATE TABLE categories (
    category_id   NUMBER(10)    NOT NULL,
    category_name VARCHAR2(100) NOT NULL,
    description   VARCHAR2(500),
    created_on    DATE          DEFAULT SYSDATE NOT NULL,
    CONSTRAINT pk_categories PRIMARY KEY (category_id)
);
