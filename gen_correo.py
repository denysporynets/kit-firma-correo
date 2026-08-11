#!/usr/bin/env python3
"""Genera correo.html: un correo listo para copiar, con la firma al pie.

Reutiliza la firma de gen_firma.py — no la duplica. Si cambias la firma, este
correo cambia solo.
"""
import re

import perfil as P
from _comun import SALIDA, esc, kb
from gen_firma import MONO, SANS, firma

C = P.PALETA
T = P.CORREO_PLANTILLA
SERIF = "Georgia,'Times New Roman',serif"
PAR = (f'style="margin:0 0 15px;font-family:{SERIF};font-size:15px;'
       f'line-height:1.65;color:{C["tinta"]};"')


def marca(texto):
    """Lo que va entre [corchetes] sale resaltado: es lo que hay que cambiar."""
    return re.sub(r"\[([^\]]+)\]",
                  r'<span style="background:#F6E9C9;padding:0 3px;">[\1]</span>',
                  esc(texto))


parrafos = "".join(f"<p {PAR}>{marca(t)}</p>" for t in T["parrafos"])

cuerpo = f"""<div style="font-family:{SERIF};font-size:15px;line-height:1.65;color:{C["tinta"]};">
  <p {PAR}>{marca(T["saludo"])}</p>
  {parrafos}
  <p style="margin:0 0 26px;font-family:{SERIF};font-size:15px;line-height:1.65;color:{C["tinta"]};">
  {marca(T["despedida"])}<br>{esc(P.NOMBRE)} {esc(P.APELLIDO)}</p>
  {firma}
</div>"""

asuntos = "".join(
    f'<div class="asunto"><code>{esc(s)}</code>'
    f'<button class="mini" data-text="{esc(s)}">copiar</button></div>'
    for s in T["asuntos"])

pagina = f"""<!doctype html>
<meta charset="utf-8">
<title>{esc(T["titulo"])} &#183; {esc(P.NOMBRE)} {esc(P.APELLIDO)}</title>
<style>
  body{{margin:0;padding:34px 26px;background:#F4F3EF;
       font-family:{SANS};color:{C["tinta"]};}}
  .wrap{{max-width:720px;margin:0 auto;}}
  h1{{font:600 19px/1.3 Georgia,serif;margin:0 0 4px;}}
  .sub{{font-size:13px;color:{C["apagado"]};margin:0 0 6px;}}
  h2{{font:600 13px/1 {SANS};letter-spacing:.07em;text-transform:uppercase;
      color:{C["apagado"]};margin:32px 0 10px;}}
  .zona{{background:#fff;border:1px solid #C9C6BC;border-radius:3px;padding:24px;}}
  .btn{{margin:12px 0 0;padding:8px 15px;font:500 13px/1 {SANS};color:#fff;background:{C["acento"]};
        border:0;border-radius:3px;cursor:pointer;}}
  .btn:active{{opacity:.8}}
  .ok{{margin-left:10px;font-size:13px;color:{C["metal"]};opacity:0;transition:opacity .18s}}
  .ok.on{{opacity:1}}
  .asunto{{display:flex;align-items:center;gap:12px;background:#fff;border:1px solid #C9C6BC;
           border-radius:3px;padding:11px 14px;margin-bottom:7px;}}
  .asunto code{{flex:1;font:13.5px {MONO};color:{C["tinta"]};}}
  .mini{{font:500 11.5px/1 {SANS};color:{C["acento"]};background:none;border:1px solid #C9C6BC;
         border-radius:3px;padding:5px 9px;cursor:pointer;}}
  .nota-inline{{font-size:12.5px;color:{C["apagado"]};margin:0 0 10px;}}
  .nota{{margin-top:30px;padding:13px 15px;border-left:2px solid {C["metal"]};background:#EFEDE6;
         font-size:12.5px;line-height:1.65;color:#434B4E;}}
  mark{{background:#F6E9C9;padding:0 3px}}
</style>
<div class="wrap">
  <h1>{esc(T["titulo"])}</h1>
  <p class="sub">Elige asunto, copia el mensaje y p&#233;galo en tu correo. La firma va incluida.</p>

  <h2>Asunto &#8212; elige uno</h2>
  {asuntos}

  <h2>Mensaje</h2>
  <p class="nota-inline">Se copia con la firma dentro.
     <strong>Cambia lo resaltado en <mark>[amarillo]</mark> antes de enviar</strong>
     &#8212; est&#225; marcado justo para que no se te pase.</p>
  <div class="zona" id="cuerpo">{cuerpo}</div>
  <button class="btn" data-target="cuerpo">Copiar mensaje</button><span class="ok">copiado</span>

  <div class="nota">
    <strong>Es un correo de uno a uno, no un env&#237;o masivo.</strong> Si se lo mandas a varias
    personas, ponlas en <strong>CCO</strong> o m&#225;ndalo de una en una: un &#171;Para&#187; con
    veinte direcciones deja los contactos de todos a la vista, y con contactos profesionales eso se
    nota.<br><br>
    <strong>Si escribes en otro idioma, no traduzcas literal.</strong> &#171;Felices vacaciones&#187;
    en agosto no es <em>happy holidays</em> (en ingl&#233;s eso suena a Navidad), sino
    <em>summer break</em>. Las f&#243;rmulas de cortes&#237;a no caen en el mismo mes en cada idioma.
  </div>
</div>
<script>
  document.querySelectorAll('.btn').forEach(function (b) {{
    b.onclick = function () {{
      var r = document.createRange();
      r.selectNodeContents(document.getElementById(b.dataset.target));
      var s = getSelection(); s.removeAllRanges(); s.addRange(r);
      if (document.execCommand('copy')) {{
        var o = b.nextElementSibling;
        o.className = 'ok on'; setTimeout(function () {{ o.className = 'ok'; }}, 1500);
      }}
      s.removeAllRanges();
    }};
  }});
  document.querySelectorAll('.mini').forEach(function (b) {{
    b.onclick = function () {{
      navigator.clipboard.writeText(b.dataset.text).then(function () {{
        var t = b.textContent; b.textContent = 'copiado';
        setTimeout(function () {{ b.textContent = t; }}, 1500);
      }});
    }};
  }});
</script>
"""

if __name__ == "__main__":
    (SALIDA / "correo.html").write_text(pagina, encoding="utf-8")
    print(f"  correo.html      {kb(SALIDA / 'correo.html')} KB")
