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
- **MP4 / WebM** : 10 à 20 fois plus légers à qualité égale, lus directement par
  le navigateur. À privilégier au-delà de ~2 Mo — les étudiants ouvrent ces
  liens en 4G.
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
- PDF vectoriel aux dimensions exactes : dans le polycopié,
  `\includegraphics{qr/electronics/pont-h.pdf}` sans option donne la bonne
  taille ;
- `--png` ajoute des PNG à 600 dpi.

`qr/MANIFEST.txt` récapitule, pour chaque média, son URL et la ligne
`\includegraphics` correspondante.

Dépendance : `segno` (pur Python), à installer une fois par machine.

## Mémo

Voir [CHEATSHEET.md](CHEATSHEET.md) pour les commandes courantes.
