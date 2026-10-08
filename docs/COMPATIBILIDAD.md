# Compatibilidad y diagnóstico

## Requisitos

La UI requiere `Drawing.new`, `Vector2`, `Color3`, un reloj (`os.clock` o `tick`) y un planificador (`task.spawn`/`task.wait` o `spawn`/`wait`). Necesita las primitivas Drawing Square, Line, Circle y Text con sus propiedades geométricas básicas.

Para interacción necesita coordenadas del ratón y una fuente de su estado: `ismouse1pressed`, `iskeypressed` o el servicio de entrada compatible. Las teclas requieren sondeo de teclado o eventos disponibles en el host. La presencia de un nombre no garantiza que la implementación de una versión concreta sea completa.

Consulta `ui:GetCapabilities()` sin ejecutar ninguna acción en el juego. `Touch` y `ProximityPrompt` solo indican si existen esas funciones, no las añaden ni las utilizan desde la UI.

## Alternativas incluidas

| Si falta… | Comportamiento |
|---|---|
| `task` | Usa `spawn` y `wait` globales |
| RenderStepped | Prueba Heartbeat |
| Ambos eventos de frame | Actualiza en un bucle con esperas |
| Fonts/TextBounds | Fuentes numéricas y estimación del ancho del texto |
| Corner/FontSize/Transparency | Prueba propiedades compatibles y omite las opcionales rechazadas |
| Internet o archivos de imágenes | El diseño por defecto no descarga ni lee imágenes |
| readfile/writefile/JSON | El menú funciona; las operaciones de configuración devuelven un error |
| Requisitos básicos de inicio | Devuelve nil y registra un mensaje de entorno incompatible |

La ventana se mantiene dentro del viewport y los controles se reacomodan al faltar ancho. Se simuló 640×360; por debajo de 340×280 no se asegura espacio suficiente. No es una promesa de soporte para móviles ni para cualquier escala de pantalla.

## Qué se verificó

Pruebas locales con Python/Lupa y mocks de Drawing, servicios, ratón y planificador:

- Sintaxis y creación de todos los tipos de controles documentados.
- Renderizado simulado sin excepciones.
- Herencia de estilo, anchos, columnas y ocultación de controles.
- `Set(value,true)` sin callbacks/observadores; valores repetidos sin callbacks dobles.
- Dos clics consecutivos sobre el toggle: solo uno aceptado; otro después del cooldown sí funciona.
- Slider con redondeo al paso.
- JSON: exportar/importar, restauración silenciosa, rechazo de contenido/versiones inválidas.
- Ausencia de archivos, eventos de frame, fuentes, métricas de texto y propiedades Drawing opcionales.
- Cambio de viewport a 640×360 y destrucción de todos los dibujos creados.

La vista PNG se generó a partir de los dibujos simulados y se revisó visualmente. **No se ejecutó esta versión en Matcha real.** Los mocks no validan comportamiento nativo, consumo de GPU, rendimiento en equipos distintos ni políticas de un juego.

## Antes de distribuir tu script

1. Prueba `demo_independiente.lua` en la versión de Matcha que vas a soportar.
2. Verifica abrir/cerrar, todos los controles que uses, arrastre, scrolling, cambio de resolución y recarga.
3. Añade tus callbacks de uno en uno. Pon esperas en bucles y detén tus tareas al cerrar.
4. No dependas de rutas absolutas, una imagen guardada solo en tu PC o un enlace temporal de Discord.
5. Publica la versión/SHA exacta que probaste junto a los requisitos del host.

## Síntomas

- **El menú no aparece:** busca `[Astra]` en consola y comprueba Drawing, planificador y coordenadas del ratón. Si usas carga remota, verifica que descargaste 4.0.0.
- **Un interruptor cambia dos veces:** no mezcles dos instancias. Usa cambios silenciosos al sincronizar tu estado. El cooldown de clics es 0.35 s por control.
- **`{} 0`:** no es un mensaje de esta librería; puede quedar una tarea del hub anterior. Cierra la instancia anterior y prueba la demo sola en una sesión limpia.
- **Las acciones del juego fallan pero la UI funciona:** comprueba las APIs y rutas de ese script. La librería no agrega acceso al servidor ni sustituye las APIs faltantes de Matcha.
- **No guarda archivos:** verifica readfile/writefile, JSON y la carpeta de trabajo de Matcha.
- **Se cierra el juego:** registra versión de Matcha, resolución, función activada, último mensaje y pasos para reproducir. Un `pcall` no captura fallos nativos del proceso.

## Fuentes

- [Repositorio original de la UI](https://github.com/Leox385/ima).
- [Diseño de API de tamaños de Jdui](https://github.com/jdev-studio/jdui#sizes-and-layout).
- [Drawing en la documentación de Matcha](https://matcha-latte.gitbook.io/matcha/luau-environment/drawing).

La compatibilidad se describe por funciones detectadas, no como una garantía sobre todas las versiones de Matcha.
