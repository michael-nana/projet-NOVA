# NOVA

Assistant IA qui pilote un PC Windows depuis un téléphone. Voir `docs/ARCHITECTURE_ET_SUIVI.md` et `docs/DESIGN_SYSTEM.md`.

## Modules de la Phase 1
| Module | Dossier |
|---|---|
| M1 protocol | `packages/protocol` |
| M2 api | `services/api` |
| M3 agent | `services/agent` |
| M4 tools | `services/agent/agent/tools` |

## Installation (PowerShell, à la racine du dépôt)
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -e packages/protocol
pip install -r services/api/requirements.txt -r services/agent/requirements.txt
copy .env.example .env      # puis remplis .env (clé API + 2 secrets)
```

## Lancement (3 terminaux, venv activé dans chacun)
```powershell
cd services\api   ; uvicorn app.main:app          # 1. serveur
cd services\agent ; python -m agent.main          # 2. agent PC
python scripts\send.py                            # 3. état (agent connecté ?)
python scripts\send.py "ouvre le bloc-notes"      # 3. un ordre
```

## Sécurité (déjà en place)
- Serveur lié à 127.0.0.1 par défaut, tokens obligatoires (24 caractères minimum).
- Agent : liste blanche d'applications, dossiers autorisés, aucun shell libre.
- Outils L2/L3 refusés tant que la confirmation téléphone n'existe pas.
- Journal d'audit : `data/audit.jsonl`.

## Notes
- Les outils s'appellent `apps_open`, `files_list`... (l'API Claude refuse les points dans les noms).
- L'authentification actuelle (2 secrets partagés) sera remplacée par l'appairage + passkey (Phase 1, étape 4).
