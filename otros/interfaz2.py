import tkinter as tk
from tkinter import ttk
from pathlib import Path
from tkinterdnd2 import DND_FILES, TkinterDnD
from PIL import Image, ImageTk
from pbf_decode import ArchivoPbf
import io


class Interfaz2(TkinterDnD.Tk):
    def __init__(self):
        super(Interfaz2, self).__init__()
        self.geometry('400x250')

        s = ttk.Style()
        print(s.theme_names())
        s.theme_use('clam')
        s.configure(
            'Treeview', rowheight=56, background='gray10',
            fieldbackground='gray10', foreground='white'
        )
        # s.configure('Treeview.Heading', background=[('selected', '#318CE7')], foreground='blue')
        s.layout("Treeview", [('Treeview.treearea', {'sticky': 'nswe'})])
        s.map('Treeview', background=[('selected', '#F4CA16')], foreground=[('selected', '#004242')])

        cols = ['TIEMPO', 'TAGS']
        self.arbol = ttk.Treeview(self, columns=cols)
        self.arbol.heading('#0', text='IMAGEN')
        self.arbol.heading('TIEMPO', text='TIEMPO')
        self.arbol.heading('TAGS', text='TAGS')
        self.columnconfigure(0, weight=1)
        self.arbol.pack(fill='both', expand=1)
        scroll = tk.Scrollbar(self, orient='vertical', command=self.arbol.yview)
        self.arbol.config(yscrollcommand=scroll.set)
        scroll.pack(fill='y', expand=0, side='right', in_=self.arbol)

        self.arbol.column('TIEMPO', width=80)
        self.arbol.column('#0', width=120)
        # self._muestra_imagen()

        self.drop_target_register(DND_FILES)
        self.dnd_bind('<<Drop>>', self.drop_archivo)

    def _muestra_imagen(self):
        with Image.open('3.jpg') as img:
            self.ico = ImageTk.PhotoImage(img.resize((100,55)))
        for x in range(8):
            fila = self.arbol.insert(
                parent='',
                index='end',
                # text='algo',
                values=("01:40:1-{0}", 'marcador con n{0}'.format(x+1)),
                image=self.ico
            )
            # fila.

    def drop_archivo(self, event):
        e = event.data
        if e.startswith('{'):
            e = e[1:]
        if e.endswith('}'):
            e = e[:-1]
        nom = Path(e).name
        self.title(nom)

        pbf = ArchivoPbf(e)
        self.imagenes = []
        uno = pbf.decode()
        
        for item in self.arbol.get_children():
            self.arbol.delete(item)

        for d in uno:
            img1 = d.get('imagen hex')
            # self.ico = ImageTk.PhotoImage(data=img1)
            valores = d.get('tiempo'), d.get('titulo')
            self.ico = ImageTk.PhotoImage(self.quita_bordes_negros(img1))
            self.imagenes.append(self.ico)
            self.arbol.insert(parent='', index='end', image=self.ico, values=valores)
        # self.update()

    def quita_bordes_negros(self, img_hex, md=16):
        filei = io.BytesIO(img_hex)
        img_pil = Image.open(filei)
        w, h = img_pil.size
        # return img_pil.crop((0,md,w,h-md))
        return img_pil.crop((0,md,w,h-md)).resize((100,55))

        


if __name__=="__main__":
    app = Interfaz2()
    app.mainloop()