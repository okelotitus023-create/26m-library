from flask import Flask, request, redirect, session
import sqlite3, os
from datetime import date, datetime
app = Flask(__name__)
app.secret_key = '26M-SECURE-2024'
DB='library.db'
os.makedirs('static',exist_ok=True)

def init():
 con=sqlite3.connect(DB)
 con.execute('CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username TEXT UNIQUE, password TEXT, email TEXT)')
 con.execute('CREATE TABLE IF NOT EXISTS students (id INTEGER PRIMARY KEY, name TEXT, adm TEXT UNIQUE, phone TEXT, course TEXT, d TEXT)')
 con.execute('CREATE TABLE IF NOT EXISTS attendance (id INTEGER PRIMARY KEY, adm TEXT, name TEXT, d TEXT, t TEXT)')
 con.execute('CREATE TABLE IF NOT EXISTS issues (id INTEGER PRIMARY KEY, adm TEXT, week TEXT, module TEXT, unit TEXT, problem TEXT, d TEXT)')
 c=con.cursor()
 c.execute("SELECT * FROM users WHERE username='admin'")
 if not c.fetchone():
  c.execute("INSERT INTO users (username,password,email) VALUES (?,?,?)",('admin','admin26m','admin@26m.com'))
 else:
  c.execute("UPDATE users SET password=? WHERE username='admin'",('admin26m',))
 con.commit()
 con.close()
init()

def get_bgs():
 bgs=[]
 for i in range(1,5):
  p=f'static/bg{i}.jpg'
  if os.path.exists(p): bgs.append(f"/static/bg{i}.jpg")
  else: bgs.append("")
 return bgs

def get_stats():
 con=sqlite3.connect(DB);c=con.cursor()
 c.execute("SELECT COUNT(*) FROM students");total=c.fetchone()[0]
 c.execute("SELECT COUNT(*) FROM issues");issues=c.fetchone()[0]
 td=str(date.today())
 c.execute("SELECT COUNT(*) FROM attendance WHERE d=?",(td,));present=c.fetchone()[0]
 absent=total-present if total>=present else 0
 perc=round((present/total*100) if total>0 else 0,1)
 con.close()
 return total,issues,present,absent,perc,td

def neon_css():
 bgs=get_bgs()
 return f"<meta name='viewport' content='width=device-width,initial-scale=1'><style>*{{margin:0;padding:0;box-sizing:border-box;font-family:sans-serif}}body{{min-height:100vh;display:flex;align-items:center;justify-content:center;background:#020617;overflow:hidden}}.bg{{position:fixed;top:0;left:0;width:100%;height:100%;z-index:-2;display:grid;grid-template-columns:1fr 1fr;grid-template-rows:1fr 1fr;gap:10px;padding:10px;background:#020617}}.b{{background-size:cover;background-position:center;border-radius:18px;filter:brightness(0.6)}}.circle{{width:420px;height:420px;background:rgba(10,15,35,0.95);border-radius:50%;display:flex;flex-direction:column;align-items:center;justify-content:center;padding:30px;box-shadow:0 0 20px #22d3ee;border:1px solid #22d3ee;z-index:5}}.inp{{width:100%;background:rgba(0,0,0,0.6);border:1px solid #334155;border-radius:20px;padding:11px 16px;color:white;margin:6px 0}}.btn{{width:100%;padding:11px;border-radius:20px;border:1px solid #22d3ee;background:linear-gradient(90deg,#06b6d4,#8b5cf6);color:white;font-weight:bold;cursor:pointer}} </style><div class=bg><div class=b style=\"background-image:url('{bgs[0]}')\"></div><div class=b style=\"background-image:url('{bgs[1]}')\"></div><div class=b style=\"background-image:url('{bgs[2]}')\"></div><div class=b style=\"background-image:url('{bgs[3]}')\"></div></div>"

def main_css():
 return "<meta name='viewport' content='width=device-width,initial-scale=1'><style>*{margin:0;padding:0;box-sizing:border-box;font-family:sans-serif}body{min-height:100vh;background:#f1f5f9}.top{background:#16a34a;color:white;padding:12px;display:flex;justify-content:space-between;position:sticky;top:0;z-index:9}.nav{display:flex;gap:5px;padding:8px;flex-wrap:wrap;background:#f1f5f9;position:sticky;top:48px;z-index:8}.nav a{background:white;color:#16a34a;padding:6px 10px;border-radius:20px;text-decoration:none;font-weight:bold;font-size:12px;box-shadow:0 1px 3px rgba(0,0,0,0.1)}.nav a.on{background:#16a34a;color:white}.card{background:white;margin:8px;padding:14px;border-radius:14px;box-shadow:0 2px 8px rgba(0,0,0,0.08)}.g4{display:grid;grid-template-columns:1fr 1fr;gap:8px}.stat{padding:16px;border-radius:14px;font-weight:bold;text-align:center}.w{background:white;border:2px solid #e2e8f0}.b{background:#38bdf8}.y{background:#facc15}.r{background:#f87171;color:white}.btn{padding:12px;border:none;border-radius:10px;color:white;font-weight:bold;width:100%;display:block;text-align:center;text-decoration:none;margin:4px 0}.btn-g{background:#16a34a}.btn-p{background:#7c3aed}.btn-o{background:#f59e0b}.btn-b{background:#0ea5e9}input,select,textarea{width:100%;padding:11px;margin:6px 0;border:2px solid #bbf7d0;border-radius:10px}table{width:100%;border-collapse:collapse;font-size:12px}th,td{border:1px solid #ddd;padding:6px}th{background:#dcfce7}.title{font-size:16px;font-weight:bold;color:#16a34a;margin-bottom:6px}.desc{font-size:11px;color:#6b7280;margin-bottom:10px}</style>"

@app.route('/')
def home(): return redirect('/login')

@app.route('/login',methods=['GET','POST'])
def login():
 msg=''
 if request.method=='POST':
  u=request.form['u'].strip(); p=request.form['p'].strip()
  con=sqlite3.connect(DB);c=con.cursor()
  c.execute("SELECT * FROM users WHERE (username=? OR email=?) AND password=?",(u,u,p))
  r=c.fetchone();con.close()
  if r:
   session['u']=r[1]; return redirect('/dashboard')
  else: msg="<div style='color:#fca5a5;font-size:12px;background:rgba(239,68,68,0.2);padding:6px;border-radius:8px;margin:5px 0'>Invalid username or password!</div>"
 return neon_css()+f"<div class=circle><h2 style='color:#22d3ee;font-size:20px;text-align:center'>WELCOME TO 26M LIBRARY</h2><p style='color:#64748b;font-size:11px;margin:10px'>Secure Login System</p>{msg}<form method=POST style='width:100%'><input class=inp name=u placeholder='Username' required><input class=inp name=p type=password placeholder='Password' required><button class=btn>LOGIN</button></form><p style='font-size:11px;color:#64748b;margin-top:14px'>No account? <a href='/signup' style='color:#22d3ee;font-weight:bold;text-decoration:none'>Sign Up</a></p></div>"

@app.route('/signup',methods=['GET','POST'])
def signup():
 msg=''
 if request.method=='POST':
  u=request.form['u'].strip().lower();p=request.form['p'].strip()
  if u=='admin':
   msg="<div style='color:#fca5a5;font-size:12px;background:rgba(239,68,68,0.2);padding:6px;border-radius:8px'>Cannot use admin username!</div>"
  elif len(u)<3 or len(p)<3:
   msg="<div style='color:#fca5a5;font-size:12px'>Min 3 chars</div>"
  else:
   con=sqlite3.connect(DB);c=con.cursor()
   try: c.execute("INSERT INTO users (username,password,email) VALUES (?,?,?)",(u,p,''));con.commit();con.close();session['u']=u;return redirect('/dashboard')
   except: con.close();msg="<div style='color:#fca5a5;font-size:12px'>Username taken!</div>"
 return neon_css()+f"<div class=circle><h2 style='color:#22d3ee;font-size:18px'>CREATE ACCOUNT</h2>{msg}<form method=POST style='width:100%'><input class=inp name=u placeholder='Choose Username' required><input class=inp name=p type=password placeholder='Choose Password' required><button class=btn>SIGN UP</button></form><p style='font-size:11px;color:#64748b;margin-top:14px'>Have account? <a href='/login' style='color:#22d3ee;font-weight:bold;text-decoration:none'>Login</a></p></div>"

@app.route('/dashboard')
def dash():
 if 'u' not in session: return redirect('/login')
 total,issues,present,absent,perc,td=get_stats()
 return main_css()+f"<div class=top><b>26M LIBRARY | {session['u']} | {td}</b><a href=/logout style='background:#ef4444;color:white;padding:5px 10px;border-radius:20px;text-decoration:none;font-size:12px'>Logout</a></div><div class=nav><a href=/dashboard class=on>Dashboard</a><a href=/students>Students ({total})</a><a href=/units>Units</a><a href=/issues>Issues ({issues})</a><a href=/register>Register ({present}/{total})</a><a href=/admin_monitor style='background:#7c3aed;color:white'>Admin Monitor</a></div><div class=card><div class=title>LIVE MONITOR - Auto Calculation</div><div class=desc>Today {td} | {perc}% Present</div></div><div class=g4><div class='stat w'>Students: {total}</div><div class='stat b'>Issues: {issues}</div><div class='stat y'>Present: {present}<br>{perc}%</div><div class='stat r'>Absent: {absent}<br>{total}-{present}={absent}</div></div><div class=card><div class=g4><a href=/students class='btn btn-g'>Add Student</a><a href=/register class='btn btn-o'>Mark Present</a><a href=/admin_monitor class='btn btn-b'>Admin Monitor</a><a href=/units class='btn btn-p'>Units</a></div></div>"

@app.route('/admin_monitor')
def admin_monitor():
 if 'u' not in session: return redirect('/login')
 if session.get('u')!='admin': return "<script>alert('Only admin can access monitor!');window.location='/dashboard'</script>"
 total,issues,present,absent,perc,td=get_stats()
 con=sqlite3.connect(DB);c=con.cursor()
 c.execute("SELECT * FROM students ORDER BY id DESC");all_students=c.fetchall()
 c.execute("SELECT adm FROM attendance WHERE d=?",(td,));present_adms=[x[0] for x in c.fetchall()]
 c.execute("SELECT * FROM attendance WHERE d=? ORDER BY t DESC",(td,));today=c.fetchall()
 con.close()
 absent_list=[s for s in all_students if s[2] not in present_adms]
 html=main_css()+f"<div class=top><b>ADMIN MONITOR SECURE | {td}</b><a href=/dashboard style='background:white;color:#16a34a;padding:5px 10px;border-radius:20px;text-decoration:none'>Back</a></div><div class=nav><a href=/dashboard>Dashboard</a><a href=/admin_monitor class=on>Admin Monitor</a><a href=/students>Students</a><a href=/register>Register</a></div>"
 html+=f"<div class=card><div class=g4><div class='stat w'><span style='font-size:22px'>{total}</span><br>Students</div><div class='stat y'><span style='font-size:22px'>{present}</span><br>Present<br>{perc}%</div><div class='stat r'><span style='font-size:22px'>{absent}</span><br>Absent</div><div class='stat b'><span style='font-size:22px'>{issues}</span><br>Issues</div></div><div style='background:#f0fdf4;padding:8px;border-radius:8px;font-size:11px;margin-top:8px'>Auto: Absent = {total} - {present} = {absent}</div></div>"
 html+=f"<div class=g4><div class=card><div class=title>Present Today {present}</div><table><tr><th>Time</th><th>Name</th><th>ADM</th></tr>"
 for r in today: html+=f"<tr><td>{r[4]}</td><td>{r[2]}</td><td>{r[1]}</td></tr>"
 if not today: html+="<tr><td colspan=3>No attendance yet</td></tr>"
 html+="</table></div><div class=card><div class=title>Absent Today "+str(absent)+"</div><table><tr><th>Name</th><th>ADM</th></tr>"
 for s in absent_list[:20]: html+=f"<tr><td>{s[1]}</td><td>{s[2]}</td></tr>"
 html+="</table></div></div>"
 html+=f"<div class=card><div class=title>All Students {total}</div><table><tr><th>Name</th><th>ADM</th><th>Course</th><th>Status</th></tr>"
 for s in all_students:
  status="Present" if s[2] in present_adms else "Absent"
  color="#16a34a" if status=="Present" else "#ef4444"
  html+=f"<tr><td>{s[1]}</td><td>{s[2]}</td><td>{s[4]}</td><td style='color:{color};font-weight:bold'>{status}</td></tr>"
 html+="</table></div>"
 return html

@app.route('/students',methods=['GET','POST'])
def stud():
 if 'u' not in session: return redirect('/login')
 total,issues,present,absent,perc,td=get_stats()
 con=sqlite3.connect(DB);c=con.cursor()
 msg=""
 if request.method=='POST':
  try:
   c.execute("INSERT INTO students (name,adm,phone,course,d) VALUES (?,?,?,?,?)",(request.form['name'],request.form['adm'],request.form['phone'],request.form['course'],str(date.today())));con.commit()
   msg=f"<div style='background:#dcfce7;padding:8px;border-radius:8px;font-size:12px;color:#16a34a'>Added! Total now {total+1}</div>"
  except: msg="<div style='background:#fee2e2;padding:8px;border-radius:8px;font-size:12px;color:#ef4444'>ADM exists!</div>"
 c.execute("SELECT * FROM students ORDER BY id DESC");rows=c.fetchall();con.close()
 tr="".join([f"<tr><td>{r[1]}</td><td>{r[2]}</td><td>{r[3]}</td><td>{r[4]}</td></tr>" for r in rows])
 return main_css()+f"<div class=top><b>Students Total:{len(rows)} Present:{present} Absent:{absent}</b></div><div class=nav><a href=/dashboard>Dashboard</a><a href=/students class=on>Students</a><a href=/register>Register</a><a href=/admin_monitor>Monitor</a></div><div class=card><div class=g4><div class='stat w'>{len(rows)} Students</div><div class='stat y'>{present} Present</div><div class='stat r'>{absent} Absent</div><div class='stat b'>{issues} Issues</div></div></div>{msg}<div class=card><form method=POST><input name=name placeholder='Full Name' required><input name=adm placeholder='ADM Unique' required><input name=phone placeholder='Phone' required><input name=course placeholder='Course' required><button class='btn btn-g'>ADD STUDENT</button></form></div><div class=card><table><tr><th>Name</th><th>ADM</th><th>Phone</th><th>Course</th></tr>{tr if tr else '<tr><td colspan=4>No students yet</td></tr>'}</table></div>"

@app.route('/register',methods=['GET','POST'])
def reg():
 if 'u' not in session: return redirect('/login')
 td=str(date.today())
 total,issues,present,absent,perc,td2=get_stats()
 con=sqlite3.connect(DB);c=con.cursor()
 msg=""
 if request.method=='POST':
  adm=request.form['adm'].strip()
  c.execute("SELECT name FROM students WHERE adm=?",(adm,));r=c.fetchone()
  if not r: msg=f"<div style='background:#fee2e2;padding:8px;border-radius:8px;font-size:12px;color:#ef4444'>ADM {adm} not found!</div>"
  else:
   c.execute("SELECT * FROM attendance WHERE adm=? AND d=?",(adm,td));ex=c.fetchone()
   if ex: msg=f"<div style='background:#fef3c7;padding:8px;border-radius:8px;font-size:12px'>Already present at {ex[4]}</div>"
   else:
    c.execute("INSERT INTO attendance (adm,name,d,t) VALUES (?,?,?,?)",(adm,r[0],td,datetime.now().strftime('%H:%M')));con.commit()
    msg=f"<div style='background:#dcfce7;padding:8px;border-radius:8px;font-size:12px;color:#16a34a'>SUCCESS {r[0]} marked present!</div>"
 c.execute("SELECT * FROM students");alls=c.fetchall()
 c.execute("SELECT adm FROM attendance WHERE d=?",(td,));prs=[x[0] for x in c.fetchall()]
 con.close()
 tr="".join([f"<tr><td>{s[1]}</td><td>{s[2]}</td><td>{'Present' if s[2] in prs else 'Absent'}</td></tr>" for s in alls])
 return main_css()+f"<div class=top><b>Register {td} P:{present} A:{absent} {perc}%</b></div><div class=nav><a href=/dashboard>Dashboard</a><a href=/students>Students</a><a href=/register class=on>Register ({present}/{total})</a><a href=/admin_monitor>Monitor</a></div><div class=card><div class=g4><div class='stat w'>Total: {total}</div><div class='stat y'>Present: {present}</div><div class='stat r'>Absent: {absent}</div><div class='stat b'>{issues} Issues</div></div></div>{msg}<div class=card><form method=POST><input name=adm placeholder='ADM to mark present' required><button class='btn btn-o'>MARK PRESENT</button></form></div><div class=card><table><tr><th>Name</th><th>ADM</th><th>Status Auto</th></tr>{tr if tr else '<tr><td colspan=3>No students</td></tr>'}</table></div>"

@app.route('/units')
def units_page():
 if 'u' not in session: return redirect('/login')
 return main_css()+"<div class=top><b>Units</b></div><div class=nav><a href=/dashboard>Dashboard</a><a href=/units class=on>Units</a></div><div class=card><div class=title>Module 1</div><p>Computer Operations</p><p>Internet and Email</p><p>Library Management</p></div>"

@app.route('/issues',methods=['GET','POST'])
def iss():
 if 'u' not in session: return redirect('/login')
 total,issues,present,absent,perc,td=get_stats()
 con=sqlite3.connect(DB);c=con.cursor()
 if request.method=='POST':
  c.execute("INSERT INTO issues (adm,week,module,unit,problem,d) VALUES (?,?,?,?,?,?)",(request.form['adm'],request.form['week'],request.form['module'],request.form['unit'],request.form['problem'],str(date.today())));con.commit()
 c.execute("SELECT * FROM issues ORDER BY id DESC");rows=c.fetchall();con.close()
 tr="".join([f"<tr><td>{r[2]}</td><td>{r[1]}</td><td>{r[4]}</td><td>{r[5][:30]}</td></tr>" for r in rows])
 return main_css()+f"<div class=top><b>Issues {len(rows)}</b></div><div class=nav><a href=/dashboard>Dashboard</a><a href=/issues class=on>Issues</a><a href=/register>Register</a></div><div class=card><form method=POST><input name=adm placeholder='ADM' required><input name=week placeholder='Week' required><select name=module required><option value=''>Module</option><option>Module 1</option><option>Module 2</option></select><select name=unit required><option value=''>Unit</option><option>Computer Operations</option><option>Library</option></select><textarea name=problem placeholder='Problem' required></textarea><button class='btn btn-p'>Submit</button></form></div><div class=card><table><tr><th>Week</th><th>ADM</th><th>Unit</th><th>Problem</th></tr>{tr if tr else '<tr><td colspan=4>No issues</td></tr>'}</table></div>"

@app.route('/logout')
def lo(): session.clear();return redirect('/login')

if __name__=="__main__":
    import os
    port = int(os.environ.get("PORT", 8000))
    app.run(host="0.0.0.0", port=port)
