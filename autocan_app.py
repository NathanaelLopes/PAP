import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import sqlite3, random, time
from pathlib import Path
from datetime import datetime

DB = Path(__file__).with_name("autocan.db")
BG, PANEL, ALT = "#0b1020", "#121a2b", "#172238"
TEXT, MUTED, CYAN = "#edf3ff", "#93a4bf", "#43d9ff"
GREEN, YELLOW, RED, PURPLE = "#42d392", "#ffc857", "#ff5d73", "#a99bff"

class AutoCAN:
    def __init__(self, root):
        self.root = root
        root.title("AutoCAN | Monitorização Automóvel")
        root.geometry("1150x760")
        root.minsize(950, 650)
        root.configure(bg=BG)
        self.faults = set()
        self.history = []
        self.last_alerts = set()
        self.session_start = time.time()
        self.session_id = None
        self.active = True
        self.values = {"rpm": 1500, "temp": 84.0, "speed": 45.0, "battery": 12.6}
        self._db()
        self._style()
        self._ui()
        self.new_session()
        self.tick()
        root.protocol("WM_DELETE_WINDOW", self.close)

    def _db(self):
        with sqlite3.connect(DB) as c:
            c.execute("CREATE TABLE IF NOT EXISTS sessions(id INTEGER PRIMARY KEY, start TEXT, end TEXT, status TEXT)")
            c.execute("CREATE TABLE IF NOT EXISTS samples(id INTEGER PRIMARY KEY, session_id INTEGER, ts TEXT, rpm INTEGER, temp REAL, speed REAL, battery REAL, status TEXT)")
            c.execute("CREATE TABLE IF NOT EXISTS alerts(id INTEGER PRIMARY KEY, session_id INTEGER, ts TEXT, level TEXT, message TEXT)")

    def _style(self):
        s = ttk.Style()
        s.theme_use("clam")
        s.configure("Treeview", background=PANEL, foreground=TEXT, fieldbackground=PANEL, rowheight=25)
        s.configure("Treeview.Heading", background=ALT, foreground=TEXT)

    def _ui(self):
        head = tk.Frame(self.root, bg=BG); head.pack(fill="x", padx=20, pady=(16, 10))
        tk.Label(head, text="AUTOCAN", bg=BG, fg=CYAN, font=("Segoe UI", 24, "bold")).pack(anchor="w")
        tk.Label(head, text="SISTEMA INTELIGENTE DE MONITORIZAÇÃO AUTOMÓVEL", bg=BG, fg=MUTED, font=("Segoe UI", 9, "bold")).pack(anchor="w")
        self.session_lbl = tk.Label(head, text="SIMULAÇÃO ATIVA", bg=BG, fg=GREEN, font=("Segoe UI", 10, "bold"))
        self.session_lbl.pack(anchor="e")

        bar = tk.Frame(self.root, bg=BG); bar.pack(fill="x", padx=20, pady=(0, 12))
        tk.Button(bar, text="Nova sessão", command=self.new_session, bg="#183c52", fg=CYAN, relief="flat", padx=12, pady=7).pack(side="left", padx=(0, 7))
        tk.Button(bar, text="Terminar sessão + relatório", command=self.end_session, bg=ALT, fg=TEXT, relief="flat", padx=12, pady=7).pack(side="left")
        tk.Button(bar, text="Exportar relatório", command=self.export, bg=ALT, fg=TEXT, relief="flat", padx=12, pady=7).pack(side="right")

        cards = tk.Frame(self.root, bg=BG); cards.pack(fill="x", padx=20, pady=(0, 12))
        self.metric = {}
        for i, (key, label, unit, color) in enumerate([
            ("rpm","ROTAÇÃO DO MOTOR","RPM",CYAN),("temp","TEMPERATURA","°C",YELLOW),
            ("speed","VELOCIDADE","km/h",PURPLE),("battery","TENSÃO DA BATERIA","V",GREEN)]):
            card=tk.Frame(cards,bg=PANEL,highlightbackground="#263650",highlightthickness=1,padx=14,pady=12)
            card.grid(row=0,column=i,sticky="nsew",padx=(0 if i==0 else 8,0)); cards.grid_columnconfigure(i,weight=1)
            tk.Label(card,text=label,bg=PANEL,fg=MUTED,font=("Segoe UI",8,"bold")).pack(anchor="w")
            v=tk.StringVar(value="—"); self.metric[key]=v
            tk.Label(card,textvariable=v,bg=PANEL,fg=color,font=("Segoe UI",22,"bold")).pack(anchor="w",pady=7)
            tk.Label(card,text=unit,bg=PANEL,fg=MUTED,font=("Segoe UI",9)).pack(anchor="w")

        body=tk.Frame(self.root,bg=BG); body.pack(fill="both",expand=True,padx=20,pady=(0,14))
        left=tk.Frame(body,bg=BG); left.pack(side="left",fill="both",expand=True,padx=(0,10))
        right=tk.Frame(body,bg=PANEL,highlightbackground="#263650",highlightthickness=1,width=300); right.pack(side="right",fill="y"); right.pack_propagate(False)
        chartbox=tk.Frame(left,bg=PANEL,highlightbackground="#263650",highlightthickness=1); chartbox.pack(fill="both",expand=True)
        tk.Label(chartbox,text="MONITORIZAÇÃO EM TEMPO REAL",bg=PANEL,fg=TEXT,font=("Segoe UI",10,"bold")).pack(anchor="w",padx=14,pady=(12,3))
        self.chart=tk.Canvas(chartbox,bg=PANEL,highlightthickness=0,height=230); self.chart.pack(fill="both",expand=True,padx=8,pady=8)
        self.chart.bind("<Configure>",lambda e:self.draw_chart())
        diag=tk.Frame(left,bg=PANEL,highlightbackground="#263650",highlightthickness=1); diag.pack(fill="x",pady=(10,0))
        tk.Label(diag,text="DIAGNÓSTICO E ALERTAS",bg=PANEL,fg=TEXT,font=("Segoe UI",10,"bold")).pack(anchor="w",padx=13,pady=(10,5))
        self.diag=tk.Label(diag,text="A iniciar…",bg=PANEL,fg=GREEN,font=("Segoe UI",9,"bold"),anchor="w",wraplength=600)
        self.diag.pack(fill="x",padx=13,pady=(0,8))
        self.alertbox=tk.Listbox(diag,height=4,bg="#0e1626",fg=TEXT,relief="flat",highlightthickness=0,font=("Consolas",9))
        self.alertbox.pack(fill="x",padx=10,pady=(0,10))

        tk.Label(right,text="SIMULADOR DE AVARIAS",bg=PANEL,fg=TEXT,font=("Segoe UI",10,"bold")).pack(anchor="w",padx=13,pady=(13,4))
        tk.Label(right,text="Ativa falhas para testar os alertas.",bg=PANEL,fg=MUTED,font=("Segoe UI",8)).pack(anchor="w",padx=13,pady=(0,8))
        self.faultbtn={}
        for key,label,color in [("overheat","Simular sobreaquecimento",RED),("battery","Simular bateria fraca",YELLOW),("rpm","Simular RPM elevado",PURPLE),("engine","Simular falha do motor",RED)]:
            b=tk.Button(right,text="+  "+label,command=lambda k=key:self.toggle_fault(k),bg=ALT,fg=color,activebackground="#263650",relief="flat",anchor="w",padx=10,pady=8)
            b.pack(fill="x",padx=10,pady=3); self.faultbtn[key]=(b,label,color)
        tk.Button(right,text="Repor estado normal",command=self.reset_faults,bg="#183c52",fg=CYAN,relief="flat",pady=8).pack(fill="x",padx=10,pady=(8,12))
        tk.Label(right,text="HISTÓRICO DE ALERTAS",bg=PANEL,fg=TEXT,font=("Segoe UI",10,"bold")).pack(anchor="w",padx=13,pady=(4,6))
        self.tree=ttk.Treeview(right,columns=("time","level","event"),show="headings",height=8)
        for col,title,width in [("time","Hora",62),("level","Nível",65),("event","Evento",145)]:
            self.tree.heading(col,text=title); self.tree.column(col,width=width,anchor="w")
        self.tree.pack(fill="both",expand=True,padx=8,pady=(0,10))
        self.tree.tag_configure("CRÍTICO",foreground=RED); self.tree.tag_configure("AVISO",foreground=YELLOW)
        self.footer=tk.StringVar(value="Fonte: dados simulados • Base de dados SQLite local")
        tk.Label(self.root,textvariable=self.footer,bg=BG,fg=MUTED,font=("Segoe UI",8)).pack(fill="x",padx=20,pady=(0,10))

    def new_session(self):
        if getattr(self,"session_id",None) is not None and getattr(self,"active",False):
            if not messagebox.askyesno("Nova sessão","A sessão atual está ativa. Iniciar outra?"): return
            self.end_session(show=False)
        with sqlite3.connect(DB) as c:
            cur=c.execute("INSERT INTO sessions(start,status) VALUES(?,?)",(datetime.now().isoformat(timespec="seconds"),"EM CURSO"))
            self.session_id=cur.lastrowid
        self.session_start=time.time(); self.session_duration=0; self.active=True; self.last_alerts=set()
        self.session_lbl.config(text=f"SESSÃO #{self.session_id} • EM CURSO")
        self.footer.set("Fonte: dados simulados • Base de dados SQLite local")

    def toggle_fault(self,key):
        if key in self.faults: self.faults.remove(key)
        else: self.faults.add(key)
        b,label,color=self.faultbtn[key]
        b.config(text=("✓  " if key in self.faults else "+  ")+label,bg="#3b2030" if key in self.faults else ALT)
        self.footer.set("Falhas ativas: "+(", ".join(self.faults) if self.faults else "nenhuma")+" • Dados simulados")

    def reset_faults(self):
        self.faults.clear()
        for b,label,color in self.faultbtn.values(): b.config(text="+  "+label,bg=ALT)
        self.footer.set("Fonte: dados simulados • Base de dados SQLite local")

    def diagnose(self):
        issues=[]
        if self.values["temp"]>100: issues.append(("CRÍTICO","Sobreaquecimento"))
        if self.values["battery"]<11.5: issues.append(("AVISO","Bateria fraca"))
        if self.values["rpm"]>5000: issues.append(("AVISO","RPM elevado"))
        if "engine" in self.faults: issues.append(("CRÍTICO","Possível falha do motor"))
        return issues

    def tick(self):
        if not self.root.winfo_exists(): return
        self.values["rpm"]=random.randint(5100,5900) if "rpm" in self.faults else max(700,min(6000,self.values["rpm"]+random.randint(-240,240)))
        self.values["temp"]=random.uniform(102,115) if "overheat" in self.faults else max(60,min(120,self.values["temp"]+random.uniform(-1,1)))
        self.values["speed"]=max(0,min(180,self.values["speed"]+random.uniform(-5,5)))
        self.values["battery"]=random.uniform(10.7,11.4) if "battery" in self.faults else max(10.5,min(14.2,self.values["battery"]+random.uniform(-.06,.06)))
        if "engine" in self.faults: self.values["rpm"]=random.randint(300,550)
        v=self.values
        self.metric["rpm"].set(f'{v["rpm"]:,}'.replace(","," "))
        self.metric["temp"].set(f'{v["temp"]:.1f}')
        self.metric["speed"].set(f'{v["speed"]:.0f}')
        self.metric["battery"].set(f'{v["battery"]:.2f}')
        issues=self.diagnose()
        self.diag.config(text="  •  ".join(f"{a}: {b}" for a,b in issues) if issues else "SISTEMA NORMAL — sem anomalias nos limites configurados.",fg=RED if any(a=="CRÍTICO" for a,b in issues) else (YELLOW if issues else GREEN))
        current={msg for sev,msg in issues}
        for sev,msg in issues:
            if msg not in self.last_alerts:
                ts=datetime.now().isoformat(timespec="seconds")
                with sqlite3.connect(DB) as c: c.execute("INSERT INTO alerts(session_id,ts,level,message) VALUES(?,?,?,?)",(self.session_id,ts,sev,msg))
                self.alertbox.insert(0,f"{ts[11:19]} [{sev}] {msg}")
                if self.alertbox.size()>6: self.alertbox.delete(6,tk.END)
        self.last_alerts=current
        ts=datetime.now().isoformat(timespec="seconds")
        self.history.append((v["rpm"],v["temp"],v["speed"],v["battery"])); self.history=self.history[-50:]
        if self.active:
            with sqlite3.connect(DB) as c:
                c.execute("INSERT INTO samples(session_id,ts,rpm,temp,speed,battery,status) VALUES(?,?,?,?,?,?,?)",(self.session_id,ts,v["rpm"],v["temp"],v["speed"],v["battery"],"ANOMALIA" if issues else "NORMAL"))
        for item in self.tree.get_children(): self.tree.delete(item)
        with sqlite3.connect(DB) as c:
            rows=c.execute("SELECT ts,level,message FROM alerts WHERE session_id=? ORDER BY id DESC LIMIT 10",(self.session_id,)).fetchall()
        for t,l,m in rows: self.tree.insert("","end",values=(t[11:19],l,m),tags=(l,))
        self.draw_chart()
        self.root.after(1000,self.tick)

    def draw_chart(self):
        if not hasattr(self,"chart"): return
        c=self.chart; c.delete("all"); w=max(c.winfo_width(),300); h=max(c.winfo_height(),160)
        left,right,top,bottom=38,w-12,28,h-22
        for i in range(5):
            y=top+(bottom-top)*i/4; c.create_line(left,y,right,y,fill="#263248",dash=(2,4))
        for x,label,color in [(left,"RPM",CYAN),(left+48,"TEMP",YELLOW),(left+104,"VELOCIDADE",PURPLE),(left+190,"BATERIA",GREEN)]:
            c.create_text(x,10,text=label,fill=color,anchor="w",font=("Segoe UI",8,"bold"))
        if len(self.history)<2:
            c.create_text(w/2,h/2,text="A recolher dados simulados…",fill=MUTED); return
        for idx,(key,lo,hi,color) in enumerate([(0,0,6000,CYAN),(1,60,120,YELLOW),(2,0,180,PURPLE),(3,10.5,14.2,GREEN)]):
            pts=[]
            for i,row in enumerate(self.history):
                x=left+(right-left)*i/(len(self.history)-1); ratio=max(0,min(1,(row[key]-lo)/(hi-lo)))
                pts.extend((x,bottom-ratio*(bottom-top)))
            c.create_line(*pts,fill=color,width=2,smooth=True)

    def report(self):
        with sqlite3.connect(DB) as c:
            agg=c.execute("SELECT MAX(rpm),MAX(temp),MAX(speed),MIN(battery),COUNT(*) FROM samples WHERE session_id=?",(self.session_id,)).fetchone()
            alerts=c.execute("SELECT ts,level,message FROM alerts WHERE session_id=? ORDER BY id DESC LIMIT 12",(self.session_id,)).fetchall()
            start=c.execute("SELECT start FROM sessions WHERE id=?",(self.session_id,)).fetchone()
        duration=int(time.time()-self.session_start) if self.active else getattr(self,"session_duration",0)
        lines=["AUTOCAN — RELATÓRIO DA SESSÃO","="*36,f"Sessão: #{self.session_id}",f"Início: {start[0] if start else '—'}",f"Geração: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}",f"Duração: {duration//60:02d}:{duration%60:02d}",f"Amostras: {agg[4]}", "", "RESUMO",f"RPM máximo: {agg[0] or self.values['rpm']}",f"Temperatura máxima: {agg[1] or self.values['temp']} °C",f"Velocidade máxima: {agg[2] or self.values['speed']} km/h",f"Tensão mínima da bateria: {agg[3] or self.values['battery']} V","","ALERTAS RECENTES"]
        lines += [f"- {t.replace('T',' ')} | {lev} | {msg}" for t,lev,msg in alerts] if alerts else ["- Sem alertas registados."]
        lines += ["","Nota: dados simulados para demonstração académica; não é diagnóstico profissional de veículo real."]
        return "\n".join(lines)

    def end_session(self,show=True):
        if not self.active:
            if show: messagebox.showinfo("Sessão","A sessão já está terminada.")
            return
        with sqlite3.connect(DB) as c: c.execute("UPDATE sessions SET end=?,status=? WHERE id=?",(datetime.now().isoformat(timespec="seconds"),"TERMINADA",self.session_id))
        self.session_duration=int(time.time()-self.session_start); self.active=False; self.session_lbl.config(text=f"SESSÃO #{self.session_id} • TERMINADA")
        text=self.report()
        if show and messagebox.askyesno("Relatório final",text+"\n\nQueres guardar o relatório?"): self.save_report(text)

    def export(self):
        self.save_report(self.report())

    def save_report(self,text):
        path=filedialog.asksaveasfilename(title="Guardar relatório",defaultextension=".txt",filetypes=[("Ficheiro de texto","*.txt")],initialfile=f"AutoCAN_sessao_{self.session_id}.txt")
        if path:
            Path(path).write_text(text,encoding="utf-8")
            messagebox.showinfo("Guardado","Relatório guardado com sucesso.")

    def close(self):
        if self.active and messagebox.askyesno("Sair","Queres terminar a sessão antes de sair?"): self.end_session(False)
        self.root.destroy()

if __name__=="__main__":
    root=tk.Tk()
    app=AutoCAN(root)
    root.mainloop()
