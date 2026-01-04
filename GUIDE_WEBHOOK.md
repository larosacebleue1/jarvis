# Guide du Webhook Jarvis

Ce guide explique comment connecter votre agent Jarvis local à l'API Remote Control pour qu'il exécute automatiquement les commandes envoyées depuis votre portable.

## 🎯 Fonctionnement

```
┌─────────────────┐         ┌──────────────────┐         ┌─────────────────┐
│  Votre Portable │  HTTP   │  API Remote      │  Polling│  Agent Jarvis   │
│  (Interface Web)│────────▶│  Control (Cloud) │◀────────│  (Votre PC)     │
└─────────────────┘         └──────────────────┘         └─────────────────┘
     Envoie des                 Stocke les                 Récupère et
     commandes                  commandes                  exécute
```

1. **Depuis votre portable** : Vous envoyez une commande via l'interface web
2. **API Remote Control** : La commande est stockée en base de données (statut: `pending`)
3. **Webhook Jarvis** : Vérifie régulièrement s'il y a de nouvelles commandes
4. **Agent Jarvis** : Exécute la commande et met à jour le résultat
5. **Vous** : Consultez le résultat dans l'historique de l'interface web

## 📋 Prérequis

- Agent Jarvis installé sur votre PC
- API Remote Control déployée et accessible
- Compte Manus pour l'authentification
- Python 3.8+ avec les dépendances de Jarvis

## 🚀 Installation rapide

### Étape 1 : Obtenir le cookie de session

Le webhook a besoin de votre cookie de session pour s'authentifier auprès de l'API.

```bash
# Afficher les instructions détaillées
python3 get_session_cookie.py
```

**Méthode rapide (Chrome/Firefox) :**

1. Ouvrez l'API dans votre navigateur : `https://votre-api.manus.space`
2. Connectez-vous avec votre compte Manus
3. Appuyez sur **F12** pour ouvrir les outils de développement
4. Allez dans **Application** → **Cookies** → Trouvez `jarvis_session`
5. **Copiez la valeur** du cookie (longue chaîne de caractères)

### Étape 2 : Configurer les variables d'environnement

```bash
# URL de votre API Remote Control
export JARVIS_API_URL="https://3000-xxx.manus.computer"

# Cookie de session (obtenu à l'étape 1)
export JARVIS_SESSION_COOKIE="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
```

### Étape 3 : Lancer le webhook

```bash
cd jarvis-agent

python3 jarvis_webhook.py \
  --api-url "$JARVIS_API_URL" \
  --session-cookie "$JARVIS_SESSION_COOKIE" \
  --interval 5
```

**Paramètres :**
- `--api-url` : URL de l'API Remote Control
- `--session-cookie` : Cookie de session pour l'authentification
- `--interval` : Intervalle de polling en secondes (défaut: 5)

## 📊 Utilisation

Une fois le webhook lancé, vous verrez :

```
🔗 Webhook Jarvis initialisé
   API: https://3000-xxx.manus.computer
   Polling: toutes les 5s
🚀 Webhook Jarvis démarré
En attente de commandes...
```

### Envoyer une commande

1. **Depuis votre portable**, ouvrez l'interface web
2. **Envoyez une commande**, par exemple : "Crée un site web pour mon portfolio"
3. **Le webhook** détecte la nouvelle commande
4. **Jarvis exécute** la commande sur votre PC
5. **Consultez le résultat** dans l'historique de l'interface web

### Logs du webhook

```
📥 1 commande(s) en attente

═══════════════════════════════════════════════════════════
  Exécution de la commande #42
═══════════════════════════════════════════════════════════
Type: build
Commande: Crée un site web pour mon portfolio

[Agent Jarvis exécute la commande...]

✓ Commande #42 terminée avec succès
```

## 🔧 Configuration avancée

### Lancer en arrière-plan

```bash
# Avec nohup
nohup python3 jarvis_webhook.py \
  --api-url "$JARVIS_API_URL" \
  --session-cookie "$JARVIS_SESSION_COOKIE" \
  > webhook.log 2>&1 &

# Avec screen
screen -S jarvis-webhook
python3 jarvis_webhook.py --api-url "$JARVIS_API_URL" --session-cookie "$JARVIS_SESSION_COOKIE"
# Ctrl+A puis D pour détacher

# Avec systemd (service Linux)
# Voir section "Service systemd" ci-dessous
```

### Service systemd (Linux)

Créez `/etc/systemd/system/jarvis-webhook.service` :

```ini
[Unit]
Description=Jarvis Webhook Service
After=network.target

[Service]
Type=simple
User=votre_utilisateur
WorkingDirectory=/home/votre_utilisateur/jarvis-agent
Environment="JARVIS_API_URL=https://votre-api.manus.space"
Environment="JARVIS_SESSION_COOKIE=votre_cookie"
ExecStart=/usr/bin/python3 jarvis_webhook.py --api-url $JARVIS_API_URL --session-cookie $JARVIS_SESSION_COOKIE
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Activez et démarrez le service :

```bash
sudo systemctl daemon-reload
sudo systemctl enable jarvis-webhook
sudo systemctl start jarvis-webhook
sudo systemctl status jarvis-webhook
```

### Ajuster l'intervalle de polling

```bash
# Vérifier toutes les 10 secondes (moins de charge)
python3 jarvis_webhook.py \
  --api-url "$JARVIS_API_URL" \
  --session-cookie "$JARVIS_SESSION_COOKIE" \
  --interval 10

# Vérifier toutes les 2 secondes (plus réactif)
python3 jarvis_webhook.py \
  --api-url "$JARVIS_API_URL" \
  --session-cookie "$JARVIS_SESSION_COOKIE" \
  --interval 2
```

**Recommandations :**
- **5 secondes** : Bon équilibre (défaut)
- **2-3 secondes** : Pour une réactivité maximale
- **10-30 secondes** : Pour économiser les ressources

## 🔐 Sécurité

### Protection du cookie de session

⚠️ **IMPORTANT** : Le cookie de session donne accès complet à votre compte !

**À FAIRE :**
- ✅ Stocker le cookie dans une variable d'environnement
- ✅ Utiliser un fichier `.env` avec permissions restrictives
- ✅ Ne jamais commiter le cookie dans Git
- ✅ Renouveler le cookie régulièrement

**À NE PAS FAIRE :**
- ❌ Écrire le cookie en dur dans un script
- ❌ Partager le cookie avec d'autres personnes
- ❌ Commiter le cookie dans un dépôt public

### Fichier .env (recommandé)

Créez `jarvis-agent/.env` :

```bash
JARVIS_API_URL=https://votre-api.manus.space
JARVIS_SESSION_COOKIE=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

Protégez le fichier :

```bash
chmod 600 .env
```

Ajoutez à `.gitignore` :

```bash
echo ".env" >> .gitignore
```

Utilisez avec le webhook :

```bash
# Charger les variables
source .env

# Lancer le webhook
python3 jarvis_webhook.py \
  --api-url "$JARVIS_API_URL" \
  --session-cookie "$JARVIS_SESSION_COOKIE"
```

### Renouvellement du cookie

Les cookies de session expirent après un certain temps (généralement 7-30 jours).

**Signes d'expiration :**
- Erreurs d'authentification dans les logs
- Commandes qui ne sont plus récupérées
- Erreur HTTP 401 Unauthorized

**Solution :**
1. Reconnectez-vous dans le navigateur
2. Récupérez le nouveau cookie (voir Étape 1)
3. Mettez à jour la variable d'environnement
4. Relancez le webhook

## 🐛 Dépannage

### Le webhook ne récupère pas les commandes

**Vérifications :**

1. **Le webhook est-il lancé ?**
   ```bash
   ps aux | grep jarvis_webhook
   ```

2. **Le cookie est-il valide ?**
   - Reconnectez-vous dans le navigateur
   - Récupérez un nouveau cookie

3. **L'URL de l'API est-elle correcte ?**
   ```bash
   curl "$JARVIS_API_URL/api/trpc/auth.me"
   ```

4. **Les commandes sont-elles bien en statut "pending" ?**
   - Vérifiez dans l'interface web (page Historique)

### Erreur "Command not found"

L'utilisateur du webhook ne correspond pas à l'utilisateur qui a créé la commande.

**Solution :**
- Utilisez le même compte Manus pour :
  1. Envoyer les commandes (interface web)
  2. Authentifier le webhook (cookie de session)

### Le webhook s'arrête après quelques minutes

**Causes possibles :**
- Session SSH fermée → Utilisez `nohup`, `screen`, ou `systemd`
- Cookie expiré → Renouvelez le cookie
- Erreur non gérée → Consultez les logs

### Performances lentes

**Optimisations :**

1. **Réduire l'intervalle de polling** (si vous avez beaucoup de commandes)
2. **Augmenter l'intervalle** (si vous avez peu de commandes)
3. **Vérifier la latence réseau** entre votre PC et l'API

## 📈 Monitoring

### Logs en temps réel

```bash
# Avec tail
tail -f webhook.log

# Avec journalctl (systemd)
sudo journalctl -u jarvis-webhook -f
```

### Statistiques

Le webhook affiche :
- Nombre de commandes récupérées
- Temps d'exécution de chaque commande
- Succès / Échecs

## 🎯 Cas d'usage

### Développement à distance

```
Vous êtes au café → Envoyez "Crée un site web" depuis votre téléphone
→ Jarvis construit le site sur votre PC à la maison
→ Vous consultez le résultat depuis votre téléphone
```

### Maintenance automatique

```
Vous détectez un bug → Envoyez "Répare le bug dans ./mon-projet"
→ Jarvis diagnostique et corrige sur votre PC
→ Vous recevez le rapport de correction
```

### Apprentissage continu

```
Vous apprenez une nouvelle technique → Envoyez "Apprends: Docker Compose"
→ Jarvis enregistre dans sa base de connaissances
→ Il pourra utiliser cette connaissance dans ses futures constructions
```

## 🔄 Alternatives au webhook

Si le webhook ne convient pas à votre cas d'usage, voici d'autres options :

### Option 1 : API directe

Exposez l'agent Jarvis comme une API locale :

```python
# server.py
from fastapi import FastAPI
from jarvis_agent import JarvisAgent

app = FastAPI()
agent = JarvisAgent()

@app.post("/execute")
def execute(command: str, command_type: str):
    if command_type == "build":
        return agent.build(command)
    # ...

# Lancer: uvicorn server:app --host 0.0.0.0 --port 8000
```

### Option 2 : WebSocket

Pour une communication bidirectionnelle en temps réel :

```python
# Utiliser Socket.IO ou WebSocket
# L'API envoie les commandes directement à l'agent
```

### Option 3 : Message Queue

Pour une architecture plus robuste :

```python
# Utiliser RabbitMQ, Redis Pub/Sub, ou Kafka
# L'API publie les commandes, l'agent les consomme
```

## 📚 Ressources

- **Documentation API** : Voir `README.md` dans `jarvis-remote-api/`
- **Architecture Jarvis** : Voir `jarvis_agent_architecture.md`
- **Guide de déploiement** : Voir `GUIDE_DEPLOIEMENT.md`

## 🆘 Support

Si vous rencontrez des problèmes :

1. Consultez les logs : `logs/jarvis-agent.log`
2. Vérifiez l'authentification : `python3 get_session_cookie.py`
3. Testez l'API manuellement : `curl $JARVIS_API_URL/api/trpc/auth.me`

---

**Contrôlez Jarvis depuis n'importe où ! 🚀**

*Version 1.1.0 - Webhook intégré*
