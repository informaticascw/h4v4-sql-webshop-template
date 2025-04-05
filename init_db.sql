-- source: https://chatgpt.com/share/67f1905a-73b0-8012-ae39-f105fcf0efc4
-- create database from command line:
-- sqlite3 products.db < init_db.sql

-- Verwijder bestaande tabellen (voor herstartbare setup)
DROP TABLE IF EXISTS product_materials;
DROP TABLE IF EXISTS materials;
DROP TABLE IF EXISTS products;

-- Maak products-tabel aan
CREATE TABLE products (
    id INTEGER PRIMARY KEY,
    name TEXT,
    brand TEXT,
    price REAL
);

-- Maak materials-tabel aan
CREATE TABLE materials (
    id INTEGER PRIMARY KEY,
    name TEXT
);

-- Maak koppeltabel voor N:M-relatie
CREATE TABLE product_materials (
    product_id INTEGER,
    material_id INTEGER,
    FOREIGN KEY(product_id) REFERENCES products(id),
    FOREIGN KEY(material_id) REFERENCES materials(id)
);

-- Voeg producten toe
INSERT INTO products (id, name, brand, price) VALUES
    (1, 'Wireless Mouse', 'LogiTech', 29.99),
    (2, 'T-shirt Classic', 'Hanes', 14.95),
    (3, 'Ceramic Mug', 'KitchenPro', 9.50);

-- Voeg materialen toe
INSERT INTO materials (id, name) VALUES
    (1, 'Plastic'),
    (2, 'Rubber'),
    (3, 'Metal'),
    (4, 'Cotton'),
    (5, 'Polyester'),
    (6, 'Ceramic');

-- Koppel producten aan materialen
INSERT INTO product_materials (product_id, material_id) VALUES
    (1, 1), (1, 2), (1, 3),
    (2, 4), (2, 5),
    (3, 6), (3, 3);
