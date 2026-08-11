#!/usr/bin/env python3
"""Genera el banner de la firma: banner.html -> banner@1x.png y banner@2x.png.

Se hacen DOS tamaños a propósito. El que se usa es el @2x (1200x300 mostrado a
600 px): en pantallas retina el @1x se ve borroso, y en el correo no hay forma
de arreglarlo después.
"""
import perfil as P
from _comun import (SALIDA, ajusta, captura, constelacion, esc, fuentes_google,
                    kb, optimiza, svg_constelacion)

W, H = 600, 150
C = P.PALETA

# Lo que queda para el nombre: 600 menos los márgenes y menos el motivo de la
# derecha. Si el nombre es largo, encoge en vez de salirse.
NOMBRE_COMPLETO = f"{P.NOMBRE} {P.APELLIDO}"
TAM_NOMBRE = ajusta(31, W - 26 - 6 - 150 - 26 - 10, NOMBRE_COMPLETO)

# El motivo vive en un recuadro de 150x120 a la derecha. Separación y radio más
# cortos que en la portada de LinkedIn porque el lienzo es diez veces menor.
nodos, aristas = constelacion(150, 120, P.MOTIVO["nodos"], P.MOTIVO["semilla"],
                              margen=22, separacion=30, radio=78, grado_max=3)
motivo = svg_constelacion(nodos, aristas, C["tinta"], C["metal"],
                          r_min=2.2, r_var=2.6, aros=2)

ante = P.ANTETITULO
bloque_ante = ""
if ante.get("destacado") or ante.get("resto"):
    bloque_ante = (f'<div class="eyebrow"><b>{esc(ante.get("destacado", ""))}</b>'
                   f'&nbsp;{esc(ante.get("resto", ""))}</div>')

bloque_web = ""
if P.WEB.get("texto"):
    bloque_web = (f'<div class="rule"></div>'
                  f'<div class="link">{esc(P.WEB["texto"])} '
                  f'<span class="arrow">&#8599;</span></div>')

html = f"""<!doctype html>
<meta charset="utf-8">
{fuentes_google(P)}
<style>
  *{{margin:0;padding:0;box-sizing:border-box}}
  html,body{{background:#fff}}
  .banner{{
    position:relative; width:{W}px; height:{H}px; overflow:hidden;
    background:linear-gradient(105deg,#E5E4DE 0%,{C["papel"]} 46%,#D6D3C8 100%);
    border:1px solid rgba(30,58,52,0.16);
    display:flex; align-items:center; padding:0 26px;
  }}
  /* Marcas de instrumento en las esquinas. No son decoración gratuita: hacen
     que el banner lea como TARJETA y no como un bloque blanco huérfano, que es
     lo que pasa en el modo oscuro de Gmail (no invierte las imágenes). */
  .tick{{position:absolute;width:9px;height:9px;border:1.25px solid {C["metal"]};opacity:.75}}
  .tl{{top:9px;left:9px;border-right:0;border-bottom:0}}
  .tr{{top:9px;right:9px;border-left:0;border-bottom:0}}
  .bl{{bottom:9px;left:9px;border-right:0;border-top:0}}
  .br{{bottom:9px;right:9px;border-left:0;border-top:0}}

  .txt{{position:relative;flex:1;padding-left:6px}}
  .eyebrow{{font-family:'{P.FUENTES["mono"]}',monospace;font-weight:500;font-size:8.5px;
            letter-spacing:.19em;text-transform:uppercase;color:{C["apagado"]};
            margin-bottom:9px;}}
  .eyebrow b{{color:{C["acento"]};font-weight:600}}
  .name{{font-family:'{P.FUENTES["titulo"]}',Georgia,serif;font-weight:600;font-size:{TAM_NOMBRE:.1f}px;
         line-height:1;letter-spacing:.005em;color:{C["tinta"]};white-space:nowrap}}
  .role{{font-family:'{P.FUENTES["mono"]}',monospace;font-weight:400;font-size:10px;
         letter-spacing:.15em;text-transform:uppercase;color:{C["tinta"]};opacity:.8;
         margin-top:9px;}}
  .rule{{width:74px;height:1px;background:{C["metal"]};opacity:.55;margin:12px 0 10px}}
  .link{{font-family:'{P.FUENTES["mono"]}',monospace;font-weight:500;font-size:10.5px;
         color:{C["acento"]};}}
  .link .arrow{{color:{C["metal"]}}}
  .mark{{position:relative;width:150px;height:120px;flex:0 0 auto;opacity:.92}}
</style>

<div class="banner">
  <i class="tick tl"></i><i class="tick tr"></i><i class="tick bl"></i><i class="tick br"></i>
  <div class="txt">
    {bloque_ante}
    <div class="name">{esc(NOMBRE_COMPLETO)}</div>
    <div class="role">{esc(P.ROL)}</div>
    {bloque_web}
  </div>
  <svg class="mark" viewBox="0 0 150 120" fill="none">{motivo}</svg>
</div>
"""

if __name__ == "__main__":
    SALIDA.mkdir(exist_ok=True)
    fuente = SALIDA / "banner.html"
    fuente.write_text(html, encoding="utf-8")

    for escala, nombre in ((2, "banner@2x.png"), (1, "banner@1x.png")):
        destino = SALIDA / nombre
        captura(fuente, destino, W, H, escala)
        optimiza(destino)
        print(f"  {nombre:<16} {W * escala}x{H * escala}  {kb(destino)} KB")
