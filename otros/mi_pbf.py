from pathlib import Path

class MiPbf:
    def __init__(self, video=None):
        pbf = Path(video).with_suffix('.pbf').as_posix()
        self.ruta_pbf = pbf if Path(pbf).exists()==True else None

    def hex2str(self, texto_hex):
        return str(texto_hex.decode('utf-8', errors='ignore'))
    
    def lee_bin(self, r_pbf):
        with open(r_pbf, 'rb') as txt:
            return [self.hex2str(l) for l in txt.readlines()]
        
    def lee(self, r_pbf):
        with open(r_pbf, 'r') as txt:
            return [l.replace('\n', '') for l in txt.readlines()]

    def traduce(self, r_pbf):
        lineas = self.lee(r_pbf)
        data = []
        for linea in lineas:
            if '*' in linea:
                nlinea = linea.replace('\x00', '').split('*')
                titulo = nlinea[-2]
                ms = int(nlinea[0].split('=')[-1])
                # img_hex = nlinea[-1].rsplit('0'*43)[-1]
                t = self.ms2Hms(ms)
                tc = self.ms2Hms(ms, acorta=True)
                data.append({
                    'ms':ms,
                    # 'img hex':bytes.fromhex(img_hex),
                    't':t,
                    'tc':tc,
                    'seg':ms/1e3,
                    'titulo':titulo
                })
        return data
    
    def ms2Hms(self, ms, acorta=False):
        h, r = divmod(ms, 3.6e6)
        m, r = divmod(r, 6e4)
        s, _ = divmod(r, 1e3)
        t = f"{int(h)}:{int(m):02d}:{int(s):02d}.{int(_):03d}"
        tiempo = t[2::] if t.startswith('0:') and acorta else t
        return tiempo
    
    def data(self):
        data = []
        if self.ruta_pbf is not None:
            data = self.traduce(self.ruta_pbf)
        return data
    
    def obten_data(self, valor='t'):
        return [d.get(valor) for d in self.data()]
    
    def hms2ms(self, timestamp):
        hms, ms = timestamp.split('.')
        h, m, s = hms.split(':')
        return int(1e3*(int(h) * 3600 + int(m) * 60 + int(s)) + int(ms))


if __name__=='__main__':
    p1 = r'elles.pbf'
    pbf = MiPbf()
    _ = pbf.traduce(p1)
    d = _[-1]
    print(d.get('tc'), d.get('t'), d.get('ms'), d.get('seg'))
    img = d.get('img hex')
    # FUNCIONA
    # with open('image.png', 'wb') as file:
    #     file.write(img)