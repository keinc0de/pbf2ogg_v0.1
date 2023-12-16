import tkinter as tk
# from tkinter import ttk
from pathlib import Path
from tkinterdnd2 import DND_FILES, TkinterDnD
from pbf_decode import ArchivoPbf
# from pprint import pprint


class Ventana(TkinterDnD.Tk):
    def __init__(self):
        super(Ventana, self).__init__()
        self.geometry('400x220')

        self.info = tk.Text(self, bg='gray10', foreground='white', font=('Segoe UI', 10), height=8)
        self.info.pack(expand=1, fill='both')
        self.scroll = tk.Scrollbar(self, orient='vertical', command=self.info.yview)
        self.info.config(yscrollcommand=self.scroll.set, relief='flat')
        self.scroll.pack(fill='y', expand=0, side='right', in_=self.info)
        fmb = tk.Frame(self, bg='gray10')
        fmb.pack(expand=0, fill='x')
        self.lb = tk.Label(fmb,bg='gray10', fg='#F0EAD6', justify='left')
        self.lb.pack(side='left', fill='x', expand=1)
        self.bt_save = tk.Button(
            fmb, text='CREAR OGG', bg='gray10', fg='#F0EAD6', command=self.crea_archivo_ogg
        )
        self.bt_save.pack(side='left')
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self.columnconfigure(0, weight=1)
        self.drop_target_register(DND_FILES)
        self.dnd_bind('<<Drop>>', self.drop_archivo)

        self.valores_iniciales()

    def valores_iniciales(self):
        self.archivo = None
        self.contenido = []
        self.title('CREAR OGG v0.1')
        ico_data = 'iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAChElEQVR4nG2STWiVVxCGn3fO98WrtEQxYiyGpgvrQkGksaKg0l3diLgwosWAomkiiEvtJstis6gGDChiNopt6kpdiBa6Kd0EtbYY9LYi/kRLQETivTf35zvjwpO2iAMDZ+aceefh5Yi3sQxYCjSBAPwDfAB8mHo5cC/drQRaQAFU0jzfAv6/vAj89k7vEPDlO717lgTqQBXYD1wG1gHtwE1gL/AKWJWGmsApYAdwaE5AQAn4GtgEzAA1YDmwPZ0vpSV5erMPqMwJtJLyMmAKOAm8SF6MALeAY8mnGWAMOABMkow5kfCWg2hnzUIRHoAc5CK4yMbAdoLcaDssArAlUyLoAVYDV9JmEuYnia4OXE/424BriQ4BPwK9ABJ87tMrsGK0jSWsjeGrVTBzIXCu6S+7S3FR3wA8/t5eXYpUl+aBfgGT4+PjWyYmJmaHh4erG7OpscKptnz2fsC2In8hrKpozx3riNZcYGQNok2BfWwhhD/v3r2ztlKpnMnzUNSLWEcqB817KvLFFuchz2+77AHSZxbbojz7HflDVPRI0mt3/6Ozs3NDX9/ukV9Hvplfr8/+Zeip4Iicskv3YwxnlXm3Fb4vqpjy2DydZeFTK5VKX5RKC251dXW1urs/utpoFdEIc+YaqOlORwjF0VDEXscbclscQn7Ui7Arq9VqE6Ojo+2NRuOXgYEjN9aH3p1O5hAzsCgUJH+Cqx4Vd8j1dxRlc2pR7MkAGxwc/Pm/H5m1C49RPm2uEOWLDGtJ9XLhmbvoMGwyyss4GBDdXUNDQwY47peF7zfPjxvF6Ug87yr6o+ffiTgu9AMqDuI6LvQT74t1POrZkE1v/rfOnr2nfrYZXG8AI6QSSdtwwLAAAAAASUVORK5CYII='
        ico = tk.PhotoImage(data=ico_data)
        self.iconphoto(True, ico)

    def drop_archivo(self, event):
        e = event.data
        if e.startswith('{'):
            e = e[1:]
        if e.endswith('}'):
            e = e[:-1]
        nom = Path(e).name
        self.title(nom)

        # LECTURA PBF
        self.valores_iniciales()
        pbf = ArchivoPbf(e)
        self.info.delete(1.0, tk.END)
        try:
            linea_texto = f"CHAPTER01=00:00:00.000\n"\
                        f"CHAPTER01NAME=01 inicio\n"
            self.contenido.append(linea_texto)
            for x, md in enumerate(pbf.decode()):
                indice, tiempo, titulo = x+1, md.get('tiempo'), md.get('titulo')
                self.escribe(f"{indice:>2} ", 'num', foreground='#A2BBB0', font=('consolas', 10))
                self.escribe(f"{tiempo}", 'uno', foreground='#E4EC24', font=('Segoe UI', 10, 'italic'))
                self.escribe(' -> ', 'dos', foreground='#A2BBB0')
                self.escribe(f"{titulo}\n", 'tres', foreground='#F0EAD6')
                linea_texto = f"CHAPTER{indice+1:02d}={tiempo}\n"\
                            f"CHAPTER{indice+1:02d}NAME={indice+1:02d} {titulo}\n"
                self.contenido.append(linea_texto)
            self.lb.config(text=f"{str(indice)} marcadores. - {nom}", fg='#A2C776')
            self.archivo = Path(e)
        except Exception as err:
            self.lb.config(text=f"ERR: {err}", fg='#E45C68')
        self.info.see('end')

    def escribe(self, texto, s, **kwargs):
        self.info.insert('end', texto, s)
        self.info.tag_config(s, **kwargs)

    def crea_archivo_ogg(self):
        if self.archivo is not None:
            nom = f"OGG {self.archivo.stem}.txt"
            ruta = f"{self.archivo.with_name(nom)}"
            with open(ruta, 'w') as txt:
                txt.writelines(self.contenido)
            self.lb.config(text='archivo OGG creado.')


if __name__ == '__main__':
    app = Ventana()
    app.mainloop()