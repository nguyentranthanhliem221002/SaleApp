# import json
#
# def load_categories():
#     with open("data/category.json", encoding="UTF-8") as c:
#         return json.load(c)
#
# def load_products(res=None, category_id=None):
#     with open("data/product.json", encoding="UTF-8") as p:
#         products = json.load(p)
#
#     # Lọc theo tên sản phẩm (nếu có)
#     if res:
#         res_lower = res.lower()
#         products = [p for p in products if res_lower in p["name"].lower()]
#
#     # Lọc theo danh mục (nếu có)
#     if category_id:
#         products = [p for p in products if p["cate_id"] == category_id]
#
#     return products
#
# if __name__ == "__main__":
#     print(load_products(res="iphone", category_id=2))
from flask import Flask, render_template, request
from math import ceil
import json

app = Flask(__name__)

# Hàm load dữ liệu
def load_categories():
    with open("data/category.json", encoding="UTF-8") as c:
        return json.load(c)

def load_products(res=None, category_id=None):
    with open("data/product.json", encoding="UTF-8") as p:
        products = json.load(p)

    # Lọc theo từ khóa search
    if res:
        res_lower = res.lower()
        products = [p for p in products if res_lower in p["name"].lower()]

    # Lọc theo danh mục
    if category_id:
        products = [p for p in products if p["cate_id"] == category_id]

    return products

def paginate_products(products, page=1, per_page=2):
    total = len(products)
    total_pages = ceil(total / per_page)
    start = (page - 1) * per_page
    end = start + per_page
    return products[start:end], total_pages

@app.route("/")
def index():
    # Lấy query params
    page = int(request.args.get("page", 1))
    res = request.args.get("res", None)
    category_id = request.args.get("id", None)

    # Lọc sản phẩm
    prods = load_products(res=res, category_id=category_id)
    prods_paginated, total_pages = paginate_products(prods, page=page, per_page=2)

    return render_template(
        "index.html",
        prods=prods_paginated,
        page=page,
        total_pages=total_pages,
        category_id=category_id,
        res=res
    )

if __name__ == "__main__":
    app.run(debug=True)
