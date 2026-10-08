import sys,json
from pathlib import Path
from lupa import LuaRuntime
root=Path(__file__).resolve().parents[1]
source=root/'UI.lua' if (root/'UI.lua').exists() else root/'UI'
code=source.read_text(encoding='utf-8')
lua=LuaRuntime(unpack_returned_tuples=True)
lua.execute('assert(load(...))',code)
harness='''
now=0; frames={}; jobs={}; drawings={}; logs={}; mouse={X=0,Y=0}; down=false
os.clock=function() return now end
warn=function(s) logs[#logs+1]=tostring(s) end
print=warn
math.clamp=function(x,a,b) return math.max(a,math.min(b,x)) end
Vector2={new=function(x,y) return {X=x,Y=y} end}
Color3={new=function(r,g,b) return {R=r,G=g,B=b} end}
Color3.fromRGB=function(r,g,b) return Color3.new(r/255,g/255,b/255) end
Drawing={Fonts={},new=function(kind)
  local d={kind=kind,Visible=false,Transparency=1,Text=""}
  d.Remove=function(self) self.removed=true; self.Visible=false end
  setmetatable(d,{__index=function(self,k)
    if k=="TextBounds" then return Vector2.new(#self.Text*(self.FontSize or self.Size or 13)*0.54,self.FontSize or self.Size or 13) end
  end})
  drawings[#drawings+1]=d; return d
end}
function signal()
 return {Connect=function(_,fn) local c={active=true,fn=fn}; function c:Disconnect() self.active=false end; frames[#frames+1]=c; return c end}
end
task={spawn=function(fn) local co=coroutine.create(fn); jobs[#jobs+1]=co; return co end,
 wait=function() coroutine.yield() end}
iskeypressed=function() return false end
ismouse1pressed=function() return down end
local services={RunService={RenderStepped=signal()},Players={LocalPlayer={GetMouse=function() return mouse end}},UserInputService={}}
workspace={CurrentCamera={ViewportSize=Vector2.new(1280,720)}}
game={GetService=function(_,name) return services[name] end,HttpGet=function() error("offline") end}
function step(n)
 for i=1,n or 1 do
  now=now+1/60
  for _,c in ipairs(frames) do if c.active then c.fn(1/60) end end
  for _,co in ipairs(jobs) do if coroutine.status(co)~="dead" then local ok,err=coroutine.resume(co); assert(ok,err) end end
 end
end
function click(x,y) mouse.X=x;mouse.Y=y;down=true;step(1);down=false;step(1) end
'''
lua.execute(harness)
ui=lua.execute(code); lua.globals().ui=ui
lua.execute('''
ui:SetLayout("Compact")
w=ui:CreateWindow({Title="ASTRA / MATCHA",Size={790,570}})
w:SetVisualFX(false)
tab=w:AddTab({Title="Controls",Columns=2})
calls=0; watched=0
t=tab:AddToggle({Title="Enabled",Flag="enabled",Callback=function() calls=calls+1 end})
ui:Watch("enabled",function() watched=watched+1 end)
t2=tab:AddToggle({Title="Second",Style={Height=48}})
slider=tab:AddSlider({Title="Speed",Min=0,Max=100,Step=5,Default=20,Flag="speed"})
buttonCalls=0; b=tab:AddButton({Title="Run",Callback=function() buttonCalls=buttonCalls+1 end})
dd=tab:AddDropdown({Title="Mode",Options={"A","B"},Flag="mode"})
key=tab:AddKeybind({Title="Key",Default="h"})
cp=tab:AddColorPicker({Title="Accent"})
input=tab:AddInput({Title="Name"})
progress=tab:AddProgressBar({Title="Progress"})
label=tab:AddLabel("Status: ready")
tab:Select(); step(45)
assert(#logs==0,table.concat(logs," | "))
t:Set(true,true);step(5);assert(t:GetValue()==true and calls==0 and watched==0,"silent Set")
t:Set(true);step(5);assert(calls==0,"duplicate Set")
t:Set(false);step(5);assert(calls==1 and watched==1,"single callback")
slider:SetValue(28,true);assert(slider:GetValue()==30,"slider snapping")
local bounds=tab:GetLayoutBounds()
assert(bounds[1].Y==bounds[2].Y and bounds[2].X>bounds[1].X,"two columns")
assert(bounds[1].Height==36 and bounds[2].Height==48,"style inheritance")
t:SetStyle({Height=52});assert(tab:GetLayoutBounds()[1].Height==52)
t:SetStyle({});tab:SetStyle({Height=40});assert(tab:GetLayoutBounds()[1].Height==40)
tab:SetStyle({});tab:SetColumns(1);assert(tab:GetLayoutBounds()[2].Y>0)
tab:SetColumns(2)
t2:SetVisible(false);assert(#tab:GetLayoutBounds()==9);t2:SetVisible(true)
-- Inspect actual hit-testing and callbacks, not just a stand-alone debounce helper.
step(30)
local x=(1280-790)/2+152+16+45
local y=(720-570)/2+42+40+12+15
local old=calls
click(x,y);click(x,y);step(8)
assert(calls==old+1,"double click guard")
step(24);click(x,y);step(5);assert(calls==old+2,"cooldown expires")
assert(ui:SaveConfig("example.json")==false,"missing file API")
assert(#logs==0,table.concat(logs," | "))
''')
print('PASS: library initialization, all controls, rendering, style inheritance, columns, silent Set, callbacks, cooldown, missing filesystem')
def plain(v):
    if hasattr(v,'items'): return {k:plain(x) for k,x in v.items()}
    return v
lua.globals().py_encode=lambda x:json.dumps(plain(x))
lua.globals().py_decode=lambda x:lua.table_from(json.loads(x),recursive=True)
lua.execute('''
local getService=game.GetService
game.GetService=function(self,name)
 if name=="HttpService" then return {JSONEncode=function(_,x) return py_encode(x) end,JSONDecode=function(_,x) return py_decode(x) end} end
 return getService(self,name)
end
local data=ui:ExportConfig(); assert(type(data)=="string")
slider:Set(80,true); t:Set(true,true)
local before=calls; local good,count=ui:ImportConfig(data)
step(5);assert(good and count==3 and slider:Get()==30 and calls==before)
assert(ui:ImportConfig("not JSON")==false)
assert(ui:ImportConfig('{"Version":999,"Values":{}}')==false)
''')
print('PASS: JSON roundtrip, silent import and invalid configuration')
# Capture the Drawing output for a local simulated preview.
def val(v):
    if hasattr(v,'items'): return {str(k):val(x) for k,x in v.items() if not callable(x)}
    return v
draws=[]
for _,d in lua.globals().drawings.items():
    if d['Visible'] and not d['removed']:
        draws.append({k:val(d[k]) for k in ['kind','Position','Size','FontSize','Text','Color','From','To','Radius','Filled','Thickness','Transparency','Rounding','Corner']})
Path('work').mkdir(exist_ok=True)
Path('work/drawings.json').write_text(json.dumps(draws),encoding='utf-8')
lua.execute('ui:Destroy();step(5);for _,d in ipairs(drawings) do assert(d.removed,"leaked drawing") end')
print('PASS: Destroy removes all Drawing objects')
fallback=LuaRuntime(unpack_returned_tuples=True)
fallback.execute(harness)
fallback.execute('''
spawn=task.spawn;wait=task.wait;task=nil
local gs=game.GetService
game.GetService=function(self,name) if name=="RunService" then return {} end;return gs(self,name) end
local new=Drawing.new
Drawing.Fonts=nil
Drawing.new=function(kind)
 local d=new(kind)
 local mt=getmetatable(d)
 local old=mt.__index
 mt.__index=function(self,k) if k=="TextBounds" then return nil end;return old(self,k) end
 mt.__newindex=function(self,k,v)
  if k=="Transparency" or k=="Corner" or k=="Rounding" or k=="FontSize" then error("unsupported optional property") end
  rawset(self,k,v)
 end
 return d
end
''')
fallback.globals().ui=fallback.execute(code)
fallback.execute('''
local w=ui:CreateWindow({Title="Fallback"})
local t=w:AddTab("Test")
t:AddToggle("Toggle");t:AddSlider({Title="Slider"});t:Select()
step(45);assert(#logs==0,table.concat(logs," | "))
workspace.CurrentCamera.ViewportSize=Vector2.new(640,360)
step(30);assert(#logs==0,table.concat(logs," | "))
ui:Destroy();step(5)
for _,d in ipairs(drawings) do assert(d.removed) end
''')
print('PASS: spawn/wait fallback, missing frame events/fonts/optional Drawing properties, 640x360 resize, cleanup')
missing=LuaRuntime(unpack_returned_tuples=True)
missing.execute('logs={};warn=function(s) logs[#logs+1]=s end')
assert missing.execute(code) is None
assert len(missing.globals().logs)==1
print('PASS: missing required Drawing API returns a diagnostic without crashing')
