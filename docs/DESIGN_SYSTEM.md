# NOVA — Direction artistique et Design System

| Champ | Valeur |
|---|---|
| Version | 0.2 |
| Date | 29 octobre 2026 |
| Direction retenue | **Premium sombre minimaliste, chocolat**, avec une **chouette-mascotte vivante** comme signature |
| Référence projet | `ARCHITECTURE_ET_SUIVI.md` §7 |
| Statut | **Validé pour la V1** (maquettes mobile + web animées) |

---

## 1. Concept

> **« Le calme d'un outil de précision, la présence d'une intelligence. »**

NOVA est une **chouette** : une mascotte ailée, attachante et vivante, comme celle d'une app que l'on a envie d'ouvrir. Autour d'elle, l'interface reste un instrument haut de gamme : noir chaud, très peu d'éléments, une seule couleur d'accent (le chocolat de son plumage). Tout le reste s'efface pour la servir.

### 1.1 Principes

1. **Un seul point focal par écran.** La chouette sur l'accueil et sur le web, la réponse dans le chat, la carte d'action sur une confirmation.
2. **Une seule couleur d'accent.** Elle guide l'œil. Elle ne décore jamais.
3. **Le vide est un matériau.** Grands espaces, peu de bordures, hiérarchie par la taille et l'opacité plutôt que par les cadres.
4. **Le mouvement a un sens.** Chaque animation indique un état (écoute, réflexion, action). Aucune animation gratuite.
5. **La sécurité se voit.** Les actions sensibles ont un traitement visuel distinct, immédiatement reconnaissable.
6. **Le même langage partout.** Web et mobile partagent exactement les mêmes tokens.

### 1.2 Ton visuel

Chaleureux, précis, confiant, avec une pointe d'humour dans la mascotte. Références d'esprit : applications d'outillage haut de gamme (Linear, Raycast, Arc), instrumentation automobile premium.

---

## 2. Couleurs

### 2.1 Neutres (thème sombre, par défaut)

| Token | Valeur | Usage |
|---|---|---|
| `bg.base` | `#0C0908` | Fond de l'application |
| `bg.raised` | `#15100E` | Cartes, panneaux |
| `bg.overlay` | `#1D1714` | Modales, feuilles basses, menus |
| `bg.hover` | `#26201C` | États survol / pressé |
| `border.subtle` | `rgba(255,255,255,0.06)` | Séparateurs discrets |
| `border.default` | `rgba(255,255,255,0.10)` | Contours de cartes |
| `border.strong` | `rgba(255,255,255,0.18)` | Focus, champs actifs |
| `text.primary` | `#F5EFEA` | Titres, texte principal |
| `text.secondary` | `#A8998F` | Texte d'appui |
| `text.tertiary` | `#9A8B80` | Indications, métadonnées |
| `text.disabled` | `#5E524A` | Éléments désactivés |

### 2.2 Accent : Chocolat (décision D8)

Accent par défaut : **Chocolat** `#B97A4F`, la couleur du plumage de la chouette. Il est éclairci par rapport à un brun profond afin de rester lisible sur fond noir (contraste ≈ 5:1 pour le texte `accent.text`).

| Token | Valeur | Usage |
|---|---|---|
| `accent.base` | `#B97A4F` | Boutons principaux, micro, éléments actifs |
| `accent.text` | `#D9A27A` | Texte et puces d'accent sur fond sombre |
| `accent.soft` | `rgba(185,122,79,0.14)` | Fonds de puces, bulles utilisateur |
| `accent.on` | `#1A0F08` | Texte sur fond accent |

Palette de la chouette : corps `#9A6240 → #3E2416` (dégradé), ailes `#6B4128`, aigrettes `#5A3622`, disques faciaux `#E3C4A0`, iris `#E8B25A`, bec `#C98B4A`.

L'accent reste personnalisable (préréglages secondaires : Cyan, Violet, Émeraude, Ambre) ; la chouette garde son plumage chocolat quelle que soit la couleur d'interface choisie.

### 2.3 Sémantique

| Rôle | Valeur |
|---|---|
| Succès | `#3DDC97` |
| Alerte | `#FFB547` |
| Danger | `#FF5C6C` |
| Information | `#6FA8FF` |

> Si l'accent choisi est proche d'une couleur sémantique (émeraude vs succès), l'interface s'appuie aussi sur l'icône et le libellé : **jamais la couleur seule**.

### 2.4 Niveaux de permission (signature de sécurité)

| Niveau | Marqueur | Couleur | Traitement |
|---|---|---|---|
| L0 Lecture | Point | `text.tertiary` | Discret, aucun bandeau |
| L1 Réversible | Point | `accent` | Ligne dans le journal |
| L2 Sensible | Bouclier | `#FFB547` | Carte de confirmation avec liseré ambre |
| L3 Critique | Bouclier plein + clé | `#FF5C6C` | Confirmation plein écran + biométrie |

### 2.5 Thème clair (secondaire)

Fond `#F7F7F8`, cartes `#FFFFFF`, texte `#0B0B0E`, mêmes accents (légèrement assombris pour le contraste). Livré après le thème sombre.

---

## 3. Typographie

| Rôle | Police | Poids | Notes |
|---|---|---|---|
| Titres et interface | **Geist Sans** | 500 / 600 | Moderne, précise, licence libre |
| Texte courant | **Geist Sans** | 400 | |
| Code, chemins, commandes, logs | **Geist Mono** | 400 / 500 | Pour tout ce que l'agent exécute |

Une seule famille donne l'unité visuelle. Repli : `Inter`, puis police système.

### 3.1 Échelle (mobile / web)

| Token | Taille / interligne | Usage |
|---|---|---|
| `display` | 40 / 44 (web 56 / 60) | Écran d'accueil, état principal |
| `title-1` | 28 / 34 | Titre d'écran |
| `title-2` | 22 / 28 | Section |
| `body-lg` | 17 / 26 | Réponses du bot |
| `body` | 15 / 22 | Texte standard |
| `caption` | 13 / 18 | Métadonnées |
| `micro` | 11 / 14, +4 % d'espacement, majuscules | Étiquettes de statut |

---

## 4. Espacement, formes, élévation

- **Grille de base** : 4 px. Espacements : 4, 8, 12, 16, 24, 32, 48, 64.
- **Rayons** : `sm` 8 · `md` 14 · `lg` 20 · `xl` 28 · `full` 999. Les cartes principales en `lg`.
- **Bordures** : 1 px fines, jamais épaisses. La hiérarchie vient du contraste de surface.
- **Élévation** : pas d'ombres lourdes sur fond sombre. On utilise la **luminosité de surface** (`bg.base` → `raised` → `overlay`) et un fin liseré lumineux en haut de chaque carte (`rgba(255,255,255,0.08)`).
- **Verre** : effet flou (`blur 24`) uniquement sur la barre de navigation et les feuilles basses, jamais sur le contenu.
- **Halos** : lueurs d'accent réservées à l'orbe et aux éléments actifs. Pas de halo décoratif.

---

## 5. La chouette NOVA (mascotte signature)

Chouette stylisée, chaleureuse, avec **des ailes** : corps dégradé chocolat, aigrettes, grands yeux ambrés sur disques crème, petit bec. Elle remplace l'orbe initial (décision D8). Son comportement est la partie la plus importante de l'expérience.

### 5.1 États

| État | Comportement | Déclencheur |
|---|---|---|
| **Endormie** | Perchée, yeux fermés, ailes repliées, respiration lente, « Z » flottants | Connecté, inactif |
| **Réveil** | Bâillement, ouverture des yeux, déploiement des ailes | Ordre reçu |
| **Éveillée** | Yeux ouverts, clignements aléatoires, léger balancement | Attente après réveil |
| **Au travail** | Vol dans la machine, ailes battantes, sourcils concentrés | Exécution d'un outil |
| **Écoute** (mobile) | Tête relevée, yeux agrandis, halo réagissant à la voix | Wake word / micro |
| **Parole** (mobile) | Bec et halo pulsant au rythme de la voix | Réponse vocale |
| **Confirmation requise** | Se pose, regard vers l'utilisateur, liseré ambre | Action L2/L3 |
| **Victoire** | Petit saut, yeux souriants (arcs), confettis | Tâche terminée |
| **Erreur** | Yeux écarquillés, secousse, plumes qui se hérissent | Échec d'un outil |
| **Hors ligne** | Silhouette grisée, immobile | PC ou serveur injoignable |

### 5.2 Scène web (écran principal du web, décision D9)

Le web **n'est pas une interface de chat**. C'est une **scène animée** : la chouette dort sur sa branche ; quand un ordre arrive du téléphone, elle se réveille, vole dans la fenêtre du PC pour exécuter la tâche, célèbre, puis retourne se rendormir. Un court texte d'état en bas et un badge d'ordre en haut à droite complètent la scène. Le journal d'audit, les routines et les réglages restent accessibles via une navigation discrète.

### 5.3 Implémentation

- **Animation** : **Rive** (outil utilisé pour les mascottes animées d'apps, états pilotés par une machine à états) pour mobile (`rive-react-native`) et web (`@rive-app/react-canvas`). Les maquettes V1 utilisent des animations CSS pour valider le mouvement.
- **Machine à états** : une entrée par état (§5.1), pilotée par les événements du serveur (ordre reçu, outil en cours, terminé, erreur).
- **Performance** : 60 fps visé, dégradation automatique en économie d'énergie. Option « réduire les animations » : chouette statique avec simple changement de pose.

---

## 6. Mouvement

| Usage | Durée | Courbe |
|---|---|---|
| Micro-interactions (pression, bascule) | 120 ms | ease-out |
| Transitions d'écran | 280 ms | `cubic-bezier(0.22, 1, 0.36, 1)` |
| Feuilles et modales | 340 ms | ressort amorti |
| Apparition des messages | 200 ms + décalage de 40 ms par élément | ease-out |
| Orbe | selon l'état (§5) | continue |

Règles : pas de rebond exagéré, pas d'animation bloquant l'interaction, respect de la préférence système « réduire les animations ».

**Retour haptique (Android)** : léger au toucher des boutons principaux, distinct à la détection du wake word, double impulsion pour une confirmation L2/L3, vibration longue pour une erreur.

---

## 7. Composants

| Composant | Description |
|---|---|
| **Chouette** | Voir §5 |
| **Barre d'état PC** | Pastille (en ligne / veille / éteint) + nom de la machine + latence, en `micro` |
| **Bulle de message** | Utilisateur : fond `accent.soft`, aligné à droite. NOVA : sans fond, texte `body-lg`, aligné à gauche |
| **Carte d'action** | Montre ce que NOVA exécute : icône d'outil, nom lisible, paramètres en Geist Mono, statut (en cours, réussi, échoué) |
| **Carte de confirmation** | Résumé clair de l'action, niveau de permission, boutons « Autoriser » / « Refuser », biométrie pour L3 |
| **Bouton principal** | Fond `accent`, texte `accent.on`, rayon `full`, hauteur 52 |
| **Bouton secondaire** | Fond `bg.raised`, bordure `border.default` |
| **Bouton danger** | Fond `rgba(255,92,108,0.12)`, texte danger |
| **Champ de saisie** | Fond `bg.raised`, focus : bordure `accent` + halo léger |
| **Puce de routine** | Pastille arrondie avec icône et nom (« Mode travail ») |
| **Ligne de journal** | Heure, outil, niveau, résultat ; détail dépliable |
| **Interrupteur / sélecteur** | Piste `bg.hover`, actif en `accent` |
| **Bouton d'arrêt d'urgence** | Toujours accessible depuis l'accueil, traitement rouge discret, confirmation par appui long |
| **Feuille basse** | Verre flou, poignée fine, rayon `xl` |

### 7.1 Icônes

Jeu unique : **Phosphor** (style « Light » pour l'interface, « Fill » pour les états actifs). Trait 1,5 px, cohérent avec la finesse des bordures.

---

## 8. Écrans clés (description de mise en page)

### 8.1 Accueil mobile
- En haut : barre d'état PC (pastille + nom + latence), à droite l'icône de réglages.
- Centre : **la chouette ailée**, grande taille, et sous elle une seule ligne d'état (« Prêt », « Je vous écoute… »).
- Sous l'orbe : dernière réponse ou invitation discrète (« Dites NOVA… »).
- En bas : champ de saisie arrondi, bouton micro, et trois puces de routines favorites.
- Si le PC est éteint : la chouette est endormie et grisée et un bouton principal **« Réveiller le PC »** apparaît.

### 8.2 Conversation
Fil vertical sobre, cartes d'action intégrées aux réponses, cartes de confirmation mises en évidence, saisie ancrée en bas.

### 8.3 Confirmation d'action
Feuille basse : icône de niveau, phrase claire (« NOVA veut supprimer 12 fichiers dans Documents/Projets »), détail technique repliable en Geist Mono, boutons **Refuser** (secondaire) et **Autoriser** (principal). L3 : plein écran et biométrie.

### 8.4 Web : la scène de la chouette
Écran plein : la chouette sur sa branche à gauche, la fenêtre du PC à droite où elle vient travailler, badge d'ordre en haut à droite, barre d'état PC en haut à gauche, texte d'état en bas (« NOVA dort… », « Ordre reçu… », « NOVA est au travail : … », « Tâche terminée »). Palette de commandes `Ctrl + K`, journal et réglages dans une navigation discrète.

---

## 9. Voix et sons

- **Voix de synthèse** : calme, neutre, légèrement grave, vitesse réglable. Choix de la voix dans les réglages.
- **Sons d'interface** : trois sons courts et discrets (réveil détecté, action réussie, erreur), désactivables.
- **Ton des réponses** : concis, précis, sans enthousiasme forcé. Exemple : « Terminé. J'ai ouvert votre dossier Projets. »

---

## 10. Accessibilité

- Contraste AA minimum pour tout texte (`text.secondary` sur `bg.base` : ≈ 7:1).
- Zones tactiles ≥ 48 dp.
- Tailles de texte qui suivent le réglage système.
- Option « réduire les animations » et « contraste renforcé ».
- Aucune information portée par la couleur seule.
- Compatibilité lecteur d'écran (TalkBack) : états de la chouette annoncés par texte.

---

## 11. Tokens partagés (package `design-tokens`)

```ts
// packages/design-tokens/src/tokens.ts
export const colors = {
  bg: { base: '#0C0908', raised: '#15100E', overlay: '#1D1714', hover: '#26201C' },
  text: { primary: '#F5EFEA', secondary: '#A8998F', tertiary: '#9A8B80', disabled: '#5E524A' },
  border: {
    subtle: 'rgba(255,255,255,0.06)',
    default: 'rgba(255,255,255,0.10)',
    strong: 'rgba(255,255,255,0.18)',
  },
  accent: { base: '#B97A4F', text: '#D9A27A', on: '#1A0F08' }, // soft dérivé par code (14 %)
  owl: { body: '#9A6240', wing: '#6B4128', tuft: '#5A3622', face: '#E3C4A0', iris: '#E8B25A', beak: '#C98B4A' },
  semantic: { success: '#3DDC97', warning: '#FFB547', danger: '#FF5C6C', info: '#6FA8FF' },
} as const;

export const radius = { sm: 8, md: 14, lg: 20, xl: 28, full: 999 } as const;
export const space = [0, 4, 8, 12, 16, 24, 32, 48, 64] as const;

export const font = {
  sans: 'Geist, Inter, system-ui, sans-serif',
  mono: 'Geist Mono, ui-monospace, monospace',
} as const;

export const motion = {
  fast: 120,
  base: 280,
  sheet: 340,
  easeOut: [0.22, 1, 0.36, 1],
} as const;
```

Ces tokens alimentent Tailwind (web) et NativeWind (mobile) depuis une source unique.

---

## 12. Décisions de direction artistique

| ID | Décision | Statut |
|---|---|---|
| DA1 | Accent par défaut : **Chocolat** `#B97A4F` | ✅ Validé |
| DA2 | Typographie : Geist Sans + Geist Mono | ✅ Validé |
| DA3 | Icônes : Phosphor | ✅ Validé |
| DA4 | Mascotte : **chouette ailée** (remplace l'orbe) | ✅ Validé |
| DA5 | Bulles : utilisateur teinté, NOVA sans fond | ✅ Validé |
| DA6 | Thème clair livré après le thème sombre | ✅ Validé |
| DA7 | Web : **scène animée** de la chouette, pas de chat | ✅ Validé |
| DA8 | Animation : Rive (production), CSS (maquettes) | ✅ Validé |

---

## 13. Prochaines étapes

1. Maquettes V1 validées (mobile + scène web animée).
2. Figma : déclinaison des écrans restants (conversation, confirmation, routines, journal, réglages).
3. Création de la chouette dans Rive avec sa machine à états (§5.1).
4. Passage à la Phase 1 du projet (noyau serveur + agent).
