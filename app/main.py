# This is a simple FastAPI application that serves a static HTML site and provides API endpoints:

# source for base code https://chatgpt.com/share/67f1905a-73b0-8012-ae39-f105fcf0efc4
# extented using copilot

import sqlite3
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

app = FastAPI()

# Function to convert rows into dictionaries
def dict_factory(cursor, row):
    return {col[0]: row[idx] for idx, col in enumerate(cursor.description)}

# API endpoint to get a list of products
@app.get("/api/products")
def get_products(
    min_price: float = None,
    max_price: float = None,
    brand: list[str] = None,
    material: list[str] = None
):
    db_connection = sqlite3.connect("data/products.db")
    db_connection.row_factory = dict_factory  # Use dict_factory for query results

    # Build the base query
    query = """
        SELECT 
            p.id, 
            p.name, 
            p.price, 
            b.name AS brand 
        FROM products p
        JOIN brands b ON p.brand = b.id
        JOIN product_materials pm ON p.id = pm.product_id
        JOIN materials m ON pm.material_id = m.id
    """
    filters = []
    params = []

    # Add filters for price boundaries
    if min_price is not None:
        filters.append("p.price >= ?")
        params.append(min_price)
    if max_price is not None:
        filters.append("p.price <= ?")
        params.append(max_price)

    # Add filter for other properties (e.g. brand and material)
    if brand:
        placeholders = ", ".join(["?"] * len(brand))
        filters.append(f"b.name IN ({placeholders})")
        params.extend(brand)
    if material:
        placeholders = ", ".join(["?"] * len(material))
        filters.append(f"m.name IN ({placeholders})")
        params.extend(material)

    # Append WHERE clause if there are filters
    if filters:
        query += " WHERE " + " AND ".join(filters)

    # Add GROUP BY to ensure each product appears only once
    query += " GROUP BY p.id"

    # Execute the query
    product_rows = db_connection.execute(query, params).fetchall()

    # Add values for n:m property (e.g. materials)
    result = []
    for product in product_rows:
        product_id = product["id"]

        # Fetch materials for the product
        material_query = """
            SELECT m.name
            FROM materials m
            JOIN product_materials pm ON m.id = pm.material_id
            WHERE pm.product_id = ?
        """
        # Execute the query to fetch materials for the current product
        material_rows = db_connection.execute(material_query, (product_id,)).fetchall()

        # Add fetched materials to product
        materials = []
        for row in material_rows:
            materials.append(row["name"])
        product["materials"] = materials
        result.append(product)

    db_connection.close()
    return {"products": result}

# API endpoint to get all properties and values for filters
@app.get("/api/filters")
def get_filters():
    db_connection = sqlite3.connect("data/products.db")
    db_connection.row_factory = dict_factory  # Use dict_factory for query results

    # Fetch distinct price ranges
    price_query = """
        SELECT MIN(price) AS min_price, MAX(price) AS max_price
        FROM products
    """
    price_result = db_connection.execute(price_query).fetchone()

    # Fetch all distinct brands
    brands_query = "SELECT name FROM brands"
    brands_result = db_connection.execute(brands_query).fetchall()
    brands = [row["name"] for row in brands_result]

    # Fetch all distinct materials
    materials_query = "SELECT name FROM materials"
    materials_result = db_connection.execute(materials_query).fetchall()
    materials = [row["name"] for row in materials_result]

    # Construct the response
    filters = {
        "price": {
            "min": price_result["min_price"],
            "max": price_result["max_price"]
        },
        "brands": brands,
        "materials": materials
    }

    db_connection.close()
    return {"filters": filters}

# Serve static files like index.html, script.js, etc.
app.mount("/", StaticFiles(directory="static", html=True), name="static")

# Start server
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app)