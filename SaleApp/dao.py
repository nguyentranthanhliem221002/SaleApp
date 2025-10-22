import json

def load_categories():
    with open("data/category.json", encoding="UTF-8") as c:
        return json.load(c)

def load_products(res=None, category_id=None):
    with open("data/product.json", encoding="UTF-8") as p:
        products = json.load(p)

    # Lọc theo tên sản phẩm (nếu có)
    if res:
        res_lower = res.lower()
        products = [p for p in products if res_lower in p["name"].lower()]

    # Lọc theo danh mục (nếu có)
    if category_id:
        products = [p for p in products if p["cate_id"] == category_id]

    return products

if __name__ == "__main__":
    print(load_products(res="iphone", category_id=2))
