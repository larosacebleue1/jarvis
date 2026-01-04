# 🚀 Jarvis - Installation en Une Commande

Installation automatique de Jarvis en une seule ligne de commande !

---

## ⚡ Installation Ultra-Rapide

### 🍎 Mac / 🐧 Linux

Ouvrez un terminal et collez cette commande :

```bash
curl -fsSL https://votre-serveur.com/install_jarvis.sh | bash
```

**Ou avec wget :**

```bash
wget -qO- https://votre-serveur.com/install_jarvis.sh | bash
```

**C'est tout !** L'installeur va :
- ✅ Vérifier Python et pip
- ✅ Télécharger Jarvis
- ✅ Installer les dépendances
- ✅ Configurer la clé API
- ✅ Créer un alias `jarvis`
- ✅ Tester l'installation

---

### 🪟 Windows

Ouvrez **PowerShell en tant qu'administrateur** et collez :

```powershell
iwr -useb https://votre-serveur.com/install_jarvis.ps1 | iex
```

**Ou téléchargez et exécutez :**

```powershell
# Télécharger
Invoke-WebRequest -Uri https://votre-serveur.com/install_jarvis.ps1 -OutFile install_jarvis.ps1

# Exécuter
.\install_jarvis.ps1
```

---

## 📦 Installation Manuelle (Alternative)

Si vous préférez télécharger l'archive manuellement :

### Mac / Linux

```bash
# 1. Télécharger
curl -LO https://votre-serveur.com/jarvis-agent-v1.3.0-final.tar.gz

# 2. Extraire
tar -xzf jarvis-agent-v1.3.0-final.tar.gz

# 3. Installer
cd jarvis-agent
./install_unix.sh
```

### Windows

1. Téléchargez : [jarvis-agent-v1.3.0-final.tar.gz](https://votre-serveur.com/jarvis-agent-v1.3.0-final.tar.gz)
2. Extrayez avec 7-Zip
3. Double-cliquez sur `install_windows.bat`

---

## 🎯 Après l'installation

### Utilisation basique

```bash
# Mac / Linux
jarvis build "Crée un site web pour mon portfolio"

# Windows
jarvis build "Crée un site web pour mon portfolio"
```

### Exemples de commandes

```bash
# Construire un projet
jarvis build "Crée une API REST en Python avec FastAPI"

# Réparer un bug
jarvis fix ./mon-projet "Le serveur ne démarre pas"

# Poser une question
jarvis ask "Comment créer une base de données PostgreSQL ?"

# Apprendre quelque chose
jarvis learn "Docker Compose est un outil pour gérer des conteneurs"

# Analyser un projet
jarvis analyze ./mon-projet

# Déployer un site
jarvis deploy ./mon-site --method ssh --host serveur.com
```

---

## 📱 Contrôle depuis votre portable

Pour contrôler Jarvis depuis votre téléphone :

### 1. Obtenir le cookie de session

1. Ouvrez l'API Remote Control dans votre navigateur
2. Connectez-vous avec Manus
3. F12 → Application → Cookies → `jarvis_session`
4. Copiez la valeur

### 2. Lancer le webhook

```bash
# Mac / Linux
export JARVIS_API_URL="https://votre-api.manus.space"
export JARVIS_SESSION_COOKIE="votre-cookie"

python3 ~/jarvis-agent/jarvis_webhook.py \
  --api-url "$JARVIS_API_URL" \
  --session-cookie "$JARVIS_SESSION_COOKIE"
```

```powershell
# Windows
$env:JARVIS_API_URL="https://votre-api.manus.space"
$env:JARVIS_SESSION_COOKIE="votre-cookie"

python "$env:USERPROFILE\jarvis-agent\jarvis_webhook.py" `
  --api-url $env:JARVIS_API_URL `
  --session-cookie $env:JARVIS_SESSION_COOKIE
```

### 3. Envoyer des commandes

Depuis votre portable, ouvrez l'API Remote Control et envoyez des commandes. Jarvis les exécutera automatiquement sur votre PC !

---

## 🔧 Configuration avancée

### Changer de modèle LLM

Éditez `~/jarvis-agent/config/config.yaml` :

```yaml
llm:
  provider: openai  # ou gemini, claude, etc.
  model: gpt-4
  api_key: ${OPENAI_API_KEY}
```

### Lancer le webhook au démarrage

#### Mac (LaunchAgent)

Créez `~/Library/LaunchAgents/com.jarvis.webhook.plist` :

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.jarvis.webhook</string>
    <key>ProgramArguments</key>
    <array>
        <string>/usr/bin/python3</string>
        <string>/Users/VOTRE_USER/jarvis-agent/jarvis_webhook.py</string>
        <string>--api-url</string>
        <string>https://votre-api.manus.space</string>
        <string>--session-cookie</string>
        <string>VOTRE_COOKIE</string>
    </array>
    <key>RunAtLoad</key>
    <true/>
    <key>KeepAlive</key>
    <true/>
</dict>
</plist>
```

```bash
launchctl load ~/Library/LaunchAgents/com.jarvis.webhook.plist
```

#### Linux (systemd)

Créez `/etc/systemd/system/jarvis-webhook.service` :

```ini
[Unit]
Description=Jarvis Webhook Service
After=network.target

[Service]
Type=simple
User=votre_user
WorkingDirectory=/home/votre_user/jarvis-agent
Environment="JARVIS_API_URL=https://votre-api.manus.space"
Environment="JARVIS_SESSION_COOKIE=votre_cookie"
ExecStart=/usr/bin/python3 jarvis_webhook.py --api-url $JARVIS_API_URL --session-cookie $JARVIS_SESSION_COOKIE
Restart=always

[Install]
WantedBy=multi-user.target
```

```bash
sudo systemctl enable jarvis-webhook
sudo systemctl start jarvis-webhook
```

#### Windows (Tâche planifiée)

1. Ouvrez **Planificateur de tâches**
2. **Créer une tâche** → Général
   - Nom: Jarvis Webhook
   - Exécuter au démarrage
3. **Déclencheurs** → Nouveau
   - À l'ouverture de session
4. **Actions** → Nouveau
   - Programme: `python`
   - Arguments: `"C:\Users\VOTRE_USER\jarvis-agent\jarvis_webhook.py" --api-url "https://votre-api.manus.space" --session-cookie "VOTRE_COOKIE"`

---

## 🛠️ Dépannage

### "curl: command not found" (Mac/Linux)

```bash
# Mac
brew install curl

# Linux
sudo apt install curl
```

### "Python not found" (Windows)

Téléchargez Python depuis [python.org](https://www.python.org/downloads/) et cochez **"Add Python to PATH"**.

### "Execution policy" error (Windows PowerShell)

```powershell
Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned
```

### Le webhook ne se connecte pas

1. Vérifiez que le cookie est valide (reconnectez-vous)
2. Vérifiez l'URL de l'API
3. Vérifiez votre connexion Internet

---

## 📚 Documentation complète

- **Installation détaillée** : `INSTALLATION_RAPIDE.md`
- **Guide d'utilisation** : `GUIDE_UTILISATION.md`
- **Webhook** : `GUIDE_WEBHOOK.md`
- **Déploiement** : `GUIDE_DEPLOIEMENT.md`
- **Architecture** : `jarvis_agent_architecture.md`

---

## 🆘 Support

En cas de problème :

1. Consultez les logs : `~/jarvis-agent/logs/jarvis-agent.log`
2. Testez la configuration : `jarvis info`
3. Vérifiez la clé API : `echo $OPENAI_API_KEY`

---

**Installation en une commande. Contrôle depuis n'importe où. 🚀**

*Jarvis Agent v1.3.0 - Auto-Installer*
