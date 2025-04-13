-- source: https://chatgpt.com/share/67f1905a-73b0-8012-ae39-f105fcf0efc4
-- create database from command line:
-- sqlite3 products.db < init_db.sql

-- Remove existing tables (for a restartable setup)
DROP TABLE IF EXISTS brands;
DROP TABLE IF EXISTS products;
DROP TABLE IF EXISTS materials;
DROP TABLE IF EXISTS product_materials;

-- Create brands table
CREATE TABLE brands (
    id INTEGER PRIMARY KEY,
    name TEXT
);

-- Create products table
CREATE TABLE products (
    id INTEGER PRIMARY KEY,
    name TEXT,
    brand_id INTEGER,
    price REAL,
    FOREIGN KEY(brand_id) REFERENCES brands(id)
);

-- Create materials table
CREATE TABLE materials (
    id INTEGER PRIMARY KEY,
    name TEXT
);

-- Create join table for N:M relationship
CREATE TABLE product_materials (
    product_id INTEGER,
    material_id INTEGER,
    FOREIGN KEY(product_id) REFERENCES products(id),
    FOREIGN KEY(material_id) REFERENCES materials(id)
);

-- Add brands
INSERT INTO brands (id, name) VALUES
    (1, 'LogiTech'),
    (2, 'Hanes'),
    (3, 'KitchenPro');

-- Add products
INSERT INTO products (id, name, brand_id, price) VALUES
    (1, 'Wireless Mouse', 1, 29.99),
    (2, 'T-shirt Classic', 2, 14.95),
    (3, 'Ceramic Mug', 3, 9.50);

-- Add materials
INSERT INTO materials (id, name) VALUES
    (1, 'Plastic'),
    (2, 'Rubber'),
    (3, 'Metal'),
    (4, 'Cotton'),
    (5, 'Polyester'),
    (6, 'Ceramic');

-- Link products to materials
INSERT INTO product_materials (product_id, material_id) VALUES
    (1, 1), (1, 2), (1, 3),
    (2, 4), (2, 5),
    (3, 6), (3, 3);
