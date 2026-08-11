#!/usr/bin/env python3
"""Genera todo de una vez.  Uso:  python3 generar.py"""
import subprocess
import sys

import perfil as P
from _comun import BASE, SALIDA

PASOS = [
    ("gen_banner.py",   "Banner de la firma"),
    ("gen_firma.py",    "Firma para pegar en el correo"),
    ("gen_correo.py",   "Correo de plantilla"),
    ("gen_linkedin.py", "Portada de LinkedIn"),
]

SIN_TOCAR = {"Nombre", "Apellido", "tu@correo.com", "Tu puesto aquí", "tuweb.com"}


def avisa_si_no_lo_ha_tocado():
    puestos = {P.NOMBRE, P.APELLIDO, P.CORREO, P.ROL, P.WEB.get("texto", "")}
    if puestos & SIN_TOCAR:
        print("  Aviso: perfil.py todavía tiene datos de ejemplo sin cambiar.", flush=True)
        print("  Se genera igual, para que veas cómo queda, pero edítalo antes de usarlo.\n", flush=True)


if __name__ == "__main__":
    SALIDA.mkdir(exist_ok=True)
    print()
    avisa_si_no_lo_ha_tocado()

    for script, titulo in PASOS:
        print(f"· {titulo}", flush=True)
        r = subprocess.run([sys.executable, script], cwd=BASE)
        if r.returncode != 0:
            sys.exit(f"\n  Se ha parado en {script}. Mira el error de arriba.\n")

    print(f"\n  Listo. Todo está en:  {SALIDA}")
    print("  Abre salida/firma.html en el navegador y pulsa «Copiar firma».\n")
