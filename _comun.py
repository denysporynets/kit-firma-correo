# -*- coding: utf-8 -*-
"""Piezas compartidas por los generadores. Aquí no hay nada que tocar."""
import html
import math
import pathlib
import random
import shutil
import subprocess
import sys

BASE = pathlib.Path(__file__).resolve().parent
SALIDA = BASE / "salida"

# Chrome hace de motor de render: HTML entra, PNG sale. No hay generador de
# imágenes por medio, así que lo que ves en el navegador es exactamente el PNG.
CHROMES = [
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    "/Applications/Chromium.app/Contents/MacOS/Chromium",
    "/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge",
    "/usr/bin/google-chrome",
    "/usr/bin/chromium",
    "/usr/bin/chromium-browser",
]


def chrome():
    for ruta in CHROMES:
        if pathlib.Path(ruta).exists():
            return ruta
    for nombre in ("google-chrome", "chromium", "chrome"):
        hallado = shutil.which(nombre)
        if hallado:
            return hallado
    sys.exit(
        "\n  No encuentro Google Chrome, y hace falta para convertir el diseño en imagen.\n"
        "  Instálalo desde https://www.google.com/chrome/ y vuelve a ejecutarlo.\n"
    )


def esc(texto):
    """Nombres con & o < no deben romper el HTML."""
    return html.escape(str(texto), quote=True)


def captura(fuente_html, destino_png, ancho, alto, escala=1):
    """Renderiza un HTML a PNG con Chrome sin ventana."""
    subprocess.run(
        [chrome(), "--headless", "--disable-gpu", "--hide-scrollbars",
         f"--force-device-scale-factor={escala}",
         f"--window-size={ancho},{alto}",
         "--virtual-time-budget=6000",           # da tiempo a las Google Fonts
         f"--screenshot={destino_png}", str(fuente_html)],
        capture_output=True,
    )
    if not pathlib.Path(destino_png).exists():
        sys.exit(f"  Chrome no ha podido renderizar {fuente_html}.")


def optimiza(png):
    """Baja el peso del PNG sin que se note. Si no hay Pillow, lo deja igual."""
    try:
        from PIL import Image
    except ImportError:
        return
    im = Image.open(png).convert("RGB")
    im.quantize(colors=256, method=Image.MEDIANCUT, dither=Image.NONE).save(
        png, optimize=True)


def kb(ruta):
    return round(pathlib.Path(ruta).stat().st_size / 1024, 1)


# ─── La constelación ─────────────────────────────────────────────────────────
# Los puntos no se dibujan a mano: se siembran con rechazo y se unen por
# cercanía. Cambiar la semilla da otro dibujo con las mismas reglas.

def constelacion(ancho, alto, n, semilla, margen=20, separacion=34,
                 radio=132, grado_max=3, zonas_muertas=(), densidad_derecha=False):
    rnd = random.Random(semilla)
    nodos, intentos = [], 0
    while len(nodos) < n and intentos < n * 400:
        intentos += 1
        x = rnd.uniform(margen, ancho - margen)
        y = rnd.uniform(margen, alto - margen)
        if any(x0 <= x <= x1 and y0 <= y <= y1 for x0, y0, x1, y1 in zonas_muertas):
            continue
        if densidad_derecha and rnd.random() > 0.30 + 0.70 * (x / ancho) ** 1.4:
            continue
        if any((x - a) ** 2 + (y - b) ** 2 < separacion ** 2 for a, b, _ in nodos):
            continue
        nodos.append((x, y, rnd.random()))

    grado = [0] * len(nodos)
    pares = sorted(
        (math.dist(nodos[i][:2], nodos[j][:2]), i, j)
        for i in range(len(nodos)) for j in range(i + 1, len(nodos))
        if math.dist(nodos[i][:2], nodos[j][:2]) < radio
    )
    aristas = []
    for d, i, j in pares:
        if grado[i] < grado_max and grado[j] < grado_max:
            aristas.append((i, j, d / radio))
            grado[i] += 1
            grado[j] += 1
    return nodos, aristas


def svg_constelacion(nodos, aristas, color_linea, color_nodo,
                     r_min=2.0, r_var=4.2, aros=0):
    lineas = "".join(
        f'<line x1="{nodos[i][0]:.1f}" y1="{nodos[i][1]:.1f}" '
        f'x2="{nodos[j][0]:.1f}" y2="{nodos[j][1]:.1f}" '
        f'stroke="{color_linea}" stroke-opacity="{0.30 * (1 - t) + 0.07:.3f}" '
        f'stroke-width="1"/>' for i, j, t in aristas)
    puntos = "".join(
        f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r_min + r * r_var:.2f}" '
        f'fill="{color_nodo}" fill-opacity="{0.42 + r * 0.5:.2f}"/>'
        for x, y, r in nodos)
    # Un aro de instrumento en los nodos más grandes: es lo que hace que lea
    # como carta náutica y no como puntos sueltos.
    grandes = sorted(nodos, key=lambda n: -n[2])[:aros]
    halos = "".join(
        f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r_min * 3 + r * 6:.1f}" fill="none" '
        f'stroke="{color_nodo}" stroke-opacity="0.38" stroke-width="1"/>'
        for x, y, r in grandes)
    return lineas + puntos + halos


def ajusta(tam_max, disponible, texto, factor=0.57, tam_min=11):
    """Encoge el tamaño de letra hasta que el texto quepa en el ancho dado.

    Sin esto, un nombre largo se sale del lienzo y pisa el dibujo o el borde —
    y como el PNG se recorta, no se ve el desastre hasta que ya está subido.
    `factor` es el ancho medio de un carácter en fracción del tamaño de letra:
    ~0.57 en una serif de display, ~0.62 en una monoespaciada.
    """
    n = max(len(texto), 1)
    return max(tam_min, min(tam_max, disponible / (factor * n)))


def fuentes_google(perfil):
    fam = "&".join(
        "family=" + perfil.FUENTES[k].replace(" ", "+") + ":wght@400;500;600"
        for k in ("titulo", "mono"))
    return ('<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
            f'<link href="https://fonts.googleapis.com/css2?{fam}&display=swap" '
            'rel="stylesheet">')
