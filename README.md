# Sistema de Compra y Gestión de Acciones

![Python](https://img.shields.io/badge/Python-3.8%2B-blue?logo=python)
![Flask](https://img.shields.io/badge/Flask-2.x-lightgrey?logo=flask)
![MySQL](https://img.shields.io/badge/MySQL-8.x-blue?logo=mysql)
![Bootstrap](https://img.shields.io/badge/Bootstrap-5.x-purple?logo=bootstrap)

## Descripción

Este proyecto es una plataforma web para la **gestión y compra de acciones**, orientada tanto a usuarios administradores como a clientes. Permite administrar acciones variables y fijas, dividendos, empresas, compras y usuarios, diferenciando los permisos según el tipo de usuario. Incluye carga de comprobantes, gestión de logos de empresas y visualización de gráficas.

---

## Características

- **CRUD completo** para acciones variables, acciones fijas, dividendos y empresas.
- **Gestión de usuarios** con roles (administrador y cliente).
- **Compra de acciones** con carga de comprobante.
- **Visualización de gráficas** de acciones y dividendos.
- **Carga y gestión de archivos** (comprobantes y logos).
- **Interfaz web responsiva** con Bootstrap.
- **Seguridad**: control de acceso por roles y validaciones.

---

## Tecnologías Utilizadas

- Python 3.8+
- Flask
- Flask-SQLAlchemy
- Flask-Migrate
- MySQL
- Bootstrap 5
- JavaScript

---

## Estructura del Proyecto

```
flask-template/
│
├── app.py                # Lógica principal y rutas
├── models.py             # Modelos de la base de datos
├── config.py             # Configuración de la base de datos
├── create_user.py        # Script para crear usuarios iniciales
├── templates/            # Plantillas HTML (interfaz web)
├── static/               # Archivos estáticos (CSS, JS, imágenes)
├── uploads/              # Comprobantes y logos subidos
└── docs/                 # Documentación y reportes
```

---

## Instalación y Ejecución

1. **Clona el repositorio:**
    ```sh
    git clone https://github.com/tuusuario/sistema-acciones.git
    cd sistema-acciones/flask-template
    ```

2. **Instala las dependencias:**
    ```sh
    pip install -r requirements.txt
    ```

3. **Configura la base de datos:**
    - Edita `config.py` con tus credenciales de MySQL.

4. **Inicializa la base de datos:**
    ```sh
    flask db upgrade
    ```

5. **Crea usuarios iniciales:**
    ```sh
    python create_user.py
    ```

6. **Ejecuta la aplicación:**
    ```sh
    flask run
    ```

7. Accede desde tu navegador a [http://localhost:5000](http://localhost:5000)

---

## Capturas de Pantalla

![acciones_5](https://github.com/user-attachments/assets/238725f9-6e10-437d-95f9-a48f36c60c9a)

![acciones](https://github.com/user-attachments/assets/5e6034e8-8d2f-4d96-a7d3-95cccb01fc35)

![acciones_2](https://github.com/user-attachments/assets/b7a472b3-faa6-46ca-9a52-d31d2a1209c0)


## Contribución

¿Quieres mejorar el proyecto?  
¡Forkea el repositorio, haz tus cambios y envía un Pull Request!

---

## Licencia

Este proyecto es solo para fines educativos.

---

## Autor


- [Joan Daniel Rivas Andrade](https://github.com/JoanDaniel18)

---

¿Dudas o sugerencias? ¡Abre un issue en el repositorio!
