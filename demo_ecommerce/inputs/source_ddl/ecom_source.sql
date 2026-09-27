
CREATE TABLE customers (
    customer_id VARCHAR(64) PRIMARY KEY,
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    email VARCHAR(100),
    address VARCHAR(200),
    region VARCHAR(50)
);

CREATE TABLE products (
    product_id VARCHAR(64) PRIMARY KEY,
    product_name VARCHAR(100),
    category VARCHAR(50),
    unit_price NUMERIC(10,2)
);

CREATE TABLE orders (
    order_id VARCHAR(64) PRIMARY KEY,
    customer_id VARCHAR(64) REFERENCES customers(customer_id),
    order_date DATE,
    total_amount NUMERIC(10,2)
);

CREATE TABLE order_items (
    order_id VARCHAR(64) REFERENCES orders(order_id),
    order_item_id VARCHAR(64),
    product_id VARCHAR(64) REFERENCES products(product_id),
    quantity INT,
    unit_price NUMERIC(10,2),
    PRIMARY KEY (order_id, order_item_id)
);
