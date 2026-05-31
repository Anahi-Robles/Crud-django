# 🛒 Agente de IA con Carrito de Compras

## 📋 Descripción

Ahora tu agente de IA (TechBot) tiene la capacidad de **agregar productos al carrito de compras** cuando el usuario lo solicita, todo de manera fluida e integrada.

## 🎯 Características Nuevas

### ✨ Comandos Soportados

El usuario puede solicitar al agente que agregue productos de varias formas:

```
- "Agrega zapatillas a mi carrito"
- "Guarda 2 laptops en el carrito"
- "Compra 5 iPhones"
- "Añade este producto al carrito"
- "Quiero 3 tablets"
```

### 🔄 Flujo de Funcionamiento

```
┌─────────────────────────────────────────────────────────────┐
│  1. Usuario: "Agrega 2 zapatillas a mi carrito"             │
└─────────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────────┐
│  2. Agente (Azure OpenAI):                                  │
│     - Identifica producto "zapatillas"                      │
│     - Extrae cantidad: 2                                    │
│     - Genera: "Te agregaré 2 Zapatillas Nike al carrito"   │
│               [AGREGAR_AL_CARRITO:7:2]                      │
└─────────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────────┐
│  3. Frontend procesa:                                       │
│     - Reemplaza [AGREGAR_AL_CARRITO:7:2] con botón        │
│     - Muestra: "✓ Agregar al Carrito" (clickeable)         │
└─────────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────────┐
│  4. Usuario hace clic en el botón                          │
└─────────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────────┐
│  5. Backend valida y agrega:                               │
│     - Verifica stock disponible                             │
│     - Verifica cantidad positiva                            │
│     - Crea/Actualiza CarritoItem                            │
│     - Retorna confirmación JSON                             │
└─────────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────────┐
│  6. Frontend actualiza:                                     │
│     - Badge del carrito (contador)                          │
│     - Mensaje de confirmación                               │
│     - Botón cambia a "✓ Agregado al carrito"               │
└─────────────────────────────────────────────────────────────┘
```

## 🛠️ Componentes Implementados

### Backend

#### 1. **Nuevo Endpoint API**
- **URL**: `/carrito/agregar-agente/` (POST)
- **Método**: Requiere autenticación
- **Datos**: JSON con `producto_id` y `cantidad`

```python
{
    "producto_id": 7,
    "cantidad": 2
}
```

**Respuesta exitosa**:
```json
{
    "success": true,
    "message": "✓ 2 x Zapatillas Nike agregado(s) al carrito",
    "total_items": 5,
    "total_precio": 1250.50,
    "producto_nombre": "Zapatillas Nike",
    "cantidad": 2
}
```

**Respuesta con error**:
```json
{
    "success": false,
    "message": "Solo hay 3 unidades disponibles de Zapatillas Nike"
}
```

#### 2. **System Prompt Mejorado**
El agente ahora entiende y genera comandos en este formato:
```
[AGREGAR_AL_CARRITO:ID_PRODUCTO:CANTIDAD]
```

Ejemplo:
- `[AGREGAR_AL_CARRITO:7:2]` → Agregar 2 unidades del producto ID 7

#### 3. **Validaciones**
- ✓ Stock disponible
- ✓ Cantidad positiva > 0
- ✓ Producto activo
- ✓ Usuario autenticado
- ✓ Carrito existente (o creado)

### Frontend

#### 1. **Procesamiento de Patrones**
El frontend busca y reemplaza automáticamente:
```
[AGREGAR_AL_CARRITO:ID:CANTIDAD]
↓
<button class="btn-agregar-carrito-agente" data-producto-id="ID" data-cantidad="CANTIDAD">
    ✓ Agregar al Carrito
</button>
```

#### 2. **Manejadores de Eventos**
- `attachAddToCartListeners()` - Conecta eventos a botones
- `agregarAlCarritoDesdeAgente()` - Ejecuta la acción AJAX
- `updateCartCount()` - Actualiza contador visual

#### 3. **Estados del Botón**
- 🟢 **Normal**: `✓ Agregar al Carrito` (verde)
- 🔵 **Cargando**: `⏳ Agregando...` (deshabilitado)
- 🟢 **Éxito**: `✓ Agregado al carrito` (verde oscuro)
- 🔴 **Error**: `✗ Error: mensaje` (rojo)

## 📝 Ejemplo de Uso

### Diálogo Usuario-Agente:

```
Usuario: "Hola, quiero agregar 2 iPhones 15 Pro a mi carrito"

Agente: "¡Por supuesto! Te agregaré 2 iPhone 15 Pro [LINK:42] 
         al carrito en este momento. 
         [AGREGAR_AL_CARRITO:42:2]"

[Frontend muestra botón clickeable]

Usuario: [Hace clic en botón]

Sistema: "✓ 2 x iPhone 15 Pro agregado(s) al carrito
          Total items: 3
          Total: $2,998.00"
```

## 🔐 Seguridad

- Autenticación requerida (`@login_required`)
- CSRF token para POST requests
- Validación de stock en tiempo real
- Verificación de usuario propietario del carrito

## 🚀 Optimizaciones

1. **Validación de Stock**: El agente verifica automáticamente disponibilidad
2. **Actualización en Tiempo Real**: Badge del carrito se actualiza al instante
3. **Feedback Visual**: Estados claros del botón (cargando, éxito, error)
4. **Manejo de Errores**: Mensajes claros si hay problemas

## 📊 Base de Datos

El flujo utiliza estos modelos:
- **Carrito**: `Usuario OneToOne` con carrito
- **CarritoItem**: Relación M2M entre Carrito y Producto
- **Producto**: Información de stock y disponibilidad

## 🔧 Configuración Requerida

Asegúrate de que en tu `.env` tengas:
```
AZURE_OPENAI_ENDPOINT=your_endpoint
AZURE_OPENAI_KEY=your_key
AZURE_OPENAI_DEPLOYMENT_NAME=gpt-4o-mini
```

## 📝 Archivos Modificados

- `productos/views.py` - Lógica del agente y endpoints
- `productos/urls.py` - Rutas nuevas
- `productos/templates/productos/base.html` - Frontend y JavaScript

## 🎓 Para Desarrolladores

Si quieres extender esta funcionalidad:

### Agregar Nuevas Acciones del Agente

1. Define un nuevo patrón: `[NUEVA_ACCION:DATOS]`
2. Actualiza el system prompt del agente
3. Crea un endpoint para procesar la acción
4. Agregá JavaScript para manejar el patrón

### Ejemplo: Agregar a Lista de Deseos

```python
# En system prompt
"Si el usuario quiere guardar en favoritos: [AGREGAR_A_FAVORITOS:ID]"

# En views.py
@login_required
def agregar_a_favoritos_agente(request):
    # Lógica...

# En JavaScript (base.html)
respuestaBot = respuestaBot.replace(/\[AGREGAR_A_FAVORITOS:(\d+)\]/g, 
    function(match, id) {
        return `<button class="btn btn-sm btn-warning" 
                onclick="agregarAFavoritos(${id})">❤️ Guardar</button>`;
    }
);
```

## ✅ Checklist de Uso

- [ ] Servidor Django corriendo
- [ ] Usuario autenticado
- [ ] Agente disponible en interfaz
- [ ] Probar: "Agrega [nombre de producto] a mi carrito"
- [ ] Verificar botón aparece y funciona
- [ ] Confirmar que se agregó al carrito
- [ ] Visitar `/carrito/` para verificar items

## 🆘 Troubleshooting

### El botón no aparece
- Verifica que el agente genere el patrón `[AGREGAR_AL_CARRITO:ID:CANTIDAD]`
- Revisa la consola del navegador (F12) para errores JavaScript

### Error al agregar al carrito
- Verifica stock disponible del producto
- Comprueba que estés autenticado
- Revisa `/carrito/agregar-agente/` en la consola del navegador

### Contador del carrito no se actualiza
- Recarga la página (F5)
- Verifica que haya un `.cart-badge` en la navbar

---

**¡Listo!** Tu agente de IA ahora es totalmente funcional para gestionar el carrito. 🎉
