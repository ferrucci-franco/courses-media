# courses-media

Médias complémentaires aux polycopiés : animations extraites des présentations,
schémas, vidéos courtes. Les étudiants y accèdent en scannant un QR code imprimé
dans le polycopié, qui pointe directement vers le fichier.

**Site public :** https://ferrucci-franco.github.io/courses-media/

## Structure

Un dossier par cours, à plat. Les fichiers vivent directement dedans — pas de
sous-dossiers par année ni par chapitre.

```
courses-media/
├── index.html            # page d'accueil (générée)
├── URLS.txt              # toutes les URLs publiques (généré)
├── electronics/
│   ├── index.html        # galerie du cours (générée)
│   └── pont-h.gif
├── power-electronics/
├── control/
├── acoustics/
├── projets-fil-rouge/
├── qr/                   # un QR code par média, prêt pour le polycopié (généré)
├── update.cmd            # régénère tout et montre l'état git
└── tools/
    ├── make_index.py     # pages du site + URLS.txt
    └── make_qr.py        # QR codes (PDF vectoriel, PNG en option)
```

L'URL d'un fichier est donc :

```
https://ferrucci-franco.github.io/courses-media/<cours>/<fichier>
```

## Règle absolue : une URL publiée ne change jamais

Dès qu'un QR code est imprimé dans un polycopié distribué, l'URL qu'il encode
est gravée dans le marbre — impossible de la corriger a posteriori. Ce dépôt se
gère donc en **ajout seul** : on ajoute des fichiers, on ne les renomme pas et
on ne les déplace pas.

Si un média doit être remplacé par une version différente (autre format, autre
contenu), ajouter un nouveau fichier sous un nouveau nom et laisser l'ancien en
place.

## Conventions de nommage

- Minuscules, tirets comme séparateurs : `pont-h-commutation.gif`
- Pas d'accents, pas d'espaces, pas de caractères spéciaux
- Des noms **sémantiques**, pas positionnels : `pont-h.gif` et non `fig3.gif`
  — le numéro de figure change quand on réordonne les diapositives, le concept
  non.

## Formats et poids

- **GIF** : pratique, mais les exports PowerPoint sont lourds (5–30 Mo).
- **MP4 / WebM** : 10 à 20 fois plus légers à qualité égale. À privilégier
  au-delà de ~2 Mo — les étudiants ouvrent ces liens en 4G.

Une vidéo n'est pas publiée telle quelle : `make_index.py` lui génère une page
d'enrobage `<nom>.html` qui la rejoue en boucle, et c'est cette page que
visent la galerie et le QR code. Ouvert directement, un MP4 affiche un lecteur
qu'il faut démarrer à la main et qui ne boucle pas ; la page restitue le
comportement d'un GIF pour un dixième du poids.

Quand un GIF est converti, les deux fichiers peuvent cohabiter dans le dossier :
la vidéo remplace le GIF, qui n'est alors ni listé ni publié. Ajouter le GIF
à `.gitignore` pour ne pas le pousser par mégarde.
- Limites GitHub : avertissement à 50 Mo, blocage à 100 Mo par fichier.
- **Pas de Git LFS** : les quotas de bande passante s'appliqueraient aux
  téléchargements des étudiants.

Git conserve chaque version de chaque binaire pour toujours. Vérifier un fichier
localement avant de le pousser, plutôt que de pousser cinq corrections
successives.

## Ajouter un fichier

```bash
copy mon-animation.gif electronics\pont-h.gif
update.cmd
git add -A && git commit -m "electronics: animation pont en H" && git push
```

La mise en ligne prend environ une minute.

## Ajouter un cours

Créer le dossier, puis relancer `update.cmd`. Pour un titre affiché différent du
nom de dossier, placer dans le dossier un fichier `.title` contenant le libellé
souhaité.

## QR codes

`update.cmd` appelle `tools/make_qr.py`, qui écrit un QR par média dans
`qr/<cours>/<nom>.pdf` :

- niveau de correction **M** au minimum (relevé à Q ou H quand c'est gratuit) ;
- **18 mm** de côté par défaut — `update.cmd --size 22` pour agrandir ;
- deux formats vectoriels par défaut, tous deux à la taille physique exacte :
  - **`.pdf`** pour le polycopié : `\includegraphics{qr/signals/complexfine.pdf}`
    sans option donne la bonne dimension ;
  - **`.svg`** pour PowerPoint 2021, qui n'importe pas le PDF mais accepte le
    SVG (Insertion > Images) et l'insère à la bonne taille ;
- `--formats pdf,svg,png` ajoute des PNG à 600 dpi pour les outils sans support
  vectoriel.

`qr/MANIFEST.txt` récapitule, pour chaque média, son URL et la ligne
`\includegraphics` correspondante.

Dépendance : `segno` (pur Python), à installer une fois par machine.

## Mémo

Voir [CHEATSHEET.md](CHEATSHEET.md) pour les commandes courantes.
