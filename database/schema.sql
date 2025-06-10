CREATE TABLE customers (
    customer_id	TEXT PRIMARY KEY,
    customer_unique_id TEXT,
    customer_zip_code_prefix TEXT,
    customer_city TEXT,
    customer_state TEXT
);
CREATE TABLE geo_location (
    geolocation_zip_code_prefix TEXT PRIMARY KEY,
    geolocation_lat TEXT,
    geolocation_lng TEXT,
    geolocation_city TEXT,
    geolocation_state TEXT
);
CREATE TABLE order_items (
    order_id TEXT NOT NULL,
    order_item_id TEXT NOT NULL,
    product_id TEXT NOT NULL,
    seller_id TEXT NOT NULL,
    shipping_limit_date TIMESTAMP,
    price REAL,
    freight_value REAL,
    PRIMARY KEY (order_id, order_item_id)
);
CREATE TABLE order_payments (
    order_id TEXT NOT NULL,
    payment_sequential INTEGER NOT NULL,
    payment_type TEXT,
    payment_installments INTEGER,
    payment_value REAL,
    PRIMARY KEY (order_id, payment_sequential)
);
CREATE TABLE order_reviews (
    review_id TEXT PRIMARY KEY,
    order_id TEXT NOT NULL,
    review_score INTEGER,
    review_comment_title TEXT,
    review_comment_message TEXT,
    review_creation_date TIMESTAMP,
    review_answer_timestamp TIMESTAMP
);
CREATE TABLE orders (
    order_id TEXT PRIMARY KEY,
    customer_id TEXT,
    order_status TEXT,
    order_purchase_timestamp TIMESTAMP,
    order_approved_at TIMESTAMP,
    order_delivered_carrier_date TIMESTAMP,
    order_delivered_customer_date TIMESTAMP,
    order_estimated_delivery_date TIMESTAMP
);
CREATE TABLE products (
    product_id TEXT PRIMARY KEY,
    product_category_name TEXT,
    product_name_length INTEGER,
    product_description_length INTEGER,
    product_photos_qty INTEGER,
    product_weight_g INTEGER,
    product_length_cm INTEGER,
    product_height_cm INTEGER,
    product_width_cm INTEGER
);
CREATE TABLE sellers (
    seller_id TEXT PRIMARY KEY,
    seller_zip_code_prefix TEXT,
    seller_city TEXT,
    seller_state TEXT
);
CREATE TABLE product_category (
    product_category_name TEXT PRIMARY KEY,
    product_category_name_english TEXT,
    product_category_name_ptbr TEXT
)


