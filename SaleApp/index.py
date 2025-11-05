#
# from flask import Flask, render_template, request, abort
# from flask_sqlalchemy import SQLAlchemy
#
# app = Flask(__name__)
#
# # Cấu hình MySQL + SQLAlchemy
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://username:password@localhost/dbname'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#
# db = SQLAlchemy(app)
#
# # --- Models ---
# class Category(db.Model):
#     __tablename__ = 'category'
#     id = db.Column(db.Integer, primary_key=True, autoincrement=True)
#     name = db.Column(db.String(100), nullable=False, unique=True)
#
#     products = db.relationship('Product', backref='category', lazy=True)
#
#     def __repr__(self):
#         return f"<Category {self.name}>"
#
# class Product(db.Model):
#     __tablename__ = 'product'
#     id = db.Column(db.Integer, primary_key=True, autoincrement=True)
#     name = db.Column(db.String(200), nullable=False)
#     price = db.Column(db.Numeric(10, 2))
#     image = db.Column(db.String(255))
#     desc = db.Column(db.Text)
#     cate_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
#
#     def __repr__(self):
#         return f"<Product {self.name} - {self.price}>"
#
# # --- Routes ---
# @app.route("/")
# def index():
#     res = request.args.get("res")  # từ khóa tìm kiếm
#     category_id = request.args.get("id")  # id danh mục từ query string
#     category_id = int(category_id) if category_id else None
#
#     # Load tất cả danh mục
#     cates = Category.query.all()
#
#     # Query sản phẩm
#     query = Product.query
#     if category_id:
#         query = query.filter_by(cate_id=category_id)
#     if res:
#         query = query.filter(Product.name.ilike(f"%{res}%"))  # ilike để không phân biệt hoa thường
#     prods = query.all()
#
#     return render_template("index.html", cates=cates, prods=prods)
#
# @app.route("/product/<int:product_id>")
# def product_detail(product_id):
#     cates = Category.query.all()
#     product = Product.query.get(product_id)
#     if product:
#         return render_template("product-details.html", product=product, cates=cates)
#     else:
#         return abort(404, description="Không tìm thấy sản phẩm!")
#
# # --- Run app ---
# if __name__ == "__main__":
#     app.run(debug=True)
#
import json
from flask import render_template, request, abort, session, redirect, url_for, flash
from math import ceil
from __init__ import app, db, Category, Product, User


# --- Routes ---
@app.route("/")
def index():
    res = request.args.get("res")
    category_id = request.args.get("id")
    page = request.args.get("page", 1, type=int)
    per_page = 3

    category_id = int(category_id) if category_id else None
    cates = Category.query.all()

    query = Product.query
    if category_id:
        query = query.filter_by(cate_id=category_id)
    if res:
        query = query.filter(Product.name.ilike(f"%{res}%"))

    total = query.count()
    prods = query.order_by(Product.id.desc()).offset((page-1)*per_page).limit(per_page).all()
    total_pages = ceil(total / per_page)

    return render_template(
        "index.html",
        cates=cates,
        prods=prods,
        page=page,
        total_pages=total_pages,
        res=res,
        category_id=category_id
    )

@app.route("/product/<int:product_id>")
def product_detail(product_id):
    cates = Category.query.all()
    product = Product.query.get(product_id)
    if product:
        return render_template("product-details.html", product=product, cates=cates)
    return abort(404, description="Không tìm thấy sản phẩm!")

@app.route("/Login", methods=["GET", "POST"])
def login():
    if request.method.__eq__("POST"):
        username = request.form.get("username")
        password = request.form.get("password")
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            session['user_id'] = user.id
            session['username'] = user.username
            flash("Đăng nhập thành công!", "success")
            return redirect(url_for("index"))
        flash("Sai username hoặc password!", "danger")
        return redirect(url_for("login"))
    return render_template("login.html")

@app.route("/Logout")
def logout():
    session.clear()
    flash("Bạn đã đăng xuất!", "success")
    return redirect(url_for("index"))

def seed_data():
    # --- Categories ---
    if Category.query.count() == 0:
        with open("data/category.json", encoding="utf-8") as f:
            categories = json.load(f)
        for c in categories:
            db.session.add(Category(id=c["Id"], name=c["Name"]))
        db.session.commit()

    # --- Products ---
    if Product.query.count() == 0:
        with open("data/product.json", encoding="utf-8") as f:
            products = json.load(f)
        for p in products:
            db.session.add(Product(
                id=p["id"],
                name=p["name"],
                price=p["price"],
                image=p["image"],
                cate_id=p["cate_id"]
            ))
        db.session.commit()

    # --- Admin User ---
    if User.query.count() == 0:
        admin = User(username="admin")
        admin.set_password("123456")
        db.session.add(admin)
        db.session.commit()

# --- Run app ---
if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        seed_data()
    app.run(debug=True)
