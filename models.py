# filepath: c:\Users\wilso\Desktop\new_acciones\flask-template\models.py
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Stock(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    date = db.Column(db.String(20), nullable=False)
    value = db.Column(db.Float, nullable=False)
    company = db.Column(db.String(100), nullable=False)  # Campo para la empresa

class Dividend(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    company = db.Column(db.String(100), nullable=False)
    year = db.Column(db.String(10), nullable=False)
    value = db.Column(db.Float, nullable=False)

class FixedStock(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    company = db.Column(db.String(100), nullable=False)
    performance = db.Column(db.Float, nullable=False)  # porcentaje
    term = db.Column(db.Integer, nullable=False)       # días

class Purchase(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    stock_id = db.Column(db.Integer, db.ForeignKey('stock.id'), nullable=False)
    buyer_name = db.Column(db.String(100), nullable=False)
    buyer_email = db.Column(db.String(100), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    proof_filename = db.Column(db.String(255), nullable=False)
    status = db.Column(db.String(20), default='pendiente')
    fecha = db.Column(db.DateTime, server_default=db.func.now())

class CompanyInfo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    logo_filename = db.Column(db.String(255), nullable=True)
    description = db.Column(db.Text, nullable=False)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)