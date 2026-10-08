# Integrar tu código con Astra UI

## Qué copiar

1. Carga una sola instancia de `UI.lua` con el cargador del README, o incrústala como en `demo_independiente.lua`.
2. Crea tu ventana y controles como en `examples/integracion.lua`.
3. Pon la lógica de tu proyecto en los callbacks o en `myStep`, conservando las esperas y comprobaciones de estado.
4. Usa un prefijo propio para cada Flag y para tu función global de limpieza. No uses literalmente el mismo identificador en dos proyectos distintos.

La plantilla debe ejecutarse después de cargar la librería. Es un ejemplo de integración, no un sustituto de las API de tu juego.

## Valores que reciben los callbacks

| Control | Argumento principal |
|---|---|
| Toggle | `true` o `false` |
| Slider | número entre Min y Max, redondeado a Step |
| Dropdown simple | cadena de Options |
| Dropdown múltiple | tabla que relaciona cada opción seleccionada con `true` |
| Keybind | código VK numérico de la tecla seleccionada |
| Colorpicker | Color3 |
| Input | texto confirmado |
| Button | sin argumento |

Un Keybind registra una tecla: no presupongas que su callback ejecuta tu acción cada vez que pulsas esa tecla. Para acciones ligadas a teclas usa `OnTriggered` con el modo correspondiente, o gestiona el teclado explícitamente.

## Evitar los problemas más comunes

- **No llames `Set` dentro de su propio callback sin motivo.** Para reflejar un estado externo usa `control:Set(value,true)`. Con `true` no se ejecutan callback ni observadores.
- **No crees un while nuevo en cada activación.** La plantilla mantiene un worker y cambia una variable. Así una secuencia rápida activar/desactivar no acumula tareas.
- **No hagas bucles sin espera.** El cooldown de la UI no limita un bucle de tu script ni el número de llamadas al servidor.
- **Una espera no cancela una acción por sí sola.** Vuelve a comprobar tu estado después de esperar y antes de mover un personaje o enviar una petición.
- **El cierre visual no equivale a destruir.** H y el botón superior X ocultan la ventana; la función sigue activa. Usa tu botón Cerrar/cleanup para detenerla.
- **La librería no conoce tus conexiones.** Guarda las creadas por tu código y desconéctalas en cleanup. Retira también tus propios dibujos y libera teclas mantenidas si las usas.
- **Los personajes y objetos pueden desaparecer.** Obtén referencias actuales y comprueba nil antes de usarlas. Evita depender de una referencia anterior al respawn.
- **Los callbacks largos necesitan un bloqueo propio.** El cooldown de 0.35 s solo filtra clics cercanos. La plantilla muestra runningAction para no repetir una operación pendiente.
- **No supongas que una función existe en todos los hosts.** Comprueba las funciones opcionales antes de invocarlas y deja una alternativa o un mensaje claro.

## Flags y configuración

Los Flags se comparten entre ventanas de una instancia. `miProyecto.auto` y `miProyecto.speed` son mejores que dos controles llamados `enabled`. Solo añadas Flags a tipos que guardan valores: toggles, sliders, dropdowns, keybinds, colorpickers e inputs.

Después de una carga silenciosa, el control cambia pero tu variable externa no se actualiza mediante callback. Actualiza tu estado leyendo `Get()` o carga con `LoadConfig(path,false)` cuando quieras ejecutar los callbacks. No guardes secretos en configuraciones compartidas.

## Versión y alcance

Comprueba `ui.Version == "4.0.0"` al usar los métodos nuevos. Una copia anterior del archivo remoto puede cargar correctamente y carecer de `SetLayout` o `AddTab`.

Los alias se parecen a los de otras librerías, pero Astra no ejecuta sin adaptación cualquier ejemplo de Jdui u otra UI. Usa únicamente las opciones documentadas en [API.md](API.md). La lógica del juego debe ser compatible por separado con tu versión de Matcha.
