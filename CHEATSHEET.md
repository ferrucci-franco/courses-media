# Cheatsheet

Referencia rápida de uso. (El resto del repo está en francés porque lo ven los
estudiantes; esto es para vos.)

- **Repo:** https://github.com/ferrucci-franco/courses-media
- **Sitio:** https://ferrucci-franco.github.io/courses-media/
- **Python con `segno`:** `C:\Users\ferrucci\miniforge3\envs\thesys_01\python.exe`

> Ojo: el `python` que está en el PATH de esta máquina es el de WAPT (32 bits) y
> no sirve. Por eso `update.cmd` busca el intérprete correcto solo.

---

## a) Traer el repo a una computadora

```bash
git clone https://github.com/ferrucci-franco/courses-media.git
```

Ejecutalo parado en la carpeta donde querés que quede (acá:
`C:\Users\ferrucci\repos`). Crea el subdirectorio `courses-media` con todo
adentro.

Una vez por máquina, instalar la única dependencia:

```bash
C:\Users\ferrucci\miniforge3\envs\thesys_01\python.exe -m pip install segno
```

Si el repo ya está clonado y querés traer los cambios hechos en otra máquina:

```bash
git pull
```

---

## b) Agregar archivos y publicar

**1. Copiar los archivos** al directorio del curso que corresponda, con el
Explorador o como prefieras:

```
courses-media\electronics\pont-h.gif
```

Nombres en minúscula, con guiones, sin acentos ni espacios.

**2. Regenerar índices y QR codes:**

```bash
.\update.cmd
```

Regenera `index.html`, las galerías, `URLS.txt` y los QR en `qr\`, y al final
muestra qué cambió. Acepta opciones: `.\update.cmd --size 22 --png`.

**3. Revisar y publicar:**

```bash
git add -A && git commit -m "electronics: animation pont en H" && git push
```

El sitio se actualiza en aproximadamente un minuto.

---

## Agregar un curso nuevo

Creá la carpeta dentro de `courses-media\` y, si querés un título distinto del
nombre de carpeta, poné un archivo `.title` adentro con el nombre a mostrar:

```bash
mkdir traitement-signal && echo Traitement du signal > traitement-signal\.title
```

Después, `.\update.cmd` y commit como siempre. No hace falta tocar ningún
script: los cursos se detectan solos.

---

## Situaciones comunes

Ver qué cambió antes de commitear:

```bash
git status --short
```

Descartar un archivo modificado que todavía no commiteaste:

```bash
git restore <archivo>
```

Ver qué archivos nuevos borrarías, sin borrarlos todavía:

```bash
git clean -nd
```

Ver las URLs para los QR (también están en `qr\MANIFEST.txt` junto con la línea
`\includegraphics` lista para pegar):

```bash
cat URLS.txt
```

---

## Regla de oro

**Una URL publicada no se toca nunca más.** Cuando un QR ya está impreso en un
polycopié que repartiste, esa URL no se puede corregir. Este repo se maneja en
modo *agregar solamente*: se suman archivos, no se renombran ni se mueven.

¿Hay que reemplazar un medio? Subí uno nuevo con otro nombre y dejá el viejo
donde está.

---

## Notas sobre los QR

- Nivel de corrección **M** como mínimo (`segno` lo sube a Q o H cuando entra
  sin agrandar el código).
- Tamaño por defecto **18 mm**, que con estas URLs da módulos de 0,40 mm —
  justo en el límite práctico de impresión. Si algún QR cuesta escanearlo,
  `.\update.cmd --size 22`.
- El PDF es vectorial y mide exactamente lo pedido: en LaTeX,
  `\includegraphics{qr/electronics/pont-h.pdf}` sin opciones sale del tamaño
  correcto.
- `--png` agrega PNG a 600 dpi por si algún flujo no acepta PDF.
- Nombres de archivo más cortos = URL más corta = menos módulos = QR más fácil
  de escanear a igual tamaño.
