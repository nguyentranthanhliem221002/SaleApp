from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Category(db.Model):
    __tablename__ = 'category'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False, unique=True)

    products = db.relationship('Product', backref='category', lazy=True)

    def __repr__(self):
        return f"<Category {self.name}>"

class Product(db.Model):
    __tablename__ = 'product'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(200), nullable=False)
    price = db.Column(db.Numeric(10, 2))
    image = db.Column(db.String(255))
    desc = db.Column(db.Text)
    cate_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)

    def __repr__(self):
        return f"<Product {self.name} - {self.price}>"
