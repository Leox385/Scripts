# API de Astra UI 4.0.0

## Instancia de librería

`UI.lua` devuelve una tabla y la registra como `_G.Kirin` y `_G.AstraUI`. La carga nueva cierra la instancia anterior de Astra. No cargues una librería por pestaña.

| Método | Resultado / efecto |
|---|---|
| `CreateWindow(options)` | Crea una ventana; `Title`, `Theme`, `Size={ancho,alto}`, `ToggleKey`, `Layout`, `Icon` opcional |
| `AddTab(options)` | Crea una ventana predeterminada si hace falta y devuelve una pestaña |
| `SetLayout("Default"/"Compact"/tabla)` | Distribución de ventanas existentes y futuras |
| `GetThemes()` / `SetTheme(nombre)` | Cosmos, Nebula, Supernova, Aurora |
| `SetTransparency(numero)` | Transparencia adicional de 0 a 0.6 |
| `Notify({Title,Content,Type,Duration})` | Notificación; duración en segundos |
| `GetCapabilities()` | Presencia de APIs; no prueba que sus implementaciones funcionen |
| `Get(flag)` / `Set(flag,value,silent)` | Valor del control identificado por Flag |
| `Watch(flag,callback)` | Observador; devuelve objeto con `Disconnect()` |
| `ExportConfig()` | Texto JSON o `nil,mensaje` |
| `ImportConfig(json,silent)` | `true,cantidad` o `false,mensaje`; silencio por defecto |
| `SaveConfig(path)` / `LoadConfig(path,silent)` | Funciones de archivos opcionales; no crean carpetas |
| `Destroy()` / `Unload()` | Retira dibujos y desconecta eventos de la librería |

Un `Flag` debe ser una cadena única en la librería. Los botones y etiquetas no tienen valor que guardar. Importar una configuración solo aplica entradas a controles ya creados con Flag y tipo coincidentes. Usa un callback o actualiza tu estado explícitamente después de una carga silenciosa.

## Ventana y pestañas

| Método | Uso |
|---|---|
| `window:Section({Title})` → `section:Tab({Title,Icon,Style,Columns})` | API original con secciones en la barra lateral |
| `window:AddTab({Title,Icon,Style,Columns})` | Atajo bajo una sección Pages |
| `window:SetLayout(value)` | Opciones de distribución de esa ventana |
| `window:SetSize(w,h)` | Tamaño solicitado, con límites del renderizador y del viewport |
| `window:SetToggleKey("h")` | Tecla de visibilidad; también acepta un código VK |
| `window:Toggle()` / `Minimize()` / `Restore()` | Estado de visibilidad |
| `window:IsPointerOver(x,y)` | Para que tu script evite hacer clic encima del menú |
| `window:SetVisualFX(false)` | Desactiva el jardín animado; otras decoraciones permanecen |
| `window:SetIcon(urlOrPath)` | Imagen explícita opcional, dependiente de red/archivos |
| `window:IsAlive()` / `Destroy()` | Ciclo de vida de la ventana |
| `tab:Select()` | Selecciona la pestaña |
| `tab:SetColumns(n)` | 1 a 4 columnas solicitadas, con reacomodo automático |
| `tab:SetStyle(table)` | Excepciones de estilo de la pestaña |
| `tab:GetLayoutBounds()` | Lista X/Y/Width/Height relativos al contenido y altura total; útil para pruebas |

Si tus callbacks crean bucles, conexiones o dibujos externos, **tu script debe detenerlos**. `Destroy()` solo administra los recursos de la UI.

## Controles

Las dos columnas de métodos son equivalentes. `Title`, `Flag`, `Default`, `Callback` y `Style` corresponden a los tipos que los admiten.

| Método original | Alias | Opciones específicas |
|---|---|---|
| `Toggle` | `AddToggle` | `Default=false`, `Type="Checkbox"` opcional |
| `Slider` | `AddSlider` | `Min`, `Max`, `Step`, `Default`, `Suffix`; redondea al paso |
| `Button` | `AddButton` | `Callback`; `Style="primary"` o `"danger"` conserva el estilo original |
| `Dropdown` | `AddDropdown` | `Options` de cadenas, `Default`, `Multi=true` opcional |
| `Keybind` | `AddKeybind` | `Default` tecla/VK, `Mode`, `OnTriggered`; admite `hold`, `toggle`, `click`, `always` |
| `Colorpicker` | `AddColorPicker` | `Default` Color3; selector de colores predefinidos |
| `Input` | `AddInput` | `Default`, `Placeholder`, `Callback` |
| `Progressbar` | `AddProgressBar` | `Default` entre 0 y 1 |
| `Paragraph` | `AddLabel` | cadena o `{Text="…"}`; vuelve a ajustar líneas según el ancho |
| `Divider` | `AddDivider` | separador decorativo |
| `Space(px)` | — | espacio vertical |
| `Section(text)` | — | encabezado dentro de una pestaña |

`Style` como tabla cambia el tamaño. En botones, el estilo antiguo de cadena y la tabla de tamaños no se combinan en una sola opción; usa `button:SetStyle({...})` después de crear un botón primary/danger.

`Description`, `SearchBarEnabled`, `AddIsland` y otras opciones de librerías ajenas **no forman parte de esta ampliación**. El colorpicker conserva una paleta, no un editor HSV completo. No asumas equivalencia total con Jdui.

## Referencias de controles

Los controles con valor ofrecen `Get()`/`GetValue()` y `Set(value,silent)`/`SetValue(value,silent)`. `silent=true` no ejecuta callback ni Watch. Asignar de nuevo el mismo valor no dispara callback. Un dropdown múltiple devuelve un mapa `{[opcion]=true}`; pásale a Set una tabla nueva en lugar de mutar directamente ese mapa.

Los controles devueltos por Toggle, Slider, Button, Dropdown, Keybind, Colorpicker, Input, Progressbar y Paragraph también tienen:

```lua
control:SetTitle("Titulo") -- alias SetText
control:SetStyle({Width=1, Height=48})
control:SetVisible(false) -- también deja de ocupar espacio
control:OnChanged(function(value) end)
control:Destroy()
```

Los botones tienen `Fire()` para invocación programática (sin cooldown). Las barras tienen `SetProgress(0.5)` y `GetProgress()`. Keybind ofrece `IsEnabled()` y `OnTriggered(callback)`.

Los callbacks se programan en tareas separadas y sus errores Lua se reportan con `[Astra] Callback`. Evita bucles sin esperas y conserva tus propios controles de cancelación. Un callback lento no debe volver a dispararse desde tu propio código sin comprobar su estado.
