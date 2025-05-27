from models import db, User
from app import app

with app.app_context():
    # Cambia estos valores según lo que quieras
    admin = User(username='admin', password='admin123', is_admin=True)
    cliente = User(username='cliente', password='cliente123', is_admin=False)
    db.session.add(admin)
    db.session.add(cliente)
    db.session.commit()
    print("Usuarios creados: admin/admin123 y cliente/cliente123")
