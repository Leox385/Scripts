# Pruebas para desarrolladores

Estas dependencias solo se necesitan para probar la libreria fuera de Matcha:

```sh
python -m pip install "lupa>=2.0,<3"
python tests/test_ui.py
```

El test detecta UI.lua (ZIP) o UI (repositorio) automaticamente.
Las pruebas usan mocks; no abren Roblox,
no se conectan al juego y no validan la implementacion nativa de Matcha.
Los objetos dibujados quedan en work/drawings.json para inspeccion.
Consulta ESTADO_DE_REVISION.md para conocer la ultima ejecucion confirmada.
