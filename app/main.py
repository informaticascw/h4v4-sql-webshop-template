# This is a simple FastAPI application that serves a static HTML page and provides two API endpoints:

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
    brand: list[str] = None
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
    """
    filters = []
    params = []

    # Add filters for price boundaries
    if min_price is not None:
        filters.append("price >= ?")
        params.append(min_price)
    if max_price is not None:
        filters.append("price <= ?")
        params.append(max_price)

    # Add filter for brand(s)
    if brand:
        placeholders = ", ".join(["?"] * len(brand))
        filters.append(f"brand IN ({placeholders})")
        params.extend(brand)

    # Append WHERE clause if there are filters
    if filters:
        query += " WHERE " + " AND ".join(filters)

    product_query = db_connection.execute(query, params)
    product_rows = product_query.fetchall()

    result = []
    for product in product_rows:
        product_id = product["id"]

        # Fetch materials for the product
        material_query = db_connection.execute("""
            SELECT m.name
            FROM materials m
            JOIN product_materials pm ON m.id = pm.material_id
            WHERE pm.product_id = ?
        """, (product_id,))
        material_rows = material_query.fetchall()

        # Add materials to the product
        product["materials"] = [material_row["name"] for material_row in material_rows]

        result.append(product)

    db_connection.close()
    return {"products": result}

# API endpoint to get a list of materials
@app.get("/api/materials")
def get_materials():
    db_connection = sqlite3.connect("data/products.db")
    db_connection.row_factory = dict_factory  # Use dict_factory for query results

    # Query to fetch all materials
    materials_query = db_connection.execute("SELECT id, name FROM materials")
    materials_result = materials_query.fetchall()

    db_connection.close()
    return {"materials": materials_result}

# API endpoint to get a list of brands
@app.get("/api/brands")
def get_brands():
    db_connection = sqlite3.connect("data/products.db")
    db_connection.row_factory = dict_factory  # Use dict_factory for query results

    # Query to fetch all brands from the brands table
    brands_query = "SELECT id, name FROM brands"
    brands_result = db_connection.execute(brands_query).fetchall()

    db_connection.close()
    return {"brands": brands_result}

# Serve static files like index.html, script.js, etc.
app.mount("/", StaticFiles(directory="static", html=True), name="static")

# Start server
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app)