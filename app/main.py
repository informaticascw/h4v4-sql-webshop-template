# source https://chatgpt.com/share/67f1905a-73b0-8012-ae39-f105fcf0efc4

import sqlite3
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

app = FastAPI()

# Serve static files like index.html, script.js, etc.
app.mount("/", StaticFiles(directory="static", html=True), name="static")

# Serve API
@app.get("/api/products")
def get_products():
    conn = sqlite3.connect("products.db")

    product_query = conn.execute("SELECT * FROM products")
    product_rows = product_query.fetchall()
    column_names = [desc[0] for desc in product_query.description]

    result = []
    for row in product_rows:
        product_data = {}
        for i in range(len(column_names)):
            product_data[column_names[i]] = row[i]

        product_id = product_data["id"]

        material_query = conn.execute("""
            SELECT m.name
            FROM materials m
            JOIN product_materials pm ON m.id = pm.material_id
            WHERE pm.product_id = ?
        """, (product_id,))
        material_rows = material_query.fetchall()

        materials = []
        for material_row in material_rows:
            name = material_row[0]
            materials.append(name)

        product_data["materials"] = materials
        result.append(product_data)

    conn.close()
    return {"products": result}

# start server
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app)  # app is nog niet gedefinieerd hier!