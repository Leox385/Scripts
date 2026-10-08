-- Ejecutar DESPUES de cargar Astra UI 4.0.0.
-- Cambia MiProyectoAstra por un identificador unico de tu proyecto.
local ui = _G.AstraUI or _G.Kirin
if type(ui) ~= "table" or ui.Version ~= "4.0.0" or not ui._alive then
    warn("Carga Astra UI 4.0.0 primero")
    return
end
local host = task or {}
local spawnTask, waitTask = host.spawn or spawn, host.wait or wait
if type(spawnTask) ~= "function" or type(waitTask) ~= "function" then return end

if type(_G.MiProyectoAstraCleanup) == "function" then
    pcall(_G.MiProyectoAstraCleanup)
end
local alive, enabled, runningAction = true, false, false
local connections = {}
local window = ui:CreateWindow({Title="Mi proyecto",ToggleKey="h"})
local tab = window:AddTab("General")
local status = tab:AddLabel("Estado: detenido")
local toggle

local function isActive()
    return alive and enabled and window:IsAlive()
end

local function myStep()
    -- Pega aqui UN PASO de tu logica; no crees otro while ni otro worker.
    -- Comprueba que los objetos del juego existen antes de usarlos.
    -- Si tu paso necesita wait(), vuelve a comprobar isActive() despues.
    if not isActive() then return end
end

local function cleanup()
    if not alive then return end
    alive, enabled = false, false
    for _,connection in ipairs(connections) do
        pcall(function() connection:Disconnect() end)
    end
    connections = {}
    window:Destroy()
    if _G.MiProyectoAstraCleanup == cleanup then _G.MiProyectoAstraCleanup = nil end
end
_G.MiProyectoAstraCleanup = cleanup

toggle = tab:AddToggle({Title="Activar",Flag="MiProyectoAstra.enabled",Callback=function(value)
    if not alive then return end
    enabled = value
    status:SetText(value and "Estado: activo" or "Estado: detenido")
end})

tab:AddButton({Title="Accion unica",Callback=function()
    -- El cooldown evita doble clic, pero una operacion larga necesita su propio bloqueo.
    if not alive or runningAction then return end
    runningAction = true
    local ok, err = pcall(function()
        -- Tu accion aqui. Si esperas, comprueba alive antes de continuar.
    end)
    runningAction = false
    if not ok then warn("[MiProyectoAstra] "..tostring(err)) end
end})
tab:AddButton({Title="Cerrar",Style="danger",Callback=cleanup})
tab:Select()

-- Un solo worker por instancia. El toggle cambia estado; no crea nuevas tareas.
spawnTask(function()
    while alive and window:IsAlive() do
        waitTask(0.2)
        if isActive() then
            local ok, err = pcall(myStep)
            if not ok then
                enabled = false
                if alive and window:IsAlive() then
                    toggle:Set(false,true)
                    status:SetText("Error en tu logica; revisa la consola")
                end
                warn("[MiProyectoAstra] "..tostring(err))
            end
        end
    end
    cleanup()
end)
