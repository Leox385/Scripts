-- Usar DESPUES de publicar UI 4.0.0 en main de Leox385/ima.
local URL = "https://raw.githubusercontent.com/Leox385/ima/refs/heads/main/UI"
local previous = _G.Kirin
local ok, ui = pcall(function()
    local source = game:HttpGet(URL)
    if type(source) ~= "string" or #source == 0 then return nil end
    local chunk = loadstring(source)
    if type(chunk) ~= "function" then return nil end
    return chunk()
end)
if type(ui) ~= "table" and _G.Kirin ~= previous then ui = _G.Kirin end
if not ok or type(ui) ~= "table" or not ui._alive or ui.Version ~= "4.0.0" then
    local output = warn or print
    if type(output) == "function" then
        pcall(output, "[Astra] No se pudo cargar UI 4.0.0. Comprueba internet, Matcha y el archivo publicado.")
    end
    return
end
ui:SetLayout("Compact")
local window = ui:CreateWindow({Title="Mi proyecto",ToggleKey="h"})
local tab = window:AddTab({Title="General"})
tab:AddToggle({Title="Activar",Default=false,Callback=function(on)
    -- Tu codigo aqui. Consulta examples/integracion.lua para tareas continuas.
    print("Activado:", on)
end})
tab:Select()
