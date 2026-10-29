# NOVA — Assistant IA de contrôle à distance (PC Windows 11)

> **NOVA** est un nom de code provisoire. Il sera remplacé par le nom définitif du bot (c'est aussi le *wake word* vocal).

| Champ | Valeur |
|---|---|
| Version du document | 0.4 |
| Date de création | 29 octobre 2026 |
| Statut du projet | Phase 0 terminée côté design (maquettes V1 validées), prêt pour la Phase 1 |
| Propriétaire | Toi (projet personnel) |
| Machine cible | PC Windows 11 |
| Clients | Application web (React) + application mobile Android (React Native) |
| Téléphone | Android |
| Stack | React / TypeScript (web + mobile) · Python (backend + agent PC) |

---

## 1. Vision

Un assistant personnel de type « Jarvis » : depuis mon téléphone, partout dans le monde, je parle ou j'écris un ordre, et mon PC l'exécute, **sans que j'aie besoin d'être à côté**. Seule condition : une connexion Internet sur le téléphone et sur le PC.

Exemple : j'ouvre l'app mobile, je dis « NOVA, prépare mon environnement de travail », et le PC ouvre mon IDE, mon navigateur et mes dossiers de projet, puis me confirme sur le téléphone.

### 1.1 Objectifs

- **O1** — Donner des ordres en langage naturel (texte et voix) depuis le mobile et le web.
- **O2** — Exécuter des actions réelles sur le PC (applications, fichiers, système, navigateur, etc.).
- **O3** — Réveiller / démarrer le PC à distance quand il est éteint ou en veille.
- **O4** — Offrir une interface **professionnelle, soignée et personnalisable**.
- **O5** — Garantir une **sécurité forte** (un bot qui contrôle un PC est une cible de choix).
- **O6** — Architecture modulaire : ajouter un nouvel outil = ajouter un fichier.

### 1.2 Hors périmètre (v1)

- Multi-utilisateur / multi-PC (prévu en architecture, pas en v1).
- Contrôle d'autres appareils (domotique, autres PC).
- Publication sur les stores (distribution privée d'abord).

---

## 2. Architecture globale

### 2.1 Principe clé : le PC appelle le serveur, pas l'inverse

Le téléphone et le PC ne se parlent **jamais directement**. Le PC ouvre une connexion **sortante** vers un serveur relais. Aucun port n'est ouvert sur ta box, aucune IP publique n'est nécessaire, et ça fonctionne derrière n'importe quel réseau.

```
┌──────────────┐        HTTPS / WSS         ┌───────────────────┐       WSS (sortant)      ┌──────────────────┐
│  App mobile  │ ─────────────────────────► │  Serveur relais   │ ◄─────────────────────── │   Agent PC       │
│  App web     │ ◄───────────────────────── │  (cloud / VPS)    │ ───────────────────────► │  (Windows 11)    │
└──────────────┘                            └─────────┬─────────┘                          └────────┬─────────┘
                                                      │                                             │
                                                      ▼                                             ▼
                                              ┌───────────────┐                          ┌────────────────────┐
                                              │ API Claude    │                          │ Outils (fichiers,  │
                                              │ (tool use)    │                          │ apps, système...)  │
                                              └───────────────┘                          └────────────────────┘
```

### 2.2 Composants

| # | Composant | Rôle | Technologie proposée |
|---|---|---|---|
| C1 | **App mobile Android** | Interface principale, voix, notifications | React Native (Expo) + TypeScript |
| C2 | **App web** | Scène animée de la chouette + journal, routines, réglages | Next.js + TypeScript + Tailwind |
| C3 | **Serveur relais (backend)** | Auth, routage des ordres, orchestration LLM, historique | Python FastAPI (WebSocket, async) + PostgreSQL + Redis |
| C4 | **Agent PC** | Service Windows qui exécute les outils | Python, installé comme service Windows |
| C5 | **Cerveau IA** | Comprend l'ordre, choisit et enchaîne les outils | API Claude (tool use) |
| C6 | **Voix** | Wake word + reconnaissance vocale + synthèse | Porcupine/openWakeWord + STT + TTS |
| C7 | **Module de réveil** | Allumer le PC éteint | Wake-on-LAN via relais local *ou* prise connectée |

> **Décision actée** : React Native (Expo) pour le mobile et Python pour le backend et l'agent (voir §12, décisions D1, D4, D5). Le web et le mobile partagent les types TypeScript, la logique et les design tokens.

### 2.3 Flux d'un ordre (séquence)

1. L'utilisateur dit « NOVA, ouvre mon dossier Projets » sur le mobile.
2. Le wake word est détecté **localement** dans l'app, puis la parole est transcrite en texte.
3. L'app envoie le texte au serveur via WSS (authentifié).
4. Le serveur envoie le texte + la liste des outils à Claude.
5. Claude répond avec un ou plusieurs **appels d'outils** (ex. `files.open_folder`).
6. Le serveur applique la **politique de permissions** :
   - action sûre → envoyée directement à l'agent PC ;
   - action sensible → **confirmation demandée sur le téléphone** avant envoi.
7. L'agent PC exécute l'outil et renvoie le résultat.
8. Le serveur redonne le résultat à Claude, qui formule la réponse finale.
9. Le téléphone affiche (et lit à voix haute) la réponse. Tout est écrit dans le **journal d'audit**.

---

## 3. Démarrage du PC à distance (O3)

« Dire son nom et que ça démarre tout seul » implique deux niveaux distincts.

### 3.1 Niveau 1 — Le PC est allumé ou en veille

L'agent PC est un **service Windows lancé au démarrage**. Il reste connecté au serveur. Dès qu'un ordre arrive, il agit. En veille, la connexion est coupée : il faut d'abord réveiller le PC.

### 3.2 Niveau 2 — Le PC est éteint ou en veille

Un PC éteint ne peut pas recevoir d'ordre Internet. Il faut un élément **toujours allumé** qui l'allume. Options :

| Option | Principe | Avantages | Inconvénients |
|---|---|---|---|
| **A. Relais local (Raspberry Pi / mini-PC)** | Un petit appareil toujours allumé reçoit l'ordre et envoie un paquet Wake-on-LAN au PC | Fiable, bon marché, extensible | Matériel supplémentaire |
| **B. Prise connectée + BIOS « Restore on AC power »** | Le serveur coupe/rallume la prise, le PC démarre au retour du courant | Très simple | Coupure brutale du courant (à éviter en arrêt normal) |
| **C. Fonction WoL de la box/routeur** | Certaines box exposent un WoL à distance | Pas de matériel | Dépend du modèle, souvent limité |
| **D. Simplement laisser le PC en veille** | WoL local seulement | Zéro matériel | Ne fonctionne pas à distance sans relais |

**Recommandation** : option **A** (relais local), éventuellement combinée à B en secours.
Prérequis PC : activer Wake-on-LAN dans le BIOS/UEFI et dans les propriétés de la carte réseau Windows ; désactiver le « démarrage rapide » si le WoL depuis l'arrêt complet échoue.

---

## 4. Sécurité (priorité n°1)

Un agent capable d'exécuter des actions sur ton PC est l'équivalent d'un accès à distance. La sécurité est une exigence de conception, pas une option.

### 4.1 Authentification et appairage

- Connexion utilisateur : **passkey / biométrie** (Face ID, empreinte) + mot de passe fort en secours + 2FA TOTP.
- **Appairage de l'agent PC** par code à usage unique affiché sur le PC, saisi sur le mobile. L'agent reçoit ensuite un jeton propre à l'appareil, révocable.
- Jetons d'accès courts (15 min) + jetons de rafraîchissement rotatifs.
- Liste des **appareils autorisés** consultable et révocable à tout moment.

### 4.2 Communication

- TLS partout (HTTPS/WSS), certificats gérés automatiquement.
- Messages signés entre serveur et agent (pas d'exécution d'un ordre non signé).
- Option avancée : chiffrement de bout en bout entre mobile et agent.

### 4.3 Niveaux de permission des outils

| Niveau | Nom | Exemples | Comportement |
|---|---|---|---|
| **L0** | Lecture seule | Lister un dossier, état du PC, capture d'écran | Exécution directe |
| **L1** | Action réversible | Ouvrir une app, régler le volume, créer un fichier | Exécution directe |
| **L2** | Action sensible | Supprimer/déplacer des fichiers, installer un logiciel, éteindre | **Confirmation sur le téléphone** |
| **L3** | Action critique | Commande shell libre, modification système, accès aux identifiants | **Confirmation + biométrie** |

### 4.4 Garde-fous

- **Liste blanche d'outils** : au début, pas de shell libre. Chaque capacité est un outil explicite.
- **Dossiers autorisés** : l'agent ne peut toucher que certains chemins (configurables).
- **Bouton d'arrêt d'urgence (kill switch)** sur mobile/web : coupe immédiatement l'agent.
- **Journal d'audit** complet et immuable : qui, quoi, quand, résultat.
- **Limitation de débit** et détection d'anomalies (ordres inhabituels, heures étranges).
- **Protection contre l'injection de prompt** : le contenu lu sur le PC (pages web, fichiers, e-mails) est traité comme des **données**, jamais comme des instructions. Toute action sensible déclenchée après la lecture d'un contenu externe exige une confirmation.
- Clé API Claude **uniquement côté serveur**, jamais dans les apps ni dans l'agent.
- Secrets dans un coffre (variables d'environnement chiffrées / gestionnaire de secrets).

---

## 5. Catalogue d'outils de l'agent PC

Chaque outil = une fonction avec un nom, une description, un schéma d'entrée, un niveau de permission.

| Catégorie | Outils (exemples) | Niveau |
|---|---|---|
| **Système** | `system.status`, `system.volume`, `system.lock`, `system.sleep`, `system.shutdown`, `system.restart` | L0 à L2 |
| **Applications** | `apps.open`, `apps.close`, `apps.list_running`, `apps.focus` | L1 |
| **Fichiers** | `files.list`, `files.read`, `files.create`, `files.move`, `files.delete`, `files.search` | L0 à L2 |
| **Écran** | `screen.screenshot`, `screen.describe` | L0 |
| **Navigateur** | `browser.open_url`, `browser.search`, `browser.automate` | L1 |
| **Média** | `media.play_pause`, `media.next`, `media.volume` | L1 |
| **Presse-papiers** | `clipboard.get`, `clipboard.set` | L0 / L1 |
| **Scénarios** | `routine.run` (ex. « mode travail », « mode nuit ») | selon contenu |
| **Contrôle souris/clavier** | `input.type`, `input.click` | L2 |
| **Shell** | `shell.run` (désactivé par défaut) | L3 |

Les **routines** permettent de chaîner plusieurs outils sous un nom personnalisé, créées depuis l'interface.

---

## 6. Voix (C6)

- **Wake word** détecté **sur l'appareil** (aucun audio envoyé avant le mot-clé). Candidats : Porcupine (mot-clé personnalisé), openWakeWord (open source).
- **Android** : l'écoute en arrière-plan est possible via un **foreground service** (notification permanente visible) et le SDK React Native de Porcupine. Cela demande un *development build* Expo (modules natifs), pas Expo Go.
- **Stratégie en deux temps** : en v1, wake word **quand l'app est ouverte** (« je démarre l'app, je dis son nom ») ; en évolution (Phase 3), écoute en arrière-plan via le foreground service.
- **Points d'attention Android** : consommation de batterie, optimisations constructeur (Xiaomi, Samsung, etc. qui tuent les services), permission micro, indicateur de micro actif imposé par le système.
- **STT** (voix → texte) : service cloud de qualité ou Whisper.
- **TTS** (texte → voix) : voix naturelle, personnalisable (choix de la voix dans les réglages).
- Mode **push-to-talk** en alternative au wake word.

---

## 7. Design UI/UX

### 7.1 Direction artistique

**Premium sombre minimaliste, accent chocolat** (décision D8), avec une **chouette ailée vivante** comme mascotte signature (type mascotte d'app) à la place de l'orbe initial. Le détail complet est dans `DESIGN_SYSTEM.md`.

### 7.2 Design system (tokens)

| Élément | Proposition (modifiable) |
|---|---|
| Thèmes | Sombre (défaut), clair, + thèmes personnalisés |
| Couleur d'accent | Chocolat `#B97A4F` par défaut, personnalisable |
| Typographie | Geist Sans (interface) + Geist Mono (code et logs), détail dans `DESIGN_SYSTEM.md` |
| Formes | Coins arrondis, effets de verre léger (glassmorphism), lueurs discrètes |
| Animations | Chouette animée par machine à états (dort, se réveille, vole, célèbre), transitions 60 fps |
| Icônes | Phosphor (Light / Fill) |
| Accessibilité | Contrastes AA minimum, tailles dynamiques, mode réduit des animations |

### 7.3 Écrans

**Mobile (Android)**
1. Accueil : orbe vocal, état du PC (en ligne / veille / éteint), bouton « Réveiller le PC »
2. Conversation : historique texte + résultats des actions
3. Confirmations : cartes d'approbation pour les actions L2/L3
4. Routines : liste et création
5. Journal d'activité
6. Réglages : voix, thème, appareils, sécurité, wake word

**Web (décision D9)**
- **Scène principale** : la chouette dort sur sa branche ; à l'arrivée d'un ordre elle se réveille, vole dans la fenêtre du PC pour exécuter la tâche, célèbre, puis se rendort. Pas d'interface de chat.
- Navigation discrète : journal d'audit, routines et outils (activer/désactiver), appareils et sessions, réglages, éditeur de thème
- Palette de commandes `Ctrl + K`

### 7.4 Personnalisation

Nom du bot et wake word, voix, couleur d'accent, thème, disposition de l'accueil, raccourcis, routines, ton des réponses.

### 7.5 Outils d'interface

- **Web** : Tailwind CSS, shadcn/ui, Framer Motion.
- **Mobile** : NativeWind (Tailwind sur mobile), Reanimated (animations 60 fps), Rive (chouette animée à états, mobile et web).
- **Partagé** : package `design-tokens` unique (couleurs, polices, espacements) pour garantir une identité identique web et mobile.

### 7.6 Prototypage

Direction artistique d'abord (§7.1 à 7.4 à détailler), puis maquettes Figma **avant** le code, validées écran par écran.

---

## 8. Stack technique (proposition)

| Couche | Choix proposé | Alternative |
|---|---|---|
| Mobile | React Native + Expo (TypeScript), NativeWind, Reanimated, Skia | Flutter |
| Web | Next.js (React), TypeScript, Tailwind, shadcn/ui | SvelteKit |
| Backend | FastAPI (Python), WebSocket, Pydantic ; types TypeScript générés depuis le schéma OpenAPI | Node.js (NestJS) |
| Base de données | PostgreSQL | SQLite en phase de prototype |
| Cache / files | Redis | — |
| Agent PC | Python 3.12 en service Windows (pywin32 / NSSM) | Rust ou C# (.NET) pour plus de robustesse |
| IA | SDK Python Anthropic, API Claude avec tool use | — |
| Hébergement | VPS (Hetzner, OVH, etc.) + Docker Compose | Fly.io, Railway |
| Réseau PC | WSS sortant (aucun port ouvert) | Tailscale en complément |
| CI/CD | GitHub Actions | — |

---

## 9. Structure du dépôt

```
nova/
├── apps/
│   ├── mobile/            # Application mobile
│   └── web/               # Application web
├── services/
│   ├── api/               # Serveur relais + orchestration LLM
│   └── agent/             # Agent PC (service Windows)
│       └── tools/         # Un fichier par catégorie d'outils
├── packages/
│   ├── protocol/          # Schémas de messages partagés (API ⇄ agent ⇄ apps)
│   └── design-tokens/     # Couleurs, polices, espacements partagés
├── infra/                 # Docker, déploiement, scripts
├── docs/
│   ├── ARCHITECTURE_ET_SUIVI.md   # Ce document
│   ├── SECURITY.md
│   └── adr/               # Décisions d'architecture détaillées
└── README.md
```

---

## 10. Feuille de route

Légende : ⬜ à faire · 🟨 en cours · ✅ terminé

### Phase 0 — Cadrage et conception
- ✅ Choix de la stack : React / React Native (Expo) + Python
- ✅ Direction artistique validée : `DESIGN_SYSTEM.md` v0.2
- ✅ Maquettes V1 validées (accueil mobile, scène web animée)
- ⬜ Créer la chouette dans Rive avec sa machine à états
- ⬜ Valider les décisions ouvertes restantes (§12.2)
- ⬜ Choisir le nom définitif et le wake word
- ⬜ Définir le catalogue d'outils v1
- ⬜ Maquettes Figma (mobile + web)
- ⬜ Initialiser le dépôt et la CI

### Phase 1 — Noyau (MVP texte)
- ⬜ Serveur relais : auth, WebSocket, journal d'audit
- ⬜ Agent PC : connexion sortante, appairage, 3 outils (`apps.open`, `files.list`, `screen.screenshot`)
- ⬜ Intégration Claude avec tool use
- ⬜ Interface web minimale : chat + état du PC
- ⬜ Service Windows avec démarrage automatique

### Phase 2 — Application mobile
- ⬜ App mobile : connexion, chat, état du PC
- ⬜ Notifications push + cartes de confirmation (L2/L3)
- ⬜ Biométrie
- ⬜ Kill switch

### Phase 3 — Voix
- ⬜ Push-to-talk, STT, TTS
- ⬜ Wake word dans l'app
- ⬜ Orbe animé et retours visuels

### Phase 4 — Réveil du PC
- ⬜ Configuration WoL (BIOS + Windows)
- ⬜ Relais local (Raspberry Pi / mini-PC) ou prise connectée
- ⬜ Bouton « Réveiller le PC » + détection d'état

### Phase 5 — Richesse fonctionnelle
- ⬜ Catalogue d'outils complet (§5)
- ⬜ Routines personnalisables
- ⬜ Contrôle navigateur / souris / clavier
- ⬜ Personnalisation poussée (thèmes, voix)

### Phase 6 — Durcissement et finition
- ⬜ Audit de sécurité, tests d'intrusion maison, revue des permissions
- ⬜ Tests de charge et de coupure réseau (reconnexion automatique)
- ⬜ Sauvegardes, monitoring, alertes
- ⬜ Documentation utilisateur

---

## 11. Risques

| ID | Risque | Probabilité | Impact | Mitigation |
|---|---|---|---|---|
| R1 | Compromission du compte = contrôle total du PC | Moyenne | Critique | Passkey + 2FA, niveaux de permission, kill switch, audit |
| R2 | Injection de prompt via contenu lu sur le PC | Moyenne | Élevé | Contenu traité comme donnée, confirmation des actions sensibles |
| R3 | L'IA exécute une action destructrice par erreur | Moyenne | Élevé | Pas de shell libre, corbeille plutôt que suppression, confirmations |
| R4 | Wake word en arrière-plan instable sur Android (batterie, constructeurs) | Moyenne | Moyen | Wake word in-app en v1, foreground service ensuite, push-to-talk en repli |
| R5 | WoL peu fiable selon matériel/BIOS | Moyenne | Moyen | Relais local + prise connectée en secours |
| R6 | Latence perçue trop élevée | Moyenne | Moyen | Réponses en streaming, retours visuels immédiats |
| R7 | Coût API et hébergement | Faible | Faible | Limites d'usage, cache, suivi des coûts |
| R8 | Perte de connexion pendant une action | Moyenne | Moyen | Reconnexion automatique, actions idempotentes, état persisté |

---

## 12. Décisions

### 12.1 Décisions prises

| ID | Décision | Date |
|---|---|---|
| D0 | Architecture à relais cloud, agent PC en connexion sortante, sans port ouvert | 2026-10-29 |
| D00 | Interfaces : application web + application mobile (pas de Telegram) | 2026-10-29 |
| D1 | Mobile : **React Native (Expo)** en TypeScript | 2026-10-29 |
| D4 | Backend et agent PC : **Python** (FastAPI) | 2026-10-29 |
| D5 | Plateforme mobile : **Android** uniquement | 2026-10-29 |
| D8 | Direction artistique : **premium sombre minimaliste**, accent **chocolat**, **chouette ailée** comme mascotte | 2026-10-29 |
| D9 | Web : **scène animée** de la chouette (dort, se réveille, vole, célèbre), pas d'interface de chat | 2026-10-29 |
| D10 | Animation des états de la chouette avec **Rive** (production) ; CSS pour les maquettes | 2026-10-29 |
| D11 | **Maquettes V1 validées** (mobile + web) | 2026-10-29 |

### 12.2 Décisions ouvertes (à trancher en Phase 0)

| ID | Question | Options | Recommandation |
|---|---|---|---|
| D2 | Hébergement du serveur | VPS / PaaS / auto-hébergé | VPS + Docker |
| D3 | Méthode de réveil du PC | Relais local / prise connectée | Relais local |
| D6 | Wake word | Porcupine / openWakeWord | Porcupine (SDK React Native, mot-clé personnalisé) |
| D7 | Shell libre (L3) | Désactivé / activé avec garde-fous | Désactivé en v1 |

---

## 13. Journal de suivi

### 13.1 Journal des changements

| Date | Version | Changement |
|---|---|---|
| 2026-10-29 | 0.1 | Création du document : vision, architecture, sécurité, feuille de route |
| 2026-10-29 | 0.4 | Chouette ailée et accent chocolat (D8 révisée), web en scène animée (D9), Rive (D10), maquettes V1 validées (D11), `DESIGN_SYSTEM.md` en v0.2 |
| 2026-10-29 | 0.3 | Direction artistique choisie (D8), création de `DESIGN_SYSTEM.md`, §7 aligné (typographie Geist, icônes Phosphor) |
| 2026-10-29 | 0.2 | Stack actée (React + React Native Expo + Python/FastAPI), plateforme Android, wake word Android via foreground service, décisions D1/D4/D5 déplacées en « prises », risque R4 réévalué, outils UI ajoutés |

### 13.2 Journal de session

| Date | Fait | Prochaine étape |
|---|---|---|
| 2026-10-29 | Cadrage initial, document d'architecture | Valider les décisions ouvertes, choisir le nom, lancer les maquettes |
| 2026-10-29 | Stack validée, document mis à jour en v0.2 | Direction artistique (DA), puis structure du projet et squelette de code |
| 2026-10-29 | DA rédigée (`DESIGN_SYSTEM.md` v0.1), document en v0.3 | Valider DA1 à DA6, puis maquette visuelle et prototype de l'orbe |
| 2026-10-29 | Chouette vivante, deux .md mis à jour, maquettes V1 validées | Phase 1 : serveur relais, agent PC, premier outil de bout en bout |

### 13.3 Points bloquants

_Aucun pour l'instant._

---

## 14. Glossaire

| Terme | Définition |
|---|---|
| **Agent PC** | Programme installé sur le PC qui exécute les actions |
| **Serveur relais** | Serveur cloud qui connecte mobile/web, IA et agent |
| **Tool use** | Mécanisme par lequel le LLM appelle des fonctions que tu définis |
| **Wake word** | Mot déclencheur vocal (le nom du bot) |
| **WoL** | Wake-on-LAN : allumer un PC via un paquet réseau |
| **WSS** | WebSocket sécurisé (connexion bidirectionnelle chiffrée) |
| **Kill switch** | Arrêt d'urgence immédiat de l'agent |
| **Audit log** | Journal horodaté de toutes les actions exécutées |
