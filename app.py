from flask import Flask, request, jsonify, render_template, redirect, url_for, send_from_directory, session, flash
from models import db, Stock, Dividend, FixedStock, Purchase, CompanyInfo
from werkzeug.utils import secure_filename
import os
from sqlalchemy import desc
from flask_migrate import Migrate
from functools import wraps

app = Flask(__name__)
app.config.from_object('config')
db.init_app(app)

UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = 'cambia_esto_por_un_valor_secreto'

with app.app_context():
    db.create_all()  # Ensure tables are created if they don't exist

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('is_admin'):
            flash('Acceso solo para administradores')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('user_id'):
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/')
@login_required
def index():
    # Si es admin, va al CRUD, si no, va a la página pública
    if session.get('is_admin'):
        return redirect(url_for('stocks_page'))
    else:
        return redirect(url_for('empresas_public'))

@app.route('/stocks')
@admin_required
def stocks_page():
    return render_template('stocks.html')

@app.route('/api/stocks', methods=['POST'])
@admin_required
def add_stock():
    try:
        data = request.json
        # Verifica que los datos enviados contengan todos los campos necesarios
        if not all(key in data for key in ('name', 'date', 'value')):  # Use 'name' instead of 'company'
            return jsonify({"error": "Missing fields in request"}), 400

        # Crea un nuevo registro de Stock
        stock = Stock(name=data['name'], date=data['date'], value=data['value'], company=data['name'])  # Use 'name' for both fields
        db.session.add(stock)
        db.session.commit()
        return jsonify({"message": f"Stock '{data['name']}' added successfully"}), 201  # Ensure 'message' is returned
    except Exception as e:
        return jsonify({"error": str(e)}), 500  # Return JSON error response

@app.route('/api/stocks/<name>', methods=['GET'])
def get_stocks_by_company(name):
    try:
        stocks = Stock.query.filter_by(company=name).order_by(Stock.date).all()
        return jsonify([{"date": stock.date, "value": stock.value} for stock in stocks])  # Use 'name'
    except Exception as e:
        return jsonify({"error": str(e)}), 500  # Return JSON error response

@app.route('/companies', methods=['GET'])
def get_companies():
    try:
        companies = db.session.query(Stock.company).distinct().all()
        return jsonify([company[0] for company in companies])
    except Exception as e:
        return jsonify({"error": str(e)}), 500  # Return JSON error response

@app.route('/grafica_de_acciones')
@login_required
def grafica_de_acciones():
    return render_template('grafica_de_acciones.html')

@app.route('/api/stocks/<int:id>', methods=['PUT'])
@admin_required
def update_stock(id):
    try:
        data = request.json
        stock = Stock.query.get(id)
        if not stock:
            return jsonify({"error": "Stock not found"}), 404
        # Actualizar campos si están presentes en el request
        stock.name = data.get('name', stock.name)
        stock.date = data.get('date', stock.date)
        stock.value = data.get('value', stock.value)
        stock.company = data.get('name', stock.company)
        db.session.commit()
        return jsonify({"message": f"Stock '{stock.name}' updated successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/stocks/<int:id>', methods=['DELETE'])
@admin_required
def delete_stock(id):
    try:
        stock = Stock.query.get(id)
        if not stock:
            return jsonify({"error": "Stock not found"}), 404
        db.session.delete(stock)
        db.session.commit()
        return jsonify({"message": f"Stock '{stock.name}' deleted successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/stocks', methods=['GET'])
def get_all_stocks():
    try:
        stocks = Stock.query.order_by(Stock.company, Stock.date).all()
        return jsonify([
            {
                "id": stock.id,
                "name": stock.name,
                "date": stock.date,
                "value": stock.value,
                "company": stock.company
            }
            for stock in stocks
        ])
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/dividendos', methods=['POST'])
def add_dividendo():
    try:
        data = request.json
        if not all(key in data for key in ('company', 'year', 'value')):
            return jsonify({"error": "Missing fields in request"}), 400
        dividendo = Dividend(company=data['company'], year=data['year'], value=data['value'])
        db.session.add(dividendo)
        db.session.commit()
        return jsonify({"message": f"Dividendo de '{data['company']}' para {data['year']} agregado"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/dividendos/<int:id>', methods=['PUT'])
def update_dividendo(id):
    try:
        data = request.json
        dividendo = Dividend.query.get(id)
        if not dividendo:
            return jsonify({"error": "Dividend not found"}), 404
        dividendo.company = data.get('company', dividendo.company)
        dividendo.year = data.get('year', dividendo.year)
        dividendo.value = data.get('value', dividendo.value)
        db.session.commit()
        return jsonify({"message": "Dividendo actualizado"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/dividendos/<int:id>', methods=['DELETE'])
def delete_dividendo(id):
    try:
        dividendo = Dividend.query.get(id)
        if not dividendo:
            return jsonify({"error": "Dividend not found"}), 404
        db.session.delete(dividendo)
        db.session.commit()
        return jsonify({"message": "Dividendo eliminado"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/dividendos', methods=['GET'])
def get_all_dividendos():
    try:
        dividendos = Dividend.query.order_by(Dividend.company, Dividend.year).all()
        return jsonify([
            {
                "id": d.id,
                "company": d.company,
                "year": d.year,
                "value": d.value
            }
            for d in dividendos
        ])
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/dividendos/empresas', methods=['GET'])
def get_empresas_dividendos():
    try:
        empresas = db.session.query(Dividend.company).distinct().all()
        return jsonify([empresa[0] for empresa in empresas])
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/dividendos/empresa/<company>', methods=['GET'])
def get_dividendos_by_company(company):
    try:
        dividendos = Dividend.query.filter_by(company=company).order_by(Dividend.year).all()
        return jsonify([
            {"year": d.year, "value": d.value}
            for d in dividendos
        ])
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/ingresar_dividendos')
@login_required
def ingresar_dividendos():
    return render_template('ingresar_dividendos.html')

@app.route('/grafica_dividendos')
@login_required
def grafica_dividendos():
    return render_template('grafica_dividendos.html')

@app.route('/acciones_fijas')
@login_required
def acciones_fijas_page():
    return render_template('acciones_fijas.html')

@app.route('/api/fixed_stocks', methods=['POST'])
def add_fixed_stock():
    try:
        data = request.json
        if not all(key in data for key in ('company', 'performance', 'term')):
            return jsonify({"error": "Missing fields in request"}), 400
        fixed = FixedStock(company=data['company'], performance=data['performance'], term=data['term'])
        db.session.add(fixed)
        db.session.commit()
        return jsonify({"message": f"Acción fija '{data['company']}' agregada"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/fixed_stocks/<int:id>', methods=['PUT'])
def update_fixed_stock(id):
    try:
        data = request.json
        fixed = FixedStock.query.get(id)
        if not fixed:
            return jsonify({"error": "Fixed stock not found"}), 404
        fixed.company = data.get('company', fixed.company)
        fixed.performance = data.get('performance', fixed.performance)
        fixed.term = data.get('term', fixed.term)
        db.session.commit()
        return jsonify({"message": "Acción fija actualizada"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/fixed_stocks/<int:id>', methods=['DELETE'])
def delete_fixed_stock(id):
    try:
        fixed = FixedStock.query.get(id)
        if not fixed:
            return jsonify({"error": "Fixed stock not found"}), 404
        db.session.delete(fixed)
        db.session.commit()
        return jsonify({"message": "Acción fija eliminada"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/fixed_stocks', methods=['GET'])
def get_all_fixed_stocks():
    try:
        fixeds = FixedStock.query.order_by(FixedStock.company).all()
        return jsonify([
            {
                "id": f.id,
                "company": f.company,
                "performance": f.performance,
                "term": f.term
            }
            for f in fixeds
        ])
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/fixed_stocks/companies', methods=['GET'])
def get_fixed_stock_companies():
    try:
        companies = db.session.query(FixedStock.company).distinct().all()
        return jsonify([company[0] for company in companies])
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/calculadora_rendimiento')
@login_required
def calculadora_rendimiento():
    return render_template('calculadora_rendimiento.html')

@app.route('/comprar_accion', methods=['GET', 'POST'])
@login_required
def comprar_accion():
    if request.method == 'POST':
        stock_id = request.form.get('stock_id')
        buyer_name = request.form.get('buyer_name')
        buyer_email = request.form.get('buyer_email')
        quantity = request.form.get('quantity')
        file = request.files.get('proof')
        # Debug: imprime los datos recibidos
        # print(stock_id, buyer_name, buyer_email, quantity, file)
        if not (stock_id and buyer_name and buyer_email and quantity and file):
            return render_template('comprar_accion.html', error="Todos los campos son obligatorios.")
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        purchase = Purchase(
            stock_id=stock_id,
            buyer_name=buyer_name,
            buyer_email=buyer_email,
            quantity=quantity,
            proof_filename=filename
        )
        db.session.add(purchase)
        db.session.commit()
        return render_template('comprar_accion.html', success="¡Compra registrada! Pronto será verificada.")
    return render_template('comprar_accion.html')

@app.route('/api/stocks_list')
def stocks_list():
    stocks = Stock.query.all()
    return jsonify([
        {"id": s.id, "company": s.company, "name": s.name, "value": s.value}
        for s in stocks
    ])

@app.route('/api/stocks_latest')
def stocks_latest():
    # Obtener la acción más reciente por nombre (o empresa)
    subquery = (
        db.session.query(
            Stock.name,
            db.func.max(Stock.date).label('max_date')
        )
        .group_by(Stock.name)
        .subquery()
    )
    latest_stocks = (
        db.session.query(Stock)
        .join(subquery, (Stock.name == subquery.c.name) & (Stock.date == subquery.c.max_date))
        .all()
    )
    return jsonify([
        {"id": s.id, "company": s.company, "name": s.name, "value": s.value, "date": s.date}
        for s in latest_stocks
    ])

@app.route('/empresa_info', methods=['GET', 'POST'])
@admin_required
def empresa_info():
    if request.method == 'POST':
        name = request.form.get('name')
        description = request.form.get('description')
        file = request.files.get('logo')
        logo_filename = None
        if file and file.filename:
            logo_filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], logo_filename))
        company = CompanyInfo(name=name, description=description, logo_filename=logo_filename)
        db.session.add(company)
        db.session.commit()
        return redirect(url_for('empresa_info'))
    companies = CompanyInfo.query.all()
    return render_template('empresa_info.html', companies=companies)

@app.route('/empresa_info/delete/<int:id>', methods=['POST'])
@admin_required
def delete_empresa_info(id):
    company = CompanyInfo.query.get(id)
    if company:
        if company.logo_filename:
            logo_path = os.path.join(app.config['UPLOAD_FOLDER'], company.logo_filename)
            if os.path.exists(logo_path):
                os.remove(logo_path)
        db.session.delete(company)
        db.session.commit()
    return redirect(url_for('empresa_info'))

@app.route('/empresa_info/edit/<int:id>', methods=['GET', 'POST'])
@admin_required
def edit_empresa_info(id):
    company = CompanyInfo.query.get(id)
    if not company:
        return redirect(url_for('empresa_info'))
    if request.method == 'POST':
        company.name = request.form.get('name')
        company.description = request.form.get('description')
        file = request.files.get('logo')
        if file and file.filename:
            logo_filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], logo_filename))
            company.logo_filename = logo_filename
        db.session.commit()
        return redirect(url_for('empresa_info'))
    return render_template('empresa_info_edit.html', company=company)

@app.route('/empresas')
def empresas_public():
    companies = CompanyInfo.query.all()
    return render_template('empresas_public.html', companies=companies)

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        from models import User
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and user.password == password:  # Para producción usa hash, esto es solo ejemplo
            session['user_id'] = user.id
            session['is_admin'] = user.is_admin
            flash('Bienvenido, ' + username)
            # Redirige según el tipo de usuario
            if user.is_admin:
                return redirect(url_for('stocks_page'))
            else:
                return redirect(url_for('empresas_public'))
        else:
            flash('Usuario o contraseña incorrectos')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('Sesión cerrada')
    return redirect(url_for('login'))

migrate = Migrate(app, db)