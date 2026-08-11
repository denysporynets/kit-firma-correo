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

## 2 · Cambiarle el aspecto: colores, formas y detalles

`perfil.py` te deja cambiar **colores y tipografías** tú solo. Las **formas**
—el dibujo de la derecha, las escuadras de las esquinas, el degradado del
fondo, la rayita bajo el puesto— están dentro de los generadores, y para eso
está este prompt: la IA sí puede tocarlas.

```
Quiero cambiar el aspecto del kit. Mi actividad es [a qué te dedicas] y quiero
que transmita [ej. cercanía y oficio / seriedad técnica / diseño y calma].

Propón DOS alternativas completas y enséñamelas en imagen para que elija.
De cada una quiero que decidas:

- COLOR: los cinco de `PALETA` (papel, tinta, acento, metal, apagado).
- TIPOGRAFÍA: dos de Google Fonts, una con serifa para el nombre y una
  monoespaciada para los datos.
- EL DIBUJO de la derecha del banner (ahora son puntos unidos, en
  `gen_banner.py`): puede ser otra cosa, o no estar. Si no encaja con lo que
  hago, quítalo y deja respirar el nombre.
- LAS MARCAS de las esquinas: escuadras, un filete alrededor, o nada.
- EL FONDO: degradado o plano.

Reglas:
- Contraste alto de verdad. Nada de gris claro sobre gris claro.
- Las tipografías tienen que existir en Google Fonts.
- Todo lo que sea un ajuste de valor (colores, tipos, tamaños) déjalo en
  `perfil.py`, no repartido por los generadores, para que pueda cambiarlo
  luego sin ti.

Genera las dos, hazme una captura de cada banner y las comparo.
```

### Cómo pedirlo para que salga bien

Cuatro cosas que cambian mucho el resultado:

**Di el efecto, no el CSS.** «Que parezca de un despacho serio pero no
antiguo» funciona mejor que «pon el borde a 2px». Lo segundo lo hace, pero
solo eso; lo primero mueve todo el conjunto.

**Pide dos o tres y míralas.** Describir un diseño con palabras no vale para
elegirlo. Pide siempre que te renderice las variantes y te enseñe las
imágenes; decidir sobre la captura cuesta diez segundos.

**Da una referencia si la tienes.** Una web que te guste, una tarjeta que
tengas, hasta un color de una foto. «Como la web de [X], pero más sobrio» es
una instrucción concreta.

**Di qué NO se toca.** Sin eso, un cambio de aspecto se lleva por delante lo
que hace que la firma funcione en el correo. Está en el último apartado de
este fichero: pásaselo tal cual.

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
