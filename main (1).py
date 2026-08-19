# Simple Library Management System
import tkinter as tk
from tkinter import ttk, messagebox
import json, os
FILE="books.json"
books=[]
def load():
    global books
    if os.path.exists(FILE):
        books=json.load(open(FILE))
def save():
    json.dump(books,open(FILE,"w"),indent=2)
def refresh():
    for i in tree.get_children(): tree.delete(i)
    tstok=tdip=0
    for i,b in enumerate(books):
        tstok+=b["stok"]; tdip+=1 if b["peminjam"] else 0
        tree.insert("",'end',iid=str(i),values=(b["judul"],b["stok"],b["kondisi"],b["peminjam"],b["pinjam"],b["kembali"]))
    lbl.config(text=f"Judul:{len(books)} | Stok:{tstok} | Dipinjam:{tdip}")
def add():
    books.append({"judul":e1.get(),"stok":int(e2.get() or 0),"kondisi":e3.get(),"peminjam":"","pinjam":"","kembali":""});save();refresh()
def sel(evt):
    s=tree.focus()
    if not s:return
    b=books[int(s)]
    for e,v in [(e1,b["judul"]),(e2,str(b["stok"])),(e3,b["kondisi"]),(e4,b["peminjam"]),(e5,b["pinjam"]),(e6,b["kembali"])]:
        e.delete(0,'end');e.insert(0,v)
def edit():
    s=tree.focus()
    if not s:return
    b=books[int(s)]
    b.update(judul=e1.get(),stok=int(e2.get() or 0),kondisi=e3.get());save();refresh()
def delete():
    s=tree.focus()
    if not s:return
    books.pop(int(s));save();refresh()
def borrow():
    s=tree.focus()
    if not s:return
    b=books[int(s)]
    if b["stok"]<1: 
       messagebox.showerror("Error","Stok habis");
       return
    b["stok"]-=1;b["peminjam"]=e4.get();b["pinjam"]=e5.get();b["kembali"]=e6.get();save();refresh()
def ret():
    s=tree.focus()
    if not s:return
    b=books[int(s)]
    b["stok"]+=1;b["peminjam"]=b["pinjam"]=b["kembali"]="";save();refresh()
def search():
    q=es.get().lower()
    for i in tree.get_children(): tree.delete(i)
    for i,b in enumerate(books):
        if q in b["judul"].lower():
            tree.insert("",'end',iid=str(i),values=(b["judul"],b["stok"],b["kondisi"],b["peminjam"],b["pinjam"],b["kembali"]))
root=tk.Tk();root.title("Library");lbl=tk.Label(root);lbl.pack()
f=tk.Frame(root);f.pack()
labs=["Judul","Stok","Kondisi","Peminjam","Tgl Pinjam","Tgl Kembali"];ents=[]
for i,l in enumerate(labs):
    tk.Label(f,text=l).grid(row=i,column=0)
    e=tk.Entry(f);e.grid(row=i,column=1);ents.append(e)
e1,e2,e3,e4,e5,e6=ents
for t,c in [("Tambah",add),("Edit",edit),("Hapus",delete),("Pinjam",borrow),("Kembali",ret)]:
    tk.Button(f,text=t,command=c).grid(sticky="ew")
sf=tk.Frame(root);sf.pack()
es=tk.Entry(sf);es.pack(side="left");tk.Button(sf,text="Cari",command=search).pack(side="left")
tree=ttk.Treeview(root,columns=("j","s","k","p","tp","tk"),show="headings")
for c,h in zip(("j","s","k","p","tp","tk"),("Judul","Stok","Kondisi","Peminjam","Pinjam","Kembali")):
    tree.heading(c,text=h)
tree.pack(fill="both",expand=True)
tree.bind("<<TreeviewSelect>>",sel)
load();refresh();root.mainloop()
