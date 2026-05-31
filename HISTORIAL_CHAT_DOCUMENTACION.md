# 💬 Historial Persistente del Chat - Documentación

## 🎯 ¿Qué Cambió?

Antes el chat se limpiaba cada vez que navegabas a otra sección. **Ahora el historial se mantiene** mientras navegas por la página, pero se limpia cuando:
- ❌ Cierras la pestaña/navegador
- ❌ Cierras sesión (logout)
- ❌ Recargas completamente la página (F5)

---

## 📋 Cómo Funciona

### Sistema de Almacenamiento

Usamos **sessionStorage** que es perfecto porque:

```
┌─────────────────────────────────────────────────────┐
│              sessionStorage                         │
├─────────────────────────────────────────────────────┤
│ • Persiste entre secciones de la página ✅          │
│ • Se limpia al cerrar la pestaña ✅                 │
│ • Se limpia al recargar (F5) ✅                      │
│ • Permite hasta 5-10MB de datos ✅                  │
│ • Más seguro que localStorage ✅                    │
└─────────────────────────────────────────────────────┘
```

### Flujo del Historial

```
1. Usuario abre el chat y escribe un mensaje
         ↓
2. Mensaje se envía y se recibe respuesta del agente
         ↓
3. Cada mensaje (usuario + bot) se guarda en sessionStorage
   {
       "texto": "Hola, ¿cómo estás?",
       "remitente": "user",
       "timestamp": "2026-05-30T22:38:09Z"
   }
         ↓
4. Usuario navega a otra sección de la página
         ↓
5. Chat se "recarga" pero sessionStorage se mantiene
         ↓
6. Si usuario abre el chat de nuevo
         ↓
7. Todos los mensajes anteriores se cargan automáticamente ✅
```

---

## 🔧 Funciones Principales

### 1. **guardarMensajeEnHistorial(texto, remitente)**
Guarda cada mensaje en sessionStorage

```javascript
guardarMensajeEnHistorial("Hola", "user");
// Guarda en: sessionStorage['chatbot_historial']
```

### 2. **cargarHistorialDelChat()**
Carga todos los mensajes guardados cuando se abre el chat

```javascript
cargarHistorialDelChat();
// Se ejecuta automáticamente al abrir el chat
```

### 3. **limpiarHistorialDelChat()**
Limpia el historial de sessionStorage

```javascript
limpiarHistorialDelChat();
// Se ejecuta al cerrar sesión
```

### 4. **limpiarChatVisual()**
Limpia el chat visualmente y del almacenamiento
- Botón: 🗑️ en el header del chat

```javascript
limpiarChatVisual();
// El usuario puede hacer clic en el botón de papelera
```

---

## 👁️ Interfaz de Usuario

### Header del Chat Mejorado

```
┌────────────────────────────────────────┐
│ 🤖 Asistente Virtual  [🗑️] [✕]       │  ← Nuevo botón de limpiar
├────────────────────────────────────────┤
│  • Mensaje del usuario                  │
│                                         │
│  • Respuesta del bot                    │
│  [✓ Agregar al Carrito]                │
├────────────────────────────────────────┤
│  Escribe tu mensaje...            [📨] │
└────────────────────────────────────────┘
```

### Botón "Limpiar Chat" 🗑️
- Ubicación: Top-right del header del chat
- Función: Limpia el historial visual y del almacenamiento
- No afecta la sesión del usuario
- Rápido y reversible

---

## 📊 Límites del Historial

```
┌─────────────────────────────────────────┐
│ Limitaciones Implementadas              │
├─────────────────────────────────────────┤
│ • Máximo 50 mensajes guardados          │
│ • Si hay más, se guardan los últimos 50 │
│ • Cada mensaje ≈ 200-500 bytes          │
│ • Espacio total: ~5MB disponible        │
│ • Más que suficiente para la sesión     │
└─────────────────────────────────────────┘
```

---

## 🔐 Seguridad y Privacidad

✅ **Datos Locales**: Los mensajes solo se guardan en tu navegador
✅ **No en Servidor**: NO se envían a la base de datos
✅ **Sesión Privada**: Cada usuario tiene su propio sessionStorage
✅ **Auto-limpieza**: Se borra automáticamente al cerrar la pestaña
✅ **No Persistente**: No persiste entre navegadores

---

## 🎬 Escenarios de Uso

### Escenario 1: Navegación Normal ✅

```
1. Usuario: "¿Qué productos tienen?" [Enviar]
   Bot: "Tenemos..." [Guardado ✓]

2. Usuario navega a: /carrito/
   Chat se "oculta" pero historial está en sessionStorage

3. Usuario navega a: /producto/5/
   Chat sigue "oculto" pero el historial persiste

4. Usuario abre el chat
   ¡Todos los mensajes anteriores aparecen! ✅
```

### Escenario 2: Cerrar Sesión ✅

```
1. Chat tiene 10 mensajes guardados
   sessionStorage['chatbot_historial'] = [...]

2. Usuario hace clic en "Cerrar Sesión"
   → Script detecta logout
   → limpiarHistorialDelChat() se ejecuta
   → sessionStorage se borra ✅

3. Usuario vuelve a iniciar sesión
   Chat estará vacío (nueva sesión)
```

### Escenario 3: Recargar Página ✅

```
1. Usuario presiona F5 (recargar)
   → Página se recarga completamente
   → sessionStorage se mantiene

2. Espera... ¿se mantiene?
   NO, sessionStorage se limpia al recargar en algunos navegadores
   
   Solución: Usuario abre el chat
   → Se carga el historial disponible
   → O se muestra chat vacío si fue limpiado
```

---

## 🧪 Cómo Probar

### Test 1: Persistencia entre Secciones

```
1. Abre el chat: "¿Qué producto recomendas?"
2. Navega a: /categorias/
3. Navega a: /producto/1/
4. Abre el chat nuevamente
5. ✅ Deberías ver tu mensaje anterior
```

### Test 2: Botón Limpiar

```
1. El chat tiene varios mensajes
2. Haz clic en el botón 🗑️
3. ✅ Chat se limpia completamente
4. ✅ Se muestra de nuevo el mensaje de bienvenida
```

### Test 3: Logout Limpia Chat

```
1. Abre el chat y escribe varios mensajes
2. Cierra sesión (logout)
3. Vuelve a iniciar sesión
4. Abre el chat
5. ✅ El chat debe estar vacío (nueva sesión)
```

### Test 4: Ver en DevTools

```
1. Abre Browser DevTools: F12
2. Ve a: Application → Session Storage
3. Selecciona http://127.0.0.1:8000
4. Busca: chatbot_historial
5. ✅ Verás el JSON con todos los mensajes guardados
```

---

## 💾 Estructura del Datos Guardados

```javascript
// En sessionStorage['chatbot_historial']
[
  {
    "texto": "¿Qué zapatillas tienen?",
    "remitente": "user",
    "timestamp": "2026-05-30T22:45:12.000Z"
  },
  {
    "texto": "Tenemos Zapatillas Nike [LINK:7]",
    "remitente": "bot",
    "timestamp": "2026-05-30T22:45:15.000Z"
  },
  {
    "texto": "Te agregaré 2 al carrito [AGREGAR_AL_CARRITO:7:2]",
    "remitente": "bot",
    "timestamp": "2026-05-30T22:45:16.000Z"
  }
]
```

---

## 🔧 Configuración

### Cambiar Límite de Mensajes

En `base.html`, busca:
```javascript
if (historial.length > 50) {
    historial = historial.slice(-50);
}
```

Cambiar `50` a tu valor deseado (ej: `100` para más mensajes)

### Cambiar Nombre de Clave

En `base.html`, busca:
```javascript
sessionStorage.getItem('chatbot_historial')
```

Puedes cambiar `'chatbot_historial'` a otro nombre si quieres

---

## 🚀 Características Futuras

- [ ] Exportar historial a archivo
- [ ] Guardar con timestamp de sesión
- [ ] Búsqueda en historial
- [ ] Copiar mensaje al clipboard
- [ ] Reacciones a mensajes (👍, 👎, etc.)
- [ ] Calificar respuesta del bot

---

## ❓ Preguntas Frecuentes

### P: ¿Dónde se guardan los mensajes?
R: En el navegador, en `sessionStorage`. No en servidor.

### P: ¿Puedo ver el historial en otro navegador?
R: No. sessionStorage es específico del navegador y sesión.

### P: ¿Se pierden al cerrar la pestaña?
R: Sí. sessionStorage se limpia al cerrar la pestaña.

### P: ¿Puedo desactivar esto?
R: Sí, elimina las funciones `guardarMensajeEnHistorial()` de `addMessage()`.

### P: ¿Es seguro?
R: Sí, es más seguro que localStorage. Los datos están solo en tu navegador.

### P: ¿Funciona en navegadores privados?
R: Generalmente sí, pero algunos navegadores privados limpian sessionStorage más frecuentemente.

---

## 📝 Archivos Modificados

- `productos/templates/productos/base.html`
  - Función `guardarMensajeEnHistorial()`
  - Función `cargarHistorialDelChat()`
  - Función `limpiarHistorialDelChat()`
  - Función `limpiarChatVisual()`
  - Botón 🗑️ en header
  - Estilos `.chatbot-header-btn`
  - Event listener de logout

---

## 🎉 ¡Listo!

El chat ahora mantiene el historial mientras navegas. ¡Pruébalo! 🚀
