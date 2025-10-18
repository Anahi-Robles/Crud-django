# CRUD de Productos con Django

Una aplicación web completa de CRUD (Create, Read, Update, Delete) para gestión de productos, desarrollada con Django puro.

## Características

- ✅ **Crear productos** con nombre, descripción, precio y stock
- ✅ **Listar productos** con paginación y diseño responsivo
- ✅ **Ver detalles** de cada producto
- ✅ **Editar productos** existentes
- ✅ **Eliminar productos** (eliminación lógica)
- ✅ **Panel de administración** de Django
- ✅ **Interfaz moderna** con Bootstrap 5
- ✅ **Validaciones** de formularios
- ✅ **Mensajes de confirmación** para las acciones
- ✅ **Datos de ejemplo** incluidos

## Tecnologías Utilizadas

- **Django 4.2.7** - Framework web de Python
- **SQLite** - Base de datos (incluida por defecto)
- **Bootstrap 5** - Framework CSS para diseño responsivo
- **Font Awesome** - Iconos
- **HTML5/CSS3** - Estructura y estilos

## Instalación y Configuración

### 1. Clonar el repositorio
```bash
git clone https://github.com/tu-usuario/crud-django-productos.git
cd crud-django-productos
```

### 2. Crear entorno virtual (recomendado)
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate
```

### 3. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 2. Ejecutar migraciones
```bash
python manage.py makemigrations
python manage.py migrate
```

### 3. Crear superusuario (opcional)
```bash
python manage.py createsuperuser
```

### 4. Cargar datos de ejemplo
```bash
python manage.py crear_datos_ejemplo
```

### 5. Ejecutar el servidor
```bash
python manage.py runserver
```

## Uso de la Aplicación

### Acceso a la aplicación
- **Página principal**: http://127.0.0.1:8000/
- **Panel de administración**: http://127.0.0.1:8000/admin/

### Funcionalidades principales

#### 1. Lista de Productos
- Visualiza todos los productos activos
- Paginación automática (10 productos por página)
- Acciones rápidas: Ver, Editar, Eliminar
- Información resumida: nombre, descripción, precio, stock

#### 2. Crear Producto
- Formulario con validaciones
- Campos requeridos: nombre, descripción, precio, stock
- Validación de precio positivo
- Validación de stock no negativo

#### 3. Ver Detalles
- Información completa del producto
- Fechas de creación y actualización
- Estado del stock con indicadores visuales
- Acciones disponibles: Editar, Eliminar, Volver

#### 4. Editar Producto
- Formulario pre-rellenado con datos actuales
- Mismas validaciones que la creación
- Información de fechas de creación y actualización

#### 5. Eliminar Producto
- Confirmación antes de eliminar
- Eliminación lógica (marca como inactivo)
- Los datos se conservan en la base de datos

## Estructura del Proyecto

```
crud_project/
├── crud_project/           # Configuración del proyecto
│   ├── settings.py        # Configuraciones
│   ├── urls.py           # URLs principales
│   └── wsgi.py           # WSGI configuration
├── productos/             # Aplicación de productos
│   ├── migrations/       # Migraciones de base de datos
│   ├── templates/        # Plantillas HTML
│   │   └── productos/
│   │       ├── base.html
│   │       ├── lista.html
│   │       ├── detalle.html
│   │       ├── crear.html
│   │       ├── editar.html
│   │       └── eliminar.html
│   ├── management/       # Comandos personalizados
│   │   └── commands/
│   │       └── crear_datos_ejemplo.py
│   ├── admin.py         # Configuración del admin
│   ├── forms.py         # Formularios
│   ├── models.py        # Modelos de datos
│   ├── urls.py          # URLs de la app
│   └── views.py         # Vistas
├── manage.py            # Comando de Django
├── requirements.txt     # Dependencias
└── README.md           # Este archivo
```

## Modelo de Datos

### Producto
- **nombre**: CharField (200 caracteres máximo)
- **descripcion**: TextField
- **precio**: DecimalField (10 dígitos, 2 decimales)
- **stock**: IntegerField
- **fecha_creacion**: DateTimeField (auto)
- **fecha_actualizacion**: DateTimeField (auto)
- **activo**: BooleanField (default: True)

## Comandos Útiles

### Crear datos de ejemplo
```bash
python manage.py crear_datos_ejemplo
```

### Acceder al shell de Django
```bash
python manage.py shell
```

### Crear nuevas migraciones
```bash
python manage.py makemigrations productos
```

### Ver SQL de las migraciones
```bash
python manage.py sqlmigrate productos 0001
```

## Personalización

### Cambiar el número de productos por página
Edita el archivo `productos/views.py` en la función `lista_productos`:
```python
paginator = Paginator(productos_list, 20)  # Cambiar de 10 a 20
```

### Modificar los campos del formulario
Edita el archivo `productos/forms.py` en la clase `ProductoForm`:
```python
fields = ['nombre', 'descripcion', 'precio', 'stock', 'nuevo_campo']
```

### Personalizar el admin
Edita el archivo `productos/admin.py` para modificar la vista del administrador.

## Próximas Mejoras

- [ ] Búsqueda y filtros en la lista de productos
- [ ] Categorías de productos
- [ ] Imágenes de productos
- [ ] Exportación a Excel/PDF
- [ ] API REST
- [ ] Autenticación de usuarios
- [ ] Historial de cambios

## Contribuir

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/nueva-funcionalidad`)
3. Commit tus cambios (`git commit -am 'Agrega nueva funcionalidad'`)
4. Push a la rama (`git push origin feature/nueva-funcionalidad`)
5. Crea un Pull Request

## Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo `LICENSE` para más detalles.