# Prompts para adaptarlo con una IA

Estos prompts están escritos para pegarlos en **Claude Code** (o en cualquier
asistente que pueda leer y escribir ficheros de la carpeta). Si usas un chat
normal sin acceso a ficheros, adjunta o pega `perfil.py` cuando te lo pida.

Copia el bloque entero, cambia lo que va entre `[corchetes]`, y envíalo.

---

## 1 · Rellenar el perfil sin tocar nada a mano

El más útil si te da pereza editar el fichero.

```
Estoy usando este kit de firma de correo. Rellena `perfil.py` con mis datos y
no cambies nada más:

- Nombre: [Nombre Apellido]
- A qué me dedico: [una frase, como se lo contarías a alguien en un bar]
- Puesto tal y como quiero que aparezca: [ej. Product Designer]
- Correo: [tu@correo.com]
- Teléfono: [déjalo vacío si no lo quieres en la firma]
- Ciudad: [Madrid]
- Web: [tuweb.com, o "no tengo"]
- Enlaces para la firma: [LinkedIn: ... / Instagram: ... / GitHub: ...]

Propón tú el antetítulo (la línea pequeña de arriba) a partir de lo que hago:
corto, en mayúsculas, dos o tres palabras. Si no aporta nada, déjalo vacío.

Cuando termines, ejecuta `python3 generar.py` y dime si ha salido algún aviso.
```

---

## 2 · Cambiarle el aspecto

```
Quiero cambiar el aspecto del kit. Mi actividad es [a qué te dedicas] y quiero
que transmita [ej. cercanía y oficio / seriedad técnica / diseño y calma].

Propón DOS alternativas completas de `PALETA` y `FUENTES` en `perfil.py`,
explicando en una línea qué transmite cada una. Reglas:

- Cinco colores como mucho: papel, tinta, acento, metal y apagado.
- El texto sobre el fondo tiene que leerse bien: contraste alto de verdad,
  nada de gris claro sobre gris claro.
- Las tipografías tienen que existir en Google Fonts: una con serifa para el
  nombre y una monoespaciada para los datos.

Genera las dos, hazme una captura de cada banner y las comparo.
```

---

## 3 · Un documento nuevo con la misma identidad

Sirve para un correo distinto, un presupuesto, una tarjeta, una nota de
agradecimiento… lo que sea.

```
Necesito [describe el documento: un correo de seguimiento tras una reunión /
un presupuesto de una página / una tarjeta de agradecimiento].

Contexto: [a quién va dirigido, qué quieres conseguir, qué tono].

Hazlo con la misma identidad visual que el resto del kit: lee `perfil.py` y usa
sus colores y sus tipografías, no inventes otros. Sigue el patrón de
`gen_correo.py`: un script que escribe un HTML en `salida/`, con botón de copiar
y con la firma al pie importada de `gen_firma.py` (no la dupliques).

Si es un correo que se va a enviar:
- Tablas y estilos EN LÍNEA. Nada de flex, nada de grid, nada de bloques
  <style>: Gmail los borra al pegar.
- Anchos y altos explícitos en cualquier <img>.
- Lo que yo tenga que cambiar antes de enviar, entre [corchetes], para que
  salga resaltado en amarillo.
```

---

## 4 · Revisar antes de mandarlo al mundo

```
Repasa lo que has generado antes de que lo use:

1. Abre `salida/firma.html` en el navegador y hazme una captura.
2. Comprueba que TODOS los enlaces existen y responden — uno muerto en la firma
   se repite en cada correo que mande el resto del año.
3. Dime si el correo de la firma es el mismo desde el que voy a enviar. Si no,
   avísame: quien responda irá a la cuenta de envío, no a la de la firma.
4. Mira la portada de LinkedIn y confírmame que ni la foto de perfil ni el
   recorte del móvil se comen nada.
```

---

## Lo que la IA no debería tocar

Si le pides cambios, dile explícitamente que respete esto — son las decisiones
que hacen que funcione fuera del navegador:

- **El banner incrustado en base64.** Si lo convierte en HTML "vivo" con
  degradados y tipografías de Google, en Gmail se rompe.
- **El texto real bajo el banner.** Es lo que se sigue viendo si el destinatario
  bloquea las imágenes.
- **Las zonas muertas de LinkedIn** apuntadas en `gen_linkedin.py`: el avatar y
  los ~228 px que recorta el móvil por cada lado.
- **El botón de copiar con `Range` + `execCommand`.** Es feo y está obsoleto,
  pero funciona abriendo el fichero directamente, sin servidor ni permisos. El
  portapapeles moderno no.
