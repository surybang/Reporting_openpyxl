FROM python:3.12-slim

# Métadonnées de l'image
LABEL maintainer="fabien.hos@lecnam.net"
LABEL description="Application de reporting avec OpenPyXL"
LABEL version="1.0"

# Variables d'environnement pour optimiser Python et uv
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    UV_CACHE_DIR=/tmp/uv-cache \
    UV_LINK_MODE=copy

# Créer un utilisateur non-root pour la sécurité
RUN groupadd --gid 1000 appuser && \
    useradd --uid 1000 --gid appuser --shell /bin/bash --create-home appuser

# Installer les dépendances système nécessaires
RUN apt-get update && apt-get install -y \
    --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Installer uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

# Définir le répertoire de travail
WORKDIR /app

# Changer le propriétaire du répertoire de travail
RUN chown -R appuser:appuser /app

# Passer à l'utilisateur non-root
USER appuser

# Copier les fichiers de dépendances en premier (pour optimiser le cache Docker)
COPY --chown=appuser:appuser pyproject.toml uv.lock* ./

# Copier le reste du code source
COPY --chown=appuser:appuser . .

# Installer les dépendances avec uv
RUN uv sync --frozen --no-dev

# Créer les répertoires nécessaires
RUN mkdir -p example data

# Exposer le port si nécessaire
EXPOSE 8000

# Vérification de santé
HEALTHCHECK --interval=30s --timeout=10s --start-period=30s --retries=3 \
    CMD python -c "import sys; sys.exit(0)"

# Point d'entrée par défaut
ENTRYPOINT ["uv", "run"]

CMD ["main.py"]