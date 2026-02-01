from fastapi import *
from fastapi.responses import *
from fastapi.middleware.cors import CORSMiddleware
import os,hashlib,asyncio,datetime,sys,subprocess
from typing import *

app=FastAPI()
app.add_middleware(CORSMiddleware,allow_origins=["*"],allow_credentials=True,allow_methods=["*"],allow_headers=["*"])
os.makedirs("deployed_bots",exist_ok=True);os.makedirs("bot_logs",exist_ok=True)
PW=hashlib.sha256(os.getenv("ADMIN_PASSWORD","@Xavier1").encode()).hexdigest()
sessions=set()

class Bot:
    def __init__(self,name,path,req):
        self.name=name;self.path=path;self.req=req;self.proc=None;self.logs=[];self.start=datetime.datetime.now();self.status="init";self.socks=[]
    async def install(self):
        self.log("📦 Installing...");p=await asyncio.create_subprocess_exec(sys.executable,'-m','pip','install','-r',self.req,stdout=-1,stderr=-1);await p.communicate();self.log("✅ Installed" if p.returncode==0 else "❌ Failed");return p.returncode==0
    async def run(self):
        if not await self.install():self.status="error";return False
        self.log(f"🚀 Starting...");self.proc=await asyncio.create_subprocess_exec(sys.executable,self.path,stdout=-1,stderr=-1);self.status="running";self.log(f"✅ PID:{self.proc.pid}");asyncio.create_task(self.monitor());return True
    async def monitor(self):
        while self.proc and self.proc.returncode is None:
            line=await self.proc.stdout.readline()
            if line:self.log(f"📤 {line.decode().strip()}")
    async def stop(self):
        if self.proc:self.log("⏹️ Stopping...");self.proc.terminate();await asyncio.sleep(1);self.proc.kill();self.status="stopped";self.log("✅ Stopped")
    def log(self,msg):
        t=datetime.datetime.now().strftime('%H:%M:%S');e=f"[{t}] {msg}";self.logs.append(e)
        if len(self.logs)>200:self.logs=self.logs[-200:]
        asyncio.create_task(self.send(e))
    async def send(self,msg):
        for s in self.socks[:]:
            try:await s.send_json({"type":"log","msg":msg,"status":self.status})
            except:self.socks.remove(s)
    def stat(self):
        up=str(datetime.datetime.now()-self.start).split('.')[0];alive=self.proc and self.proc.returncode is None
        return {"name":self.name,"status":self.status,"up":up,"pid":self.proc.pid if self.proc else None,"alive":alive,"logs":len(self.logs)}

bots={}

@app.get("/",response_class=HTMLResponse)
async def root():return LOGIN
@app.post("/login")
async def login(r:Request,password:str=Form(...)):
    if hashlib.sha256(password.encode()).hexdigest()==PW:s=hashlib.sha256(f"{r.client.host}{datetime.datetime.now()}".encode()).hexdigest();sessions.add(s);res=RedirectResponse("/d",303);res.set_cookie("s",s);return res
    return HTMLResponse(LOGIN.replace("{{e}}","❌ Wrong password"))
@app.get("/d",response_class=HTMLResponse)
async def dash(r:Request):
    if r.cookies.get("s") not in sessions:return RedirectResponse("/",303)
    cards=""
    for n,b in bots.items():
        st=b.stat();c="#10B981"if st["alive"]else"#EF4444";em="🟢"if st["alive"]else"🔴";lg="<br>".join(b.logs[-5:])or"No logs"
        cards+=f'<div class="bc" data-bot="{n}"><h3>🤖 {n} <span style="background:{c}20;color:{c};padding:4px 8px;border-radius:12px;font-size:10px">{em} {st["status"].upper()}</span></h3><div style="font-size:11px;color:#94A3B8;margin:8px 0">⏱️ {st["up"]} | 📊 {st["logs"]}</div><div class="con" id="c-{n}">{lg}</div><div style="display:flex;gap:6px;margin-top:12px"><form method="post" action="/stop" style="display:inline"><input type="hidden" name="n" value="{n}"><button class="b bs">⏹️</button></form><form method="post" action="/restart" style="display:inline"><input type="hidden" name="n" value="{n}"><button class="b br">🔄</button></form><form method="post" action="/del" style="display:inline" onsubmit="return confirm(\'Delete?\')"><input type="hidden" name="n" value="{n}"><button class="b bd">🗑️</button></form></div></div>'
    if not cards:cards='<div style="text-align:center;padding:60px;color:#94A3B8"><div style="font-size:48px;margin-bottom:16px">🤖</div><h3>No Bots</h3><p>Deploy your first bot!</p></div>'
    return HTMLResponse(DASH.replace("{{c}}",cards))
@app.post("/up")
async def up(r:Request,bot_file:UploadFile=File(...),requirements_file:UploadFile=File(...)):
    if r.cookies.get("s") not in sessions:return RedirectResponse("/",303)
    n=bot_file.filename.replace(".py","");p=f"deployed_bots/{bot_file.filename}";q=f"deployed_bots/{n}_req.txt"
    with open(p,"wb")as f:f.write(await bot_file.read())
    with open(q,"wb")as f:f.write(await requirements_file.read())
    b=Bot(n,p,q)
    if await b.run():bots[n]=b
    return RedirectResponse("/d",303)
@app.post("/stop")
async def stop(r:Request,n:str=Form(...)):
    if r.cookies.get("s")in sessions and n in bots:await bots[n].stop()
    return RedirectResponse("/d",303)
@app.post("/restart")
async def restart(r:Request,n:str=Form(...)):
    if r.cookies.get("s")in sessions and n in bots:await bots[n].stop();await asyncio.sleep(1);await bots[n].run()
    return RedirectResponse("/d",303)
@app.post("/del")
async def delete(r:Request,n:str=Form(...)):
    if r.cookies.get("s")in sessions and n in bots:await bots[n].stop();del bots[n]
    return RedirectResponse("/d",303)
@app.websocket("/ws/{n}")
async def ws(websocket:WebSocket,n:str):
    await websocket.accept()
    if n not in bots:await websocket.close();return
    bots[n].socks.append(websocket)
    try:await websocket.send_json({"type":"init","logs":bots[n].logs[-20:]});
    except:pass
    try:
        while True:await websocket.receive_text()
    except:pass
    finally:
        if websocket in bots[n].socks:bots[n].socks.remove(websocket)
@app.get("/manifest.json")
async def manifest():return {"name":"Pavani Bots","short_name":"Pavani","start_url":"/","display":"standalone","background_color":"#0F172A","theme_color":"#8B5CF6","icons":[{"src":"/icon.png","sizes":"512x512","type":"image/png"}]}
@app.get("/health")
async def health():return {"ok":1,"bots":len(bots)}

LOGIN='''<!DOCTYPE html><html><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="theme-color" content="#8B5CF6"><title>Pavani Bots</title><style>*{margin:0;padding:0;box-sizing:border-box}body{font-family:system-ui;background:#0F172A;color:#fff;min-height:100vh;display:flex;align-items:center;justify-content:center}.box{width:90%;max-width:400px;padding:40px 30px;background:#1E293B;border-radius:20px;box-shadow:0 20px 60px rgba(0,0,0,0.5)}.logo{width:70px;height:70px;margin:0 auto 20px;background:linear-gradient(135deg,#8B5CF6,#EC4899);border-radius:16px;display:flex;align-items:center;justify-content:center;font-size:36px}h1{text-align:center;font-size:28px;background:linear-gradient(135deg,#8B5CF6,#EC4899);-webkit-background-clip:text;-webkit-text-fill-color:transparent;margin-bottom:8px}.tag{text-align:center;color:#94A3B8;font-size:13px;margin-bottom:30px}input{width:100%;padding:14px;margin-bottom:14px;background:#0F172A;border:2px solid transparent;border-radius:10px;color:#fff;font-size:15px}input:focus{outline:none;border-color:#8B5CF6}button{width:100%;padding:14px;background:linear-gradient(135deg,#8B5CF6,#7C3AED);border:none;border-radius:10px;color:#fff;font-size:15px;font-weight:700;cursor:pointer}.e{color:#F87171;font-size:13px;margin-top:12px;text-align:center}</style></head><body><div class="box"><div class="logo">🤖</div><h1>PAVANI<br>BOT CREATOR</h1><p class="tag">Deploy · Manage · Automate</p><form action="/login" method="post"><input type="password" name="password" placeholder="Password" required autofocus><button>🔐 LOGIN</button></form><p class="e">{{e}}</p></div></body></html>'''

DASH='''<!DOCTYPE html><html><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="theme-color" content="#8B5CF6"><title>Dashboard</title><style>*{margin:0;padding:0;box-sizing:border-box}body{font-family:system-ui;background:#0F172A;color:#fff;padding-bottom:60px}.hd{background:#1E293B;padding:16px;position:sticky;top:0;z-index:100;display:flex;justify-content:space-between;align-items:center;border-bottom:1px solid rgba(139,92,246,0.2)}.lg{display:flex;align-items:center;gap:10px}.li{width:36px;height:36px;background:linear-gradient(135deg,#8B5CF6,#EC4899);border-radius:8px;display:flex;align-items:center;justify-content:center;font-size:18px}.lt{font-size:15px;font-weight:800;background:linear-gradient(135deg,#8B5CF6,#EC4899);-webkit-background-clip:text;-webkit-text-fill-color:transparent}.out{padding:8px 16px;background:rgba(239,68,68,0.15);border:1px solid #EF4444;border-radius:8px;color:#EF4444;text-decoration:none;font-size:13px}.ct{max-width:1100px;margin:0 auto;padding:20px 14px}.up{background:#1E293B;border-radius:16px;padding:24px;margin-bottom:24px;border:1px solid rgba(139,92,246,0.2)}h2{font-size:20px;margin-bottom:6px}.ds{color:#94A3B8;font-size:13px;margin-bottom:18px}.fl{display:block;color:#CBD5E1;font-size:12px;font-weight:600;margin:14px 0 6px;text-transform:uppercase}.fi{width:100%;padding:16px;background:#0F172A;border:2px dashed rgba(139,92,246,0.4);border-radius:10px;cursor:pointer;text-align:center;color:#94A3B8;margin-bottom:12px}.fi:hover{border-color:#8B5CF6}.fi.hf{border-style:solid;border-color:#10B981;background:rgba(16,185,129,0.1);color:#10B981}input[type="file"]{display:none}.db{width:100%;padding:16px;background:linear-gradient(135deg,#8B5CF6,#EC4899);border:none;border-radius:10px;color:#fff;font-size:15px;font-weight:700;cursor:pointer;margin-top:8px}.db:disabled{opacity:0.5}.ad{background:#1E293B;border:1px solid rgba(139,92,246,0.2);border-radius:10px;padding:14px;margin-top:14px;text-align:center}.at{color:#06B6D4;font-weight:700;font-size:22px;margin:10px 0}.as{padding:10px 20px;background:#10B981;border:none;border-radius:8px;color:#fff;font-weight:700;cursor:pointer;margin-top:8px}.gr{display:grid;gap:16px;grid-template-columns:repeat(auto-fill,minmax(280px,1fr))}.bc{background:#1E293B;border-radius:14px;padding:20px;border:1px solid rgba(139,92,246,0.2)}.bc h3{font-size:16px;margin-bottom:10px}.con{background:#0F172A;padding:12px;border-radius:8px;font-family:monospace;font-size:10px;line-height:1.5;color:#10B981;max-height:140px;overflow-y:auto;margin:12px 0;border:1px solid rgba(16,185,129,0.2)}.con::-webkit-scrollbar{width:4px}.con::-webkit-scrollbar-thumb{background:#8B5CF6;border-radius:2px}.b{padding:8px 14px;border:none;border-radius:8px;font-size:12px;font-weight:600;cursor:pointer;flex:1}.bs{background:rgba(239,68,68,0.15);color:#EF4444;border:1px solid #EF4444}.br{background:rgba(245,158,11,0.15);color:#F59E0B;border:1px solid #F59E0B}.bd{background:rgba(239,68,68,0.15);color:#EF4444;border:1px solid #EF4444;flex:0}@media(max-width:768px){.gr{grid-template-columns:1fr}}</style></head><body><div class="hd"><div class="lg"><div class="li">🤖</div><span class="lt">PAVANI</span></div><a href="/" class="out">🚪 Logout</a></div><div class="ct"><div class="up"><h2>🚀 Deploy Bot</h2><p class="ds">Upload files - Watch 30s ad</p><form id="f" action="/up" method="post" enctype="multipart/form-data"><label class="fl">🐍 Bot File</label><label for="bf" class="fi" id="bfl">📁 Select bot.py</label><input type="file" id="bf" name="bot_file" accept=".py" required><label class="fl">📦 Requirements</label><label for="rf" class="fi" id="rfl">📁 Select requirements.txt</label><input type="file" id="rf" name="requirements_file" accept=".txt" required><button type="button" id="db" class="db" disabled>🎬 Watch Ad & Deploy</button></form><div id="ad" class="ad" style="display:none"><div style="color:#94A3B8;margin-bottom:6px">📺 Ad</div><div style="padding:30px;background:#0F172A;border-radius:8px;margin:10px 0"><div style="font-size:16px">🎯 Pavani Bot Creator</div><div style="font-size:12px;color:#94A3B8">Deploy unlimited bots</div></div><div class="at" id="at">30</div><button id="sk" class="as" style="display:none">✅ Skip</button></div></div><div class="gr">{{c}}</div></div><script>const bf=document.getElementById('bf'),rf=document.getElementById('rf'),bfl=document.getElementById('bfl'),rfl=document.getElementById('rfl'),db=document.getElementById('db'),f=document.getElementById('f'),ad=document.getElementById('ad'),at=document.getElementById('at'),sk=document.getElementById('sk');bf.onchange=e=>{if(e.target.files.length){bfl.classList.add('hf');bfl.innerHTML=`✅ ${e.target.files[0].name}`;check()}};rf.onchange=e=>{if(e.target.files.length){rfl.classList.add('hf');rfl.innerHTML=`✅ ${e.target.files[0].name}`;check()}};function check(){if(bf.files.length&&rf.files.length)db.disabled=false}let w=false;db.onclick=e=>{e.preventDefault();if(w){f.submit();return}ad.style.display='block';db.disabled=true;let t=30;const i=setInterval(()=>{t--;at.textContent=t;if(t<=0){clearInterval(i);sk.style.display='block';w=true}},1000)};sk.onclick=()=>f.submit();document.querySelectorAll('.bc').forEach(c=>{const n=c.getAttribute('data-bot');if(n){const p=location.protocol==='https:'?'wss:':'ws:',ws=new WebSocket(`${p}//${location.host}/ws/${n}`);ws.onmessage=e=>{const d=JSON.parse(e.data),con=document.getElementById('c-'+n);if(d.type==='init')con.innerHTML=d.logs.join('<br>');else if(d.type==='log'){con.innerHTML+='<br>'+d.msg;con.scrollTop=con.scrollHeight}};ws.onclose=()=>setTimeout(()=>{},5000)}})</script></body></html>'''

if __name__=="__main__":
    import uvicorn
    uvicorn.run(app,host="0.0.0.0",port=int(os.getenv("PORT",8000)))
