# -*- coding: utf-8 -*-
"""
===============================================================================
  EL ÚNICO FICHERO QUE TIENES QUE TOCAR
===============================================================================

Cambia lo de aquí abajo, guarda, y ejecuta en la terminal:

    python3 generar.py

Todo lo que se genera aparece en la carpeta `salida/`.

Reglas de la casa:
  · Un campo vacío ("") desaparece del diseño. No deja hueco ni separador suelto.
  · No hace falta que sepas Python. Cambia solo lo que hay entre comillas.
  · Si algo peta, casi siempre es una comilla que te has comido.
"""

# ─────────────────────────────────────────────────────────────────────────────
#  1 · QUIÉN ERES
# ─────────────────────────────────────────────────────────────────────────────

NOMBRE   = "Nombre"          # va en tinta oscura
APELLIDO = "Apellido"        # va en el color de acento
ROL      = "Tu puesto aquí"  # ej. "Product Designer", "Abogado", "Fotógrafo"
CIUDAD   = "Madrid"          # "" para no ponerla

# El antetítulo es la línea pequeña de arriba del todo. Puedes dejarla vacía.
# `destacado` sale en color; `resto` en gris.
ANTETITULO = {"destacado": "", "resto": ""}
# Ejemplo real: {"destacado": "ESTUDIO", "resto": "DE ARQUITECTURA"}


# ─────────────────────────────────────────────────────────────────────────────
#  2 · CÓMO TE ENCUENTRAN
# ─────────────────────────────────────────────────────────────────────────────

CORREO   = "tu@correo.com"
TELEFONO = ""                # "" = no aparece. Formato libre: "+34 600 00 00 00"

# El enlace GRANDE que va dentro del banner. Se ve el texto, se pincha la url.
# Déjalo vacío ({"texto": "", "url": ""}) si no tienes web.
WEB = {"texto": "tuweb.com", "url": "https://tuweb.com"}

# La línea de enlaces de debajo de la firma. Añade o quita los que quieras.
# Ojo: aquí va TEXTO REAL, no imagen — es lo que se sigue viendo si el cliente
# de correo bloquea las imágenes.
ENLACES = [
    {"texto": "LinkedIn",  "url": "https://www.linkedin.com/in/tu-usuario/"},
    # {"texto": "Instagram", "url": "https://instagram.com/tu-usuario"},
    # {"texto": "GitHub",    "url": "https://github.com/tu-usuario"},
]


# ─────────────────────────────────────────────────────────────────────────────
#  3 · CÓMO SE VE
# ─────────────────────────────────────────────────────────────────────────────

# Cinco colores y ya está. Cámbialos por los tuyos si tienes marca.
# Truco: si no sabes por dónde empezar, toca solo ACENTO y deja el resto.
PALETA = {
    "papel":  "#DEDCD5",   # el fondo del banner
    "tinta":  "#20272A",   # el texto principal, casi negro
    "acento": "#A83E1E",   # enlaces y apellido. El color que "manda"
    "metal":  "#9A7420",   # reglas, nodos y marcas de esquina
    "apagado": "#6E7A6F",  # texto secundario
}

# Tipografías de Google Fonts. Se descargan solas al generar la imagen.
# Alternativas que combinan bien: ("Playfair Display", "JetBrains Mono"),
# ("Fraunces", "Space Mono"), ("Lora", "Roboto Mono"), ("Syne", "IBM Plex Mono").
FUENTES = {
    "titulo": "Spectral",       # la del nombre
    "mono":   "IBM Plex Mono",  # la de los datos y los enlaces
}

# El dibujo de la derecha del banner: una constelación de puntos unidos.
# Cambia la semilla y sale otra distinta con las mismas reglas.
MOTIVO = {
    "nodos":   5,
    "semilla": 20260811,
}


# ─────────────────────────────────────────────────────────────────────────────
#  4 · LA PORTADA DE LINKEDIN  (opcional)
# ─────────────────────────────────────────────────────────────────────────────

LINKEDIN = {
    # Los datos que salen bajo tu nombre en la portada. Máximo dos o tres.
    "datos": ["tuweb.com", "tu@correo.com"],
    # El texto vertical del lateral derecho. Vacío = no sale.
    "espina": {"destacado": "", "resto": ""},
    # Cuántos puntos tiene el campo de nodos del fondo.
    "nodos": 70,
    "semilla": 20260811,
}


# ─────────────────────────────────────────────────────────────────────────────
#  5 · EL CORREO DE PLANTILLA  (opcional)
# ─────────────────────────────────────────────────────────────────────────────
#
# Esto genera un correo listo para copiar y pegar, con tu firma al pie.
# Lo que va entre corchetes [así] sale resaltado en amarillo para que no se te
# olvide cambiarlo antes de enviar.

CORREO_PLANTILLA = {
    "titulo": "Correo de presentación",
    "asuntos": [
        "Encantado de saludarte",
        "Un momento para presentarme",
        "Seguimos en contacto",
    ],
    "saludo": "Hola [nombre],",
    "parrafos": [
        "Te escribo en dos líneas para presentarme.",
        "Me dedico a [lo que haces] y he pensado que puede encajar con lo que "
        "estáis montando. Si te viene bien, te lo cuento en diez minutos de "
        "llamada esta semana.",
        "Gracias por el tiempo.",
    ],
    "despedida": "Un saludo,",
}
