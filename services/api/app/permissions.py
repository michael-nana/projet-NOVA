"""Politique de permissions (§4.3 du document d'architecture).

Phase 1 : L0 et L1 s'exécutent directement. L2 et L3 sont REFUSÉS tant que
la confirmation sur téléphone n'existe pas (Phase 2).
"""
AUTO_MAX_LEVEL = 1


def check(level: int) -> tuple[bool, str]:
    if level <= AUTO_MAX_LEVEL:
        return True, ""
    return False, f"Action de niveau L{level} : confirmation requise (pas encore disponible)."
