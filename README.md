# Astra UI para Matcha — 4.0.0

Librería de interfaces basada en el diseño Astra/Kirin de **Leox385/ima**. Conserva sus temas, iconos dibujados, pestañas, animaciones y controles. Incorpora tamaños heredados, modo compacto, filas con varias columnas y documentación para integrarla en otros scripts.

Inspiración de uso: [Sizes and layout de Jdui](https://github.com/jdev-studio/jdui#sizes-and-layout). Esta implementación extiende el renderizador original de Astra; no incorpora el código de Jdui ni pretende ser una sustitución completa de su API.

## Archivos

- `UI.lua` en el paquete: librería independiente. En el repositorio el archivo conserva el nombre `UI` para mantener el enlace existente.
- `examples/demo.lua`: ejemplo de controles que utiliza una instancia ya cargada.
- `demo_independiente.lua`: librería y ejemplo juntos, para compartir sin archivos adicionales ni descarga de GitHub.
- `docs/API.md`: referencia de métodos y opciones.
- `docs/COMPATIBILIDAD.md`: requisitos, alternativas, pruebas y resolución de problemas.
- `docs/INTEGRACION.md` y `examples/integracion.lua`: cómo conectar código propio, evitar tareas duplicadas y cerrar correctamente.
- `ESTADO_DE_REVISION.md`: evidencia disponible y verificaciones/publicación pendientes.
- `tests/test_ui.py`: pruebas para desarrolladores con Python y Lupa; no se necesitan para usar la UI.
- `vista-simulada.png`: vista producida a partir de objetos Drawing simulados, no captura del juego.

## Primera prueba

Ejecuta **solo `demo_independiente.lua`** en Matcha, con el juego abierto. No requiere una ruta del PC del autor ni descargar imágenes. Usa **H** para mostrar/ocultar la ventana y el botón **Cerrar UI** para destruirla.

La librería presenta una interfaz; no incluye autofarm, remotos ni lógica de un juego particular. Cada desarrollador proporciona sus callbacks. Ejecutar una UI no convierte en compatibles las funciones que falten en la VM.

## Cargar un archivo local

Coloca `UI.lua` en la carpeta que Matcha expone mediante `readfile`. No es necesariamente la carpeta del script. Si tu versión no admite archivos o `loadstring`, usa el ejemplo independiente.

```lua
local previous = _G.Kirin
local ok, ui = pcall(function()
    local source = readfile("UI.lua")
    local chunk, err = loadstring(source)
    if type(chunk) ~= "function" then return nil, err end
    return chunk()
end)
if type(ui) ~= "table" and _G.Kirin ~= previous then ui = _G.Kirin end
if not ok or type(ui) ~= "table" or not ui._alive or ui.Version ~= "4.0.0" then
    warn("No se pudo cargar Astra UI 4.0.0; revisa el archivo y la consola")
    return
end
```

Para descarga remota, sustituye `readfile("UI.lua")` por `game:HttpGet(URL)` dentro del mismo `pcall`. **Hasta publicar esta versión, el enlace del repositorio puede seguir entregando la librería anterior.** Para distribuir una versión reproducible usa una URL `raw.githubusercontent.com/Leox385/ima/<COMMIT>/UI` con el SHA real del commit publicado. No añadas rutas personales de Windows a tu script.

## Crear una interfaz

```lua
-- ui es la instancia devuelta por la carga anterior.
ui:SetLayout("Compact")
local window = ui:CreateWindow({
    Title = "Mi interfaz", Theme = "Cosmos", Size = {790, 570}, ToggleKey = "h"
})
local tab = window:AddTab({Title = "General", Columns = 2})
local enabled = tab:AddToggle({
    Title = "Activado", Flag = "main.enabled", Default = false,
    Callback = function(value) print("Estado:", value) end
})
tab:AddButton({Title = "Ejecutar", Callback = function() print("Accion") end})
tab:Select()
```

También se mantiene la sintaxis original:

```lua
local section = window:Section({Title = "Funciones"})
local page = section:Tab({Title = "Jugador"})
page:Toggle({Title = "Activado", Callback = function(value) end})
```

## Tamaños y distribución

```lua
ui:SetLayout("Compact")               -- global: Height=36, TextSize=13, Gap=4
window:SetLayout({Gap=8, Corner=7})    -- sustituye la configuración de esa ventana
tab:SetStyle({Height=44, TextSize=14}) -- sustituye las excepciones de esta pestaña
enabled:SetStyle({Width=0.5})         -- sustituye las excepciones de este control
tab:SetColumns(2)                    -- entre 1 y 4; se reacomoda si falta espacio
```

Cada opción se busca en este orden: **control → pestaña → ventana → valor original**. `ui:SetLayout` establece el valor inicial de futuras ventanas y actualiza las existentes. `SetStyle({})` elimina las excepciones del nivel correspondiente; `SetLayout("Default")` recupera la distribución original en ese nivel.

`Width=0.5` solicita media fila; `Width=1` una fila completa. Una tarjeta mide al menos 200 px, salvo cuando toda la zona disponible es menor. Si no caben las columnas, se colocan en filas sucesivas. Etiquetas, divisores y encabezados ocupan toda la fila. La navegación sigue siendo por desplazamiento vertical; no se añaden las páginas ni las islas de Jdui.

| Opción de Style/Layout | Intervalo | Uso |
|---|---|---|
| `Width` | 0.1–1 | Fracción de la fila; por defecto depende de Columns |
| `Height` | 24–240 | Altura solicitada; cada tipo conserva un mínimo funcional |
| `TextSize` | 10–22 | Tamaño del título de una tarjeta |
| `Gap` | 0–24 | Separación entre tarjetas, configurada en pestaña/ventana |
| `Corner` | 0–20 | Radio de la tarjeta si Drawing lo admite |
| `Border` | 0–4 | Grosor del borde; cero lo oculta |
| `Cooldown` | 0.1–2 | Segundos entre clics del mismo botón/toggle; defecto 0.35 |

Los sliders, dropdowns, inputs y otros controles con varias líneas mantienen su altura mínima para no solaparse. El tamaño del texto afecta a los títulos, no a todos los números y decoraciones.

## Cambiar un valor desde tu código

```lua
enabled:Set(true)        -- cambia el valor y llama al callback una vez
enabled:Set(true)        -- ya estaba en true: no vuelve a llamar
enabled:Set(false, true) -- cambio silencioso, sin callback ni Watch
enabled:SetText("Listo"):SetStyle({Width=1})
```

Esto evita ciclos entre tu estado interno y los interruptores. El cooldown se aplica a los clics del usuario, no a `Set`, ni al arrastre del slider.

## Configuración opcional

Solo se exportan controles con `Flag` único. No se guarda automáticamente.

```lua
local ok, err = ui:SaveConfig("astra-settings.json")
if not ok then warn(err) end
local loaded, details = ui:LoadConfig("astra-settings.json") -- silencioso por defecto
-- Usa LoadConfig(path, false) si deseas ejecutar callbacks al restaurar.
```

Requiere `writefile`/`readfile` y JSONEncode/JSONDecode de HttpService. Su ausencia devuelve un resultado negativo y la UI sigue funcionando. La configuración es JSON, nunca código Lua ejecutable. Las carpetas deben existir previamente.

## Compartir y verificar

Distribuye la librería y tu script, o incrusta la librería en una función como en el ejemplo independiente. Prueba cargar, usar controles, cambiar resolución, cerrar y volver a cargar en cada versión de Matcha que anuncies como compatible.

**Validación disponible:** pruebas locales con servicios y Drawing simulados, y revisión visual de la vista simulada. **No validado:** ejecución real de esta versión en Matcha ni una matriz de PCs/GPUs. No se garantiza ausencia absoluta de errores o crasheos nativos.

Consulta [compatibilidad](docs/COMPATIBILIDAD.md) antes de anunciar soporte para una versión concreta.
