#!/usr/bin/env python3
"""Genera firma.html: el banner incrustado en base64 + una línea de contacto en
texto real, y una página con el botón de copiar y las instrucciones.

Dos decisiones que parecen detalles y no lo son:

  1. El banner va como IMAGEN INCRUSTADA en base64, no como HTML vivo. Gmail y
     Outlook se comen los degradados, el SVG y las Google Fonts: lo que en el
     navegador es una tarjeta, en el correo sería un churro de texto suelto.

  2. Debajo va TEXTO REAL, no más imagen. Es lo que la imagen no puede dar: se
     puede seleccionar, se puede pinchar, y sigue ahí si el cliente de correo
     bloquea las imágenes (por eso el `alt` del banner lleva nombre y puesto).
"""
import base64
import sys

import perfil as P
from _comun import SALIDA, esc, kb

C = P.PALETA
MONO = "'SF Mono',Menlo,Consolas,'Courier New',monospace"  # del sistema: en el
# correo no se puede confiar en Google Fonts, así que aquí no se usan.
SANS = "-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif"

PNG = SALIDA / "banner@2x.png"
if not PNG.exists():
    sys.exit("  Falta salida/banner@2x.png. Ejecuta antes:  python3 gen_banner.py")

src = "data:image/png;base64," + base64.b64encode(PNG.read_bytes()).decode()


def a(href, txt, color=None, weight="500"):
    return (f'<a href="{href}" style="color:{color or C["acento"]};text-decoration:none;'
            f'font-weight:{weight};">{txt}</a>')


sep = f'<span style="color:{C["metal"]};padding:0 7px;">&#183;</span>'

piezas = [a(f"mailto:{P.CORREO}", esc(P.CORREO))]
if P.TELEFONO:
    piezas.append(a(f'tel:{P.TELEFONO.replace(" ", "")}', esc(P.TELEFONO)))
for e in P.ENLACES:
    if e.get("texto") and e.get("url"):
        piezas.append(a(e["url"], esc(e["texto"]) + " &#8599;"))
if P.CIUDAD:
    piezas.append(f'<span style="color:{C["apagado"]};">{esc(P.CIUDAD)}</span>')

contacto = sep.join(piezas)
alt = esc(f"{P.NOMBRE} {P.APELLIDO} · {P.ROL}")
enlace_banner = P.WEB.get("url") or f"mailto:{P.CORREO}"

# --- La firma. Tablas + estilos EN LÍNEA: es lo único que sobrevive a Gmail y
# --- a Outlook. Nada de flex, nada de grid, nada de bloques <style>: Gmail los
# --- borra enteros al pegar. Y width/height explícitos en el <img>.
firma = f"""<table cellpadding="0" cellspacing="0" border="0" style="border-collapse:collapse;">
  <tr><td style="padding:0;">
    <a href="{enlace_banner}" style="text-decoration:none;"><img
      src="{src}"
      width="600" height="150" alt="{alt}"
      style="display:block;width:600px;max-width:100%;height:auto;border:0;outline:none;"></a>
  </td></tr>
  <tr><td style="padding:9px 2px 0 2px;font-family:{MONO};font-size:12px;line-height:1.7;color:{C["apagado"]};">
    {contacto}
  </td></tr>
</table>"""

pagina = f"""<!doctype html>
<meta charset="utf-8">
<title>Firma de correo &#183; {esc(P.NOMBRE)} {esc(P.APELLIDO)}</title>
<style>
  body{{margin:0;padding:34px 26px;background:#F4F3EF;
       font-family:{SANS};color:{C["tinta"]};}}
  .wrap{{max-width:720px;margin:0 auto;}}
  h1{{font:600 19px/1.3 Georgia,serif;margin:0 0 4px;}}
  .sub{{font-size:13px;color:{C["apagado"]};margin:0 0 22px;}}
  .zona{{background:#fff;border:1px solid #C9C6BC;border-radius:3px;padding:22px;}}
  .btn{{margin:16px 0 0;padding:9px 16px;font:500 13px/1 {SANS};color:#fff;background:{C["acento"]};
        border:0;border-radius:3px;cursor:pointer;}}
  .btn:active{{opacity:.8}}
  .ok{{margin-left:11px;font-size:13px;color:{C["metal"]};opacity:0;transition:opacity .18s}}
  .ok.on{{opacity:1}}
  h2{{font:600 12px/1 {SANS};letter-spacing:.08em;text-transform:uppercase;
      color:{C["apagado"]};margin:30px 0 8px;}}
  ol{{font-size:13.5px;line-height:1.72;color:#3A4245;padding-left:19px;margin:0;}}
  li{{margin-bottom:7px}}
  code{{font:12px {MONO};background:#EAE8E1;padding:1px 5px;border-radius:2px}}
  .nota{{margin-top:26px;padding:13px 15px;border-left:2px solid {C["metal"]};background:#EFEDE6;
         font-size:12.5px;line-height:1.65;color:#434B4E;}}
</style>
<div class="wrap">
  <h1>Firma de correo</h1>
  <p class="sub">Lo de dentro del recuadro es la firma. Todo lo dem&#225;s de esta p&#225;gina no se copia.</p>

  <div class="zona" id="firma">{firma}</div>

  <button class="btn" id="btn">Copiar firma</button><span class="ok" id="ok">copiada</span>

  <h2>Gmail</h2>
  <ol>
    <li>Pulsa <strong>Copiar firma</strong> (o selecciona el recuadro y <code>&#8984;C</code>).</li>
    <li><strong>Configuraci&#243;n &#8594; Ver toda la configuraci&#243;n &#8594; General &#8594; Firma</strong>.</li>
    <li>Crea una firma, pega dentro con <code>&#8984;V</code> y <strong>guarda los cambios</strong> al final de la p&#225;gina.</li>
    <li>Eleg&#237;la en <em>Valores predeterminados</em>: para correos nuevos <em>y</em> para respuestas.</li>
  </ol>

  <h2>Outlook &#183; Apple Mail</h2>
  <ol>
    <li><strong>Outlook:</strong> Configuraci&#243;n &#8594; Correo &#8594; Redactar y responder &#8594; Firma. Pegar y guardar.</li>
    <li><strong>Apple Mail:</strong> Ajustes &#8594; Firmas. Crea una y pega dentro.
        <strong>Desmarca &#171;Coincidir con la fuente del mensaje&#187;</strong> o te destroza el formato.</li>
  </ol>

  <div class="nota">
    <strong>El banner viaja dentro de la firma</strong>, no enlazado desde ning&#250;n sitio: al pegarlo,
    el correo se queda con su propia copia. No depende de ning&#250;n fichero de tu ordenador, as&#237;
    que puedes mover o borrar esta carpeta despu&#233;s.<br><br>
    <strong>Ojo al &#171;Responder a&#187;.</strong> Quien conteste a tu correo no va a la direcci&#243;n
    de la firma: va a la cuenta desde la que env&#237;as. Si son distintas, config&#250;ralo en tu cliente
    (en Gmail: Ajustes &#8594; Cuentas &#8594; <em>Enviar como</em>).
  </div>
</div>
<script>
  // Range + execCommand en vez del portapapeles moderno: funciona abriendo el
  // fichero directamente (file://), sin servidor y sin pedir permisos.
  document.getElementById('btn').onclick = function () {{
    var r = document.createRange(); r.selectNodeContents(document.getElementById('firma'));
    var s = getSelection(); s.removeAllRanges(); s.addRange(r);
    var ok = document.execCommand('copy'); s.removeAllRanges();
    if (ok) {{ var o = document.getElementById('ok'); o.className = 'ok on';
               setTimeout(function () {{ o.className = 'ok'; }}, 1600); }}
  }};
</script>
"""

# `firma` queda expuesta para que gen_correo.py la importe sin duplicarla.
if __name__ == "__main__":
    (SALIDA / "firma.html").write_text(pagina, encoding="utf-8")
    print(f"  firma.html       {kb(SALIDA / 'firma.html')} KB")
