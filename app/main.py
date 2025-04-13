# This is a simple FastAPI application that serves a static HTML site and provides API endpoints:

# source for base code https://chatgpt.com/share/67f1905a-73b0-8012-ae39-f105fcf0efc4
# extended using copilot

import sqlite3
from fastapi import FastAPI, Query
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Middleware to disable caching, handy for development
@app.middleware("http")
async def disable_cache(request, call_next):
    response = await call_next(request)
    response.headers.update({
        "Cache-Control": "no-store, no-cache, must-revalidate, max-age=0",
        "Pragma": "no-cache",
        "Expires": "0"
    })
    return response

# Function to convert rows into dictionaries
def dict_factory(cursor, row):
    return {col[0]: row[idx] for idx, col in enumerate(cursor.description)}

# API endpoint to get a list of products
@app.get("/api/products")
def get_products(
    brand: list[str] = Query(default=[]),
    material: list[str] = Query(default=[])
):
    print("DEBUG: Starting /api/products endpoint")
    print("DEBUG: Parameters - brand:", brand, ", material:", material)
    db_connection = sqlite3.connect("data/products.db")
    db_connection.row_factory = dict_factory  # Convert rows into dictionaries

    # Build the base query
    query = """
        SELECT 
            p.id, 
            p.name, 
            p.price, 
            b.name AS brand 
        FROM products p
        LEFT JOIN brands b ON p.brand_id = b.id
        LEFT JOIN product_materials pm ON p.id = pm.product_id
        LEFT JOIN materials m ON pm.material_id = m.id
    """
    filters = []
    params = []

    # Add filter for brands
    if brand:
        placeholders = ", ".join(["?"] * len(brand))
        filters.append("b.name IN (" + placeholders + ")")
        params.extend(brand)

    # Add filter for materials
    if material:
        placeholders = ", ".join(["?"] * len(material))
        filters.append("m.name IN (" + placeholders + ")")
        params.extend(material)

    # Append WHERE clause if there are filters
    if filters:
        query += " WHERE " + " AND ".join(filters)

    # Add GROUP BY to ensure each product appears only once
    query += " GROUP BY p.id"

    # Execute the query
    print("DEBUG: Query submitted:", query)
    print("DEBUG: Query parameters:", params)
    product_rows = db_connection.execute(query, params).fetchall()
    print("DEBUG: Query result (first 5 rows):", product_rows[:5])

    # Add values for n:m property (e.g., materials)
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
        print("DEBUG: Query submitted:", material_query)
        material_rows = db_connection.execute(material_query, (product_id,)).fetchall()
        print("DEBUG: Query result (first 5 rows):", material_rows[:5])

        # Add fetched materials to product
        materials = []
        for row in material_rows:
            materials.append(row["name"])
        product["material"] = materials
        result.append(product)

    db_connection.close()
    print("DEBUG: Finished /api/products endpoint") 
    return {"products": result}

# API endpoint to get all properties and values for filters
@app.get("/api/filters")
def get_filters():
    print("DEBUG: Starting /api/filters endpoint")  

    db_connection = sqlite3.connect("data/products.db")
    db_connection.row_factory = dict_factory  # Use dict_factory for query results

    # Fetch all distinct brands
    brands_query = "SELECT name FROM brands"
    print("DEBUG: Query submitted:", brands_query)  
    brands_result = db_connection.execute(brands_query).fetchall()
    print("DEBUG: Query result (first 5 rows):", brands_result[:5])  
    brands = [row["name"] for row in brands_result]

    # Fetch all distinct materials
    materials_query = "SELECT name FROM materials"
    print("DEBUG: Query submitted:", materials_query)  
    materials_result = db_connection.execute(materials_query).fetchall()
    print("DEBUG: Query result (first 5 rows):", materials_result[:5])  
    materials = [row["name"] for row in materials_result]

    # Construct the response
    filters = {
        "brand": brands,
        "material": materials
    }

    db_connection.close()
    print("DEBUG: Finished /api/filters endpoint")  
    return {"filters": filters}

# Serve static files like index.html, script.js, etc.
app.mount("/", StaticFiles(directory="static", html=True), name="static")

# Start server
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app)