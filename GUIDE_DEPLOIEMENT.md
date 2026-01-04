# Guide de Déploiement - Jarvis

Jarvis peut maintenant déployer automatiquement vos projets sur des serveurs ! Ce guide vous explique comment utiliser les 4 méthodes de déploiement disponibles.

## 🚀 Méthodes de déploiement

### 1. SSH/SFTP - Déploiement sur serveur distant

Déployez directement sur votre serveur via SSH et rsync.

**Prérequis :**
- Accès SSH au serveur
- `rsync` installé localement et sur le serveur

**Commande :**
```bash
python3 jarvis_agent_cli.py deploy ./mon-projet --method ssh --config '{
  "host": "example.com",
  "user": "root",
  "key_path": "~/.ssh/id_rsa",
  "remote_path": "/var/www/html",
  "port": 22,
  "post_commands": [
    "systemctl restart nginx",
    "chown -R www-data:www-data /var/www/html"
  ]
}'
```

**Configuration :**
- `host` (requis) : Adresse du serveur
- `user` (requis) : Nom d'utilisateur SSH
- `key_path` (optionnel) : Chemin vers la clé SSH privée
- `remote_path` (optionnel) : Répertoire de destination (défaut: `/var/www/html`)
- `port` (optionnel) : Port SSH (défaut: 22)
- `post_commands` (optionnel) : Commandes à exécuter après le déploiement

**Exemple complet :**
```bash
# Déployer un site web sur un serveur Nginx
python3 jarvis_agent_cli.py deploy ./mon-site-web --method ssh --config '{
  "host": "192.168.1.100",
  "user": "ubuntu",
  "remote_path": "/var/www/mon-site",
  "post_commands": ["sudo systemctl reload nginx"]
}'
```

---

### 2. Docker - Conteneurisation et déploiement

Créez une image Docker et déployez-la sur un serveur ou un registry.

**Prérequis :**
- Docker installé localement
- Accès à un Docker registry (optionnel)

**Commande :**
```bash
python3 jarvis_agent_cli.py deploy ./mon-app --method docker --config '{
  "image_name": "mon-app",
  "tag": "latest",
  "registry": "registry.example.com",
  "host": "server.example.com",
  "user": "root",
  "port_mapping": "80:3000",
  "container_name": "mon-app-prod"
}'
```

**Configuration :**
- `image_name` (optionnel) : Nom de l'image Docker (défaut: `jarvis-app`)
- `tag` (optionnel) : Tag de l'image (défaut: `latest`)
- `registry` (optionnel) : URL du Docker registry pour push
- `host` (optionnel) : Serveur distant pour déploiement automatique
- `user` (optionnel) : Utilisateur SSH pour déploiement distant
- `port_mapping` (optionnel) : Mapping de ports (défaut: `80:80`)
- `container_name` (optionnel) : Nom du container

**Exemple - Build local uniquement :**
```bash
python3 jarvis_agent_cli.py deploy ./mon-api --method docker --config '{
  "image_name": "mon-api",
  "tag": "v1.0"
}'
```

**Exemple - Build + Push vers registry :**
```bash
python3 jarvis_agent_cli.py deploy ./mon-api --method docker --config '{
  "image_name": "mon-api",
  "tag": "v1.0",
  "registry": "docker.io/username"
}'
```

**Exemple - Build + Déploiement distant :**
```bash
python3 jarvis_agent_cli.py deploy ./mon-app --method docker --config '{
  "image_name": "mon-app",
  "host": "production.example.com",
  "user": "deploy",
  "port_mapping": "443:3000"
}'
```

**Note :** Si aucun Dockerfile n'existe, Jarvis en génère un automatiquement selon le type de projet détecté (Node.js, Python, ou site statique).

---

### 3. Cloud - Plateformes managées

Déployez sur Vercel, Netlify ou Heroku en un clic.

**Prérequis :**
- CLI de la plateforme installé et configuré
- Compte sur la plateforme choisie

#### Vercel

```bash
python3 jarvis_agent_cli.py deploy ./mon-site --method cloud --config '{
  "platform": "vercel"
}'
```

**Installation de Vercel CLI :**
```bash
npm i -g vercel
vercel login
```

#### Netlify

```bash
python3 jarvis_agent_cli.py deploy ./mon-site --method cloud --config '{
  "platform": "netlify"
}'
```

**Installation de Netlify CLI :**
```bash
npm i -g netlify-cli
netlify login
```

#### Heroku

```bash
python3 jarvis_agent_cli.py deploy ./mon-app --method cloud --config '{
  "platform": "heroku",
  "app_name": "mon-app-prod"
}'
```

**Installation de Heroku CLI :**
```bash
# Voir: https://devcenter.heroku.com/articles/heroku-cli
heroku login
```

**Configuration :**
- `platform` (requis) : `vercel`, `netlify`, ou `heroku`
- `app_name` (optionnel, Heroku uniquement) : Nom de l'application

---

### 4. FTP/FTPS - Hébergement traditionnel

Uploadez vos fichiers via FTP ou FTPS.

**Commande :**
```bash
python3 jarvis_agent_cli.py deploy ./mon-site --method ftp --config '{
  "host": "ftp.example.com",
  "user": "username",
  "password": "password",
  "remote_path": "/public_html",
  "port": 21,
  "use_tls": true
}'
```

**Configuration :**
- `host` (requis) : Serveur FTP
- `user` (requis) : Nom d'utilisateur FTP
- `password` (requis) : Mot de passe FTP
- `remote_path` (optionnel) : Répertoire distant (défaut: `/`)
- `port` (optionnel) : Port FTP (défaut: 21)
- `use_tls` (optionnel) : Utiliser FTPS (défaut: false)

**Exemple avec FTPS :**
```bash
python3 jarvis_agent_cli.py deploy ./mon-site --method ftp --config '{
  "host": "ftp.monhebergeur.com",
  "user": "moncompte",
  "password": "monmotdepasse",
  "remote_path": "/www",
  "use_tls": true
}'
```

---

## 🔐 Gestion des credentials

### Méthode 1 : Variables d'environnement

Créez un fichier `.env` pour stocker vos credentials :

```bash
# .env
SSH_HOST=example.com
SSH_USER=root
SSH_KEY_PATH=~/.ssh/id_rsa

DOCKER_REGISTRY=registry.example.com

FTP_HOST=ftp.example.com
FTP_USER=username
FTP_PASSWORD=password
```

Puis utilisez-les dans vos commandes :

```bash
python3 jarvis_agent_cli.py deploy ./mon-projet --method ssh --config '{
  "host": "'$SSH_HOST'",
  "user": "'$SSH_USER'",
  "key_path": "'$SSH_KEY_PATH'"
}'
```

### Méthode 2 : Fichier de configuration

Créez un fichier `deploy-config.json` :

```json
{
  "ssh": {
    "host": "example.com",
    "user": "root",
    "key_path": "~/.ssh/id_rsa",
    "remote_path": "/var/www/html"
  },
  "docker": {
    "image_name": "mon-app",
    "registry": "registry.example.com"
  },
  "ftp": {
    "host": "ftp.example.com",
    "user": "username",
    "password": "password",
    "remote_path": "/public_html",
    "use_tls": true
  }
}
```

Puis utilisez-le :

```bash
python3 jarvis_agent_cli.py deploy ./mon-projet --method ssh --config "$(cat deploy-config.json | jq -c .ssh)"
```

---

## 📋 Cas d'usage courants

### Déployer un site statique sur un serveur Nginx

```bash
# 1. Construire le site avec Jarvis
python3 jarvis_agent_cli.py build "Crée un site web pour mon portfolio"

# 2. Déployer sur le serveur
python3 jarvis_agent_cli.py deploy ./projects/portfolio --method ssh --config '{
  "host": "monserveur.com",
  "user": "www-data",
  "remote_path": "/var/www/portfolio",
  "post_commands": ["sudo systemctl reload nginx"]
}'
```

### Déployer une application Node.js avec Docker

```bash
# 1. Construire l'application
python3 jarvis_agent_cli.py build "Crée une API REST avec Express"

# 2. Créer l'image Docker et déployer
python3 jarvis_agent_cli.py deploy ./projects/api --method docker --config '{
  "image_name": "mon-api",
  "host": "production.example.com",
  "port_mapping": "3000:3000"
}'
```

### Déployer sur Vercel pour un prototype rapide

```bash
# 1. Construire le site
python3 jarvis_agent_cli.py build "Crée un site de landing page moderne"

# 2. Déployer sur Vercel
python3 jarvis_agent_cli.py deploy ./projects/landing-page --method cloud --config '{
  "platform": "vercel"
}'
```

### Déployer sur un hébergement mutualisé via FTP

```bash
# 1. Construire le site
python3 jarvis_agent_cli.py build "Crée un site vitrine pour mon entreprise"

# 2. Uploader via FTP
python3 jarvis_agent_cli.py deploy ./projects/site-vitrine --method ftp --config '{
  "host": "ftp.monhebergeur.com",
  "user": "moncompte",
  "password": "motdepasse",
  "remote_path": "/www"
}'
```

---

## 🔄 Workflow complet : Build + Deploy

Vous pouvez enchaîner la construction et le déploiement :

```bash
#!/bin/bash
# deploy-workflow.sh

# 1. Construire le projet
python3 jarvis_agent_cli.py build "Crée un site web moderne pour AMIKAL"

# 2. Déployer automatiquement
python3 jarvis_agent_cli.py deploy ./projects/amikal-site --method ssh --config '{
  "host": "amikal.example.com",
  "user": "deploy",
  "remote_path": "/var/www/amikal"
}'

echo "✓ Projet construit et déployé avec succès !"
```

---

## 🛠️ Dépannage

### Erreur SSH : Permission denied

**Problème :** Clé SSH non acceptée

**Solution :**
```bash
# Vérifier les permissions de la clé
chmod 600 ~/.ssh/id_rsa

# Ajouter la clé au serveur
ssh-copy-id user@host
```

### Erreur Docker : Cannot connect to Docker daemon

**Problème :** Docker n'est pas démarré

**Solution :**
```bash
# Démarrer Docker
sudo systemctl start docker

# Ajouter votre utilisateur au groupe docker
sudo usermod -aG docker $USER
```

### Erreur FTP : Connection refused

**Problème :** Port FTP bloqué ou mauvais port

**Solution :**
```bash
# Vérifier le port FTP (souvent 21 ou 22)
# Essayer avec use_tls: true si le serveur supporte FTPS
```

### Erreur Cloud : CLI not authenticated

**Problème :** Non connecté à la plateforme

**Solution :**
```bash
# Vercel
vercel login

# Netlify
netlify login

# Heroku
heroku login
```

---

## 📊 Comparaison des méthodes

| Méthode | Vitesse | Facilité | Flexibilité | Coût | Cas d'usage |
|---------|---------|----------|-------------|------|-------------|
| **SSH** | ⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | Gratuit | Serveurs dédiés/VPS |
| **Docker** | ⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | Gratuit | Applications complexes |
| **Cloud** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | Freemium | Prototypes, sites statiques |
| **FTP** | ⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐ | Gratuit | Hébergement mutualisé |

---

## 💡 Conseils

1. **Testez localement** avant de déployer en production
2. **Utilisez des variables d'environnement** pour les credentials sensibles
3. **Créez des sauvegardes** avant chaque déploiement
4. **Utilisez Docker** pour garantir la reproductibilité
5. **Automatisez** avec des scripts pour les déploiements fréquents

---

## 🚀 Prochaines étapes

- Configurer un CI/CD avec GitHub Actions
- Mettre en place des rollbacks automatiques
- Ajouter des health checks post-déploiement
- Configurer des domaines personnalisés

---

**Jarvis peut maintenant gérer tout le cycle de vie de vos projets, de la construction au déploiement !** 🎉
