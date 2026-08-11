#!/usr/bin/env python3
"""Genera la portada de LinkedIn: 1584x396.

Lo importante de este fichero no son los colores: son LAS DOS ZONAS MUERTAS,
medidas sobre un perfil real. Casi todas las portadas se estropean aquí.

  · EL AVATAR tapa aproximadamente x 51-400, y 179 hacia abajo. Todo lo que
    pongas en esa esquina se lo come la foto de perfil. Por eso el texto no
    empieza hasta x=445.

  · EL MÓVIL RECORTA unos 228 px por cada lado. Lo que pegues al borde
    izquierdo o derecho desaparece para quien te mire desde el teléfono, que
    son la mayoría. Por eso el texto vertical va metido a right:242px y no a
    right:20px.

Antes de darla por buena: sube la imagen, ábrete el perfil en el móvil y
míralo. Es la única comprobación que vale.
"""
import perfil as P
from _comun import (SALIDA, ajusta, captura, constelacion, esc, fuentes_google,
                    kb, optimiza, svg_constelacion)

W, H = 1584, 396
C = P.PALETA
L = P.LINKEDIN

X_TEXTO = 445                    # pasado el avatar
hay_espina = bool(L["espina"].get("destacado") or L["espina"].get("resto"))

# Hasta dónde puede llegar el texto: si hay texto vertical en el lateral, se
# para antes de chocar con él.
LIMITE = (1225 if not hay_espina else 1105) - X_TEXTO

nombre_completo = f"{P.NOMBRE} {P.APELLIDO}"
tam_nombre = ajusta(80, LIMITE, nombre_completo)
datos_txt = "  ·  ".join(d for d in L["datos"] if d)
tam_datos = ajusta(21, LIMITE, datos_txt, factor=0.62)

# El bloque de texto se declara zona muerta según lo que ocupa DE VERDAD, no
# según una medida fija: si el nombre es corto, los nodos se acercan más.
ancho_texto = max(tam_nombre * 0.57 * len(nombre_completo),
                  tam_datos * 0.62 * len(datos_txt), 200)

# Zonas donde NO puede caer un nodo (x0, y0, x1, y1)
TEXTO = (430, 85, X_TEXTO + ancho_texto + 26, 320)
ESPINA = (1280, 60, 1390, 340)   # el texto vertical del lateral
AVATAR = (20, 150, 420, 396)     # lo tapa la foto de perfil

nodos, aristas = constelacion(
    W, H, L["nodos"], L["semilla"], margen=26, separacion=34, radio=132,
    grado_max=3, zonas_muertas=(TEXTO, ESPINA, AVATAR), densidad_derecha=True)
campo = svg_constelacion(nodos, aristas, C["tinta"], C["metal"],
                         r_min=2.0, r_var=4.2, aros=3)

datos = '<i>&#183;</i>'.join(esc(d) for d in L["datos"] if d)

espina = ""
if L["espina"].get("destacado") or L["espina"].get("resto"):
    espina = (f'<div class="espina"><b>{esc(L["espina"].get("destacado", ""))}</b> '
              f'{esc(L["espina"].get("resto", ""))}</div>')

html = f"""<!doctype html>
<meta charset="utf-8">
{fuentes_google(P)}
<style>
  *{{margin:0;padding:0;box-sizing:border-box}} html,body{{background:#fff}}
  .b{{position:relative;width:{W}px;height:{H}px;overflow:hidden;
      background:linear-gradient(103deg,#E5E4DE 0%,{C["papel"]} 44%,#D6D3C8 100%);}}
  svg.campo{{position:absolute;top:0;left:0;width:{W}px;height:{H}px}}
  .tick{{position:absolute;width:20px;height:20px;border:2px solid {C["metal"]};opacity:.7}}
  .tl{{top:20px;left:20px;border-right:0;border-bottom:0}}
  .tr{{top:20px;right:20px;border-left:0;border-bottom:0}}
  .bl{{bottom:20px;left:20px;border-right:0;border-top:0}}
  .br{{bottom:20px;right:20px;border-left:0;border-top:0}}
  .txt{{position:absolute;left:{X_TEXTO}px;top:112px}}   /* pasado el avatar */
  .nombre{{font-family:'{P.FUENTES["titulo"]}',Georgia,serif;font-weight:600;
           font-size:{tam_nombre:.1f}px;
           line-height:1;letter-spacing:.004em;color:{C["tinta"]};white-space:nowrap}}
  .nombre span{{color:{C["metal"]}}}
  .regla{{width:196px;height:2px;background:{C["metal"]};opacity:.6;margin:26px 0 20px}}
  .datos{{font-family:'{P.FUENTES["mono"]}',monospace;font-weight:500;font-size:{tam_datos:.1f}px;
          color:{C["acento"]};white-space:nowrap}}
  .datos i{{font-style:normal;color:{C["metal"]};padding:0 13px}}
  .espina{{position:absolute;right:242px;top:50%;                /* 242: dentro del recorte móvil */
           transform:translateY(-50%) rotate(180deg);writing-mode:vertical-rl;
           font-family:'{P.FUENTES["mono"]}',monospace;font-weight:500;font-size:16px;
           letter-spacing:.34em;text-transform:uppercase;color:{C["apagado"]};white-space:nowrap}}
  .espina b{{color:{C["acento"]};font-weight:600}}
</style>
<div class="b">
  <svg class="campo" viewBox="0 0 {W} {H}">{campo}</svg>
  <i class="tick tl"></i><i class="tick tr"></i><i class="tick bl"></i><i class="tick br"></i>
  <div class="txt">
    <div class="nombre">{esc(P.NOMBRE)} <span>{esc(P.APELLIDO)}</span></div>
    <div class="regla"></div>
    <div class="datos">{datos}</div>
  </div>
  {espina}
</div>
"""

if __name__ == "__main__":
    SALIDA.mkdir(exist_ok=True)
    fuente = SALIDA / "linkedin.html"
    fuente.write_text(html, encoding="utf-8")

    destino = SALIDA / "linkedin_portada.png"
    captura(fuente, destino, W, H, escala=1)
    optimiza(destino)
    print(f"  linkedin_portada.png  {W}x{H}  {kb(destino)} KB  "
          f"({len(nodos)} nodos, {len(aristas)} enlaces)")
