from flask import Flask, render_template, request
import dao

app = Flask(__name__)

@app.route("/")
def index():
    res = request.args.get("res")
    category_id = request.args.get("Id")

    # Convert Id sang int nếu có, tránh lỗi so sánh kiểu str với int
    category_id = int(category_id) if category_id else None

    cates = dao.load_categories()
    prods = dao.load_products(res=res, category_id=category_id)

    return render_template("index.html", cates=cates, prods=prods)

if __name__ == "__main__":
    app.run(debug=True)
