# 🎯 Guía Rápida: Agente de IA + Carrito de Compras

## ¿Cómo Funciona?

### Antes (Solo mostrar productos):
```
Usuario: "¿Qué zapatillas tienen?"
Agente: "Tenemos Zapatillas Nike [LINK:7]"
Usuario: [Hace clic en Link] → Ver página del producto
Usuario: [Agrega manualmente al carrito]
```

### Ahora (Agregar directamente):
```
Usuario: "Agrega 2 zapatillas Nike a mi carrito"
Agente: "Te agregaré 2 Zapatillas Nike al carrito. [Botón: ✓ Agregar]"
Usuario: [Hace clic en botón]
Sistema: "✓ Agregado! Total: 2 items - $250.00"
```

---

## 📱 Interfaz del Chatbot

```
┌─────────────────────────────────────┐
│ 🤖 Asistente Virtual               │ [✕]
├─────────────────────────────────────┤
│                                     │
│ Usuario: "2 zapatillas al carrito"  │
│                                     │
│ Bot: Te agregaré 2 zapatillas...   │
│      [✓ Agregar al Carrito] ←─────┐│
│                                   ││
│ Sistema: ✓ 2 x Zapatillas Nike   ││
│          Agregado al carrito       ││
│                                     │
├─────────────────────────────────────┤
│ Escribe tu mensaje...          [📨] │
└─────────────────────────────────────┘
```

---

## 🚀 Pruebas Recomendadas

### Test 1: Agregar Cantidad Específica
```
Escribe: "Agrega 3 productos electrónicos al carrito"
Esperado: Agente sugiere y crea botón para cantidad específica
```

### Test 2: Agregar Múltiples Productos
```
Escribe: "Quiero 2 iPhones y 1 laptop en el carrito"
Esperado: Crea 2 botones con las cantidades correctas
```

### Test 3: Manejo de Errores (Stock Insuficiente)
```
Escribe: "Agrega 100 iPhones"
Esperado: Agente advierte sobre stock limitado
```

### Test 4: Feedback Visual
```
Pasos:
1. Haz clic en botón "✓ Agregar al Carrito"
2. Observa animación de carga
3. Verifica confirmación en chat
4. Revisa badge del carrito (número de items)
```

---

## 🔑 Palabras Clave que Entiende el Agente

El agente genera botones cuando detecta que el usuario quiere:

✅ `agregar` / `añadir` / `guarda` / `compra` / `mete`
✅ `carrito` / `carro` / `compra`
✅ `cantidad`: "2 zapatillas", "tres laptops", "5 productos"

Ejemplos reconocidos:
- "Agrega esta laptop al carrito"
- "Mete 2 iPhones en mi compra"  
- "Guarda 5 tablets en el carrito"
- "Quiero 3 de estos productos"

---

## 📊 Información Que Se Actualiza

Después de agregar al carrito:

| Campo | Antes | Después |
|-------|-------|---------|
| Badge Carrito | 2 | 4 |
| Total Items | 2 | 4 |
| Total Precio | $500 | $750 |
| Estado Botón | ✓ Agregar | ✓ Agregado |

---

## 🎨 Estados Visuales del Botón

```
1️⃣ NORMAL (Inicial)
   [✓ Agregar al Carrito]  ← Verde, clickeable
   
2️⃣ CARGANDO (Al hacer clic)
   [⏳ Agregando...]  ← Deshabilitado, spinner
   
3️⃣ ÉXITO (Después de agregar)
   [✓ Agregado al carrito]  ← Verde oscuro
   (Se restaura a NORMAL después de 2s)
   
4️⃣ ERROR (Si hay problema)
   [✗ Error: No hay stock]  ← Rojo
   (Vuelve a NORMAL después de 3s)
```

---

## 🔗 URLs Importantes

| Ruta | Método | Autenticación | Datos |
|------|--------|---------------|-------|
| `/carrito/` | GET | ✓ | - |
| `/carrito/agregar-agente/` | POST | ✓ | JSON |
| `/chatbot/` | POST | ✓ | Form |
| `/producto/ID/` | GET | ✓ | - |

---

## 📱 JSON Enviado al Backend

```json
{
  "producto_id": 7,
  "cantidad": 2
}
```

**Ejemplo cURL**:
```bash
curl -X POST http://localhost:8000/carrito/agregar-agente/ \
  -H "Content-Type: application/json" \
  -H "X-CSRFToken: token_aqui" \
  -d '{"producto_id": 7, "cantidad": 2}'
```

---

## ⚙️ Configuración del Agente

**System Prompt importante**:
```
[AGREGAR_AL_CARRITO:ID_PRODUCTO:CANTIDAD]
```

Cuando el usuario dice "agregar", el agente incluye:
- ID del producto (del inventario)
- Cantidad solicitada (default: 1 si no especifica)

---

## 🛠️ Personalización

### Cambiar Color del Botón
En `base.html`, busca `.btn-agregar-carrito-agente` y modifica:
```css
background-color: #tu-color;  /* Cambiar aquí */
```

### Cambiar Texto del Botón
En `base.html`, busca la línea del botón:
```javascript
// Cambiar de:
`<button class="btn btn-sm btn-success mt-1 btn-agregar-carrito-agente"...>✓ Agregar al Carrito</button>`
// A:
`<button class="btn btn-sm btn-success mt-1 btn-agregar-carrito-agente"...>🛒 Agregar</button>`
```

### Agregar Sonido de Confirmación
```javascript
// En agregarAlCarritoDesdeAgente(), agregar:
new Audio('/path/to/sound.mp3').play();
```

---

## 🐛 Si Algo No Funciona

### Checklist:
- [ ] ¿Estás logueado?
- [ ] ¿El agente aparece (botón chat abajo a la derecha)?
- [ ] ¿Django server está corriendo?
- [ ] ¿Abres Developer Tools (F12) para ver errores?
- [ ] ¿El CSRF token está en la sesión?

### Ver Errores:
1. Abre browser DevTools: `F12`
2. Pestaña "Console"
3. Ve cualquier error rojo
4. Comparte en backend: Ver logs de Django

---

## 📈 Próximas Funcionalidades

Posibles extensiones:
- [ ] Agregar a Lista de Deseos
- [ ] Comprar directamente sin ir a carrito
- [ ] Aplicar cupones desde el chat
- [ ] Rastrear pedido anterior
- [ ] Recomendaciones personalizadas

---

**¡Listo para usar!** 🎉

Abre el chatbot y prueba escribiendo:
```
"Agrega 2 [nombre de un producto] a mi carrito"
```
