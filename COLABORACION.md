# 👥 Guía de Colaboración - CRUD Django

## Para Integrantes del Equipo

### 🚀 Configuración inicial

1. **Clonar el repositorio:**
```bash
git clone https://github.com/Anahi-Robles/Crud-django.git
cd Crud-django
```

2. **Configurar entorno:**
```bash
python -m venv venv
venv\Scripts\activate  # Windows
pip install -r requirements.txt
python manage.py migrate
python manage.py crear_datos_ejemplo
```

### 🌿 Flujo de trabajo simple

1. **Crear tu rama personal:**
```bash
git checkout -b tu-nombre
# Ejemplo: git checkout -b juan
# Ejemplo: git checkout -b maria
```

2. **Trabajar en tu rama:**
```bash
# Hacer tus cambios...
git add .
git commit -m "Descripción de tus cambios"
```

3. **Subir tu rama cuando quieras:**
```bash
git push origin tu-nombre
```

4. **Integrar a main cuando estés listo:**
```bash
# Cambiar a main
git checkout main

# Obtener últimos cambios
git pull origin main

# Integrar tu rama
git merge tu-nombre

# Subir a main
git push origin main
```

### 📋 Reglas simples

#### **Nombres de ramas:**
- Usa tu nombre: `juan`, `maria`, `carlos`, etc.
- O tu nombre + funcionalidad: `juan-login`, `maria-estilos`

#### **Antes de subir a main:**
- [ ] Probar que tu código funciona
- [ ] Ejecutar `python manage.py runserver` para verificar

#### **¡Libertad total!**
- Puedes subir a `main` cuando quieras
- No necesitas aprobación
- Solo asegúrate de que funcione

### 🔄 Mantener tu rama actualizada

```bash
# Cambiar a main
git checkout main

# Obtener últimos cambios
git pull origin main

# Volver a tu rama
git checkout feature/tu-rama

# Integrar cambios de main
git merge main
```

### 🆘 Comandos útiles

```bash
# Ver todas las ramas
git branch -a

# Cambiar de rama
git checkout nombre-rama

# Ver estado actual
git status

# Ver historial
git log --oneline
```

## 📞 Contacto

Si tienes dudas, contacta a **Anahi Robles** (administradora del repositorio).