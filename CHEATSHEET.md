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
git clone https://github.com/ferrucci-franco/courses-media.git C:\Users\ferrucci\repos\courses-media
```

El destino va explícito a propósito: si corrés `git clone` sin él estando ya
**dentro** del repo, te crea un clon anidado (`courses-media\courses-media\`)
que no sirve para nada y ensucia el `git add`. Si te pasa, borralo y listo — no
tiene nada propio adentro.

Para saber dónde estás parado:

```bash
pwd
```

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

## Convertir un GIF pesado a MP4

Arriba de ~2 Mo conviene convertir: pesa 10× menos y se ve igual.

```bash
C:\Users\ferrucci\miniforge3\envs\thesys_01\Library\bin\ffmpeg.exe -i signals\animacion.gif -vf "scale=trunc(iw/2)*2:trunc(ih/2)*2" -c:v libx264 -preset slow -crf 20 -pix_fmt yuv420p -movflags +faststart -an signals\animacion.mp4
```

Si tenés el entorno `thesys_01` activado, alcanza con `ffmpeg` a secas.

Qué hace cada parte: `scale=trunc(...)` fuerza dimensiones pares (H.264 las
exige), `crf 20` da calidad alta para diagramas con texto fino, `faststart`
permite empezar a ver el video antes de que termine de bajar, `-an` descarta el
audio inexistente.

Después:

1. Agregá el `.gif` a `.gitignore` — la versión MP4 lo reemplaza y no hace falta
   publicar las dos.
2. `.\update.cmd`

`make_index.py` detecta que hay video y genera una página `animacion.html` que
lo reproduce **en bucle y sin tocar nada**, igual que un GIF. Esa página es la
que apuntan la galería y el QR: un `.mp4` abierto directo muestra un reproductor
detenido que hay que arrancar a mano y se reproduce una sola vez.

`ffmpeg` está instalado en el entorno `thesys_01`, junto con `segno`.

## Regla de oro

**Una URL publicada no se toca nunca más.** Cuando un QR ya está impreso en un
polycopié que repartiste, esa URL no se puede corregir. Este repo se maneja en
modo *agregar solamente*: se suman archivos, no se renombran ni se mueven.

¿Hay que reemplazar un medio? Subí uno nuevo con otro nombre y dejá el viejo
donde está.

---

## Notas sobre los QR

Por defecto se generan **dos formatos vectoriales**, ambos con el tamaño físico
exacto:

| Formato | Para qué | Cómo se usa |
|---|---|---|
| `.pdf` | Polycopié (LaTeX) | `\includegraphics{qr/signals/complexfine.pdf}` sin opciones |
| `.svg` | PowerPoint 2021 | Insertar → Imágenes → seleccionar el `.svg` |
| `.png` | Recurso de emergencia | `.\update.cmd --formats pdf,svg,png` |

PowerPoint 2021 no importa PDF, pero sí SVG — y al ser vectorial se ve nítido
proyectado y al imprimir. El SVG lleva `width="18mm"`, así que entra a la
dimensión correcta sin que tengas que redimensionarlo a mano.

Otros detalles:

- Nivel de corrección **M** como mínimo (`segno` lo sube a Q o H cuando entra
  sin agrandar el código).
- Tamaño por defecto **18 mm**, que con estas URLs da módulos de 0,40 mm —
  justo en el límite práctico de impresión. Si alguno cuesta escanearlo,
  `.\update.cmd --size 22`.
- Nombres de archivo más cortos = URL más corta = menos módulos = QR más fácil
  de escanear a igual tamaño.
