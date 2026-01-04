# 🚀 Installation Rapide de Jarvis

Guide d'installation simple pour installer Jarvis sur votre PC (Windows, Mac, Linux).

---

## 📋 Prérequis

Avant de commencer, assurez-vous d'avoir :

- **Python 3.8 ou supérieur** installé
- **pip** (gestionnaire de paquets Python)
- **Connexion Internet**
- **Clé API OpenAI** (ou autre fournisseur LLM)

### Vérifier Python

Ouvrez un terminal et tapez :

```bash
python --version
# ou
python3 --version
```

Vous devriez voir quelque chose comme `Python 3.11.0`.

Si Python n'est pas installé :
- **Windows** : Téléchargez depuis [python.org](https://www.python.org/downloads/)
- **Mac** : `brew install python3`
- **Linux** : `sudo apt install python3 python3-pip`

---

## 📦 Étape 1 : Télécharger Jarvis

Vous avez reçu l'archive `jarvis-agent-v1.2.0-with-webhook.tar.gz`.

### Windows

1. Téléchargez [7-Zip](https://www.7-zip.org/) si vous ne l'avez pas
2. Clic droit sur l'archive → **7-Zip** → **Extraire ici**
3. Vous obtenez un dossier `jarvis-agent`

### Mac / Linux

```bash
# Aller dans le dossier où vous avez téléchargé l'archive
cd ~/Downloads

# Extraire l'archive
tar -xzf jarvis-agent-v1.2.0-with-webhook.tar.gz

# Vous avez maintenant un dossier jarvis-agent
ls jarvis-agent
```

---

## ⚙️ Étape 2 : Installer les dépendances

### Windows

Ouvrez **PowerShell** ou **CMD** :

```powershell
cd chemin\vers\jarvis-agent
pip install -r requirements.txt
```

### Mac / Linux

Ouvrez le **Terminal** :

```bash
cd ~/Downloads/jarvis-agent
pip3 install -r requirements.txt
```

**Note** : Si vous avez des erreurs de permissions, ajoutez `--user` :

```bash
pip3 install --user -r requirements.txt
```

---

## 🔑 Étape 3 : Configurer la clé API

Jarvis a besoin d'une clé API pour communiquer avec un modèle de langage (LLM).

### Obtenir une clé API OpenAI

1. Allez sur [platform.openai.com](https://platform.openai.com/)
2. Créez un compte (si vous n'en avez pas)
3. Allez dans **API Keys** → **Create new secret key**
4. Copiez la clé (commence par `sk-...`)

### Configurer la clé

#### Windows (PowerShell)

```powershell
$env:OPENAI_API_KEY="sk-votre-clé-ici"
```

#### Mac / Linux (Terminal)

```bash
export OPENAI_API_KEY="sk-votre-clé-ici"
```

**Pour rendre la clé permanente** :

#### Windows

Créez un fichier `.env` dans le dossier `jarvis-agent` :

```
OPENAI_API_KEY=sk-votre-clé-ici
```

#### Mac / Linux

Ajoutez à votre fichier `~/.bashrc` ou `~/.zshrc` :

```bash
echo 'export OPENAI_API_KEY="sk-votre-clé-ici"' >> ~/.bashrc
source ~/.bashrc
```

---

## 🎯 Étape 4 : Tester Jarvis

### Test simple

```bash
# Windows
python jarvis_agent_cli.py info

# Mac / Linux
python3 jarvis_agent_cli.py info
```

Vous devriez voir :

```
╔════════════════════════════════════════════════════════════════════╗
║                    Agent Jarvis - Informations                     ║
╚════════════════════════════════════════════════════════════════════╝

Version: 1.2.0
...
```

### Test de construction

```bash
# Windows
python jarvis_agent_cli.py build "Crée une page HTML simple avec un titre"

# Mac / Linux
python3 jarvis_agent_cli.py build "Crée une page HTML simple avec un titre"
```

Jarvis va créer un dossier avec votre projet !

---

## 🌐 Étape 5 : Connecter à l'API Remote Control (Optionnel)

Si vous voulez contrôler Jarvis depuis votre portable :

### 1. Obtenir votre cookie de session

1. Ouvrez l'API Remote Control dans votre navigateur
2. Connectez-vous avec votre compte Manus
3. Appuyez sur **F12** → **Application** → **Cookies**
4. Trouvez `jarvis_session` et copiez la valeur

### 2. Lancer le webhook

#### Windows

```powershell
$env:JARVIS_API_URL="https://votre-api.manus.space"
$env:JARVIS_SESSION_COOKIE="votre-cookie"

python jarvis_webhook.py --api-url $env:JARVIS_API_URL --session-cookie $env:JARVIS_SESSION_COOKIE
```

#### Mac / Linux

```bash
export JARVIS_API_URL="https://votre-api.manus.space"
export JARVIS_SESSION_COOKIE="votre-cookie"

python3 jarvis_webhook.py \
  --api-url "$JARVIS_API_URL" \
  --session-cookie "$JARVIS_SESSION_COOKIE"
```

Vous verrez :

```
🔗 Webhook Jarvis initialisé
   API: https://votre-api.manus.space
   Polling: toutes les 5s
🚀 Webhook Jarvis démarré
En attente de commandes...
```

Maintenant, envoyez des commandes depuis votre portable et Jarvis les exécutera sur votre PC !

---

## 📱 Utilisation depuis votre portable

1. Ouvrez l'API Remote Control sur votre téléphone
2. Tapez une commande : "Crée un site web pour mon portfolio"
3. Cliquez sur **Envoyer à Jarvis**
4. Le webhook sur votre PC détecte la commande
5. Jarvis l'exécute automatiquement
6. Consultez le résultat dans l'historique

---

## 🛠️ Commandes utiles

### Construire un projet

```bash
python3 jarvis_agent_cli.py build "Crée une API REST en Python avec FastAPI"
```

### Réparer un bug

```bash
python3 jarvis_agent_cli.py fix ./mon-projet "Le serveur ne démarre pas"
```

### Poser une question

```bash
python3 jarvis_agent_cli.py ask "Comment créer une base de données PostgreSQL ?"
```

### Apprendre quelque chose

```bash
python3 jarvis_agent_cli.py learn "Docker Compose est un outil pour définir et exécuter des applications Docker multi-conteneurs"
```

### Analyser un projet

```bash
python3 jarvis_agent_cli.py analyze ./mon-projet
```

### Déployer un site

```bash
python3 jarvis_agent_cli.py deploy ./mon-site --method ssh --host mon-serveur.com --user ubuntu
```

---

## 🔧 Dépannage

### "python: command not found"

Essayez `python3` au lieu de `python`.

### "pip: command not found"

Essayez `pip3` au lieu de `pip`, ou installez pip :

```bash
# Mac
brew install python3

# Linux
sudo apt install python3-pip

# Windows
Réinstallez Python depuis python.org en cochant "Add to PATH"
```

### "ModuleNotFoundError"

Réinstallez les dépendances :

```bash
pip3 install --user -r requirements.txt
```

### "OpenAI API error"

Vérifiez que votre clé API est correcte :

```bash
echo $OPENAI_API_KEY  # Mac/Linux
echo $env:OPENAI_API_KEY  # Windows PowerShell
```

### Le webhook ne récupère pas les commandes

1. Vérifiez que le cookie de session est valide (reconnectez-vous)
2. Vérifiez l'URL de l'API
3. Vérifiez que vous utilisez le même compte Manus

---

## 🎓 Aller plus loin

### Lancer Jarvis en arrière-plan

#### Windows (avec `pythonw`)

```powershell
start pythonw jarvis_webhook.py --api-url $env:JARVIS_API_URL --session-cookie $env:JARVIS_SESSION_COOKIE
```

#### Mac / Linux (avec `nohup`)

```bash
nohup python3 jarvis_webhook.py \
  --api-url "$JARVIS_API_URL" \
  --session-cookie "$JARVIS_SESSION_COOKIE" \
  > webhook.log 2>&1 &
```

Pour arrêter :

```bash
# Trouver le processus
ps aux | grep jarvis_webhook

# Tuer le processus (remplacez PID par le numéro)
kill PID
```

### Créer un raccourci (Windows)

1. Clic droit sur le Bureau → **Nouveau** → **Raccourci**
2. Cible : `C:\Python311\python.exe C:\chemin\vers\jarvis_agent_cli.py`
3. Nom : "Jarvis"

### Créer un alias (Mac/Linux)

Ajoutez à `~/.bashrc` ou `~/.zshrc` :

```bash
alias jarvis="python3 ~/jarvis-agent/jarvis_agent_cli.py"
```

Rechargez :

```bash
source ~/.bashrc
```

Maintenant vous pouvez taper :

```bash
jarvis build "Crée un site web"
```

---

## 📚 Documentation complète

- **Architecture** : `jarvis_agent_architecture.md`
- **Guide d'utilisation** : `GUIDE_UTILISATION.md`
- **Déploiement** : `GUIDE_DEPLOIEMENT.md`
- **Webhook** : `GUIDE_WEBHOOK.md`

---

## 🆘 Besoin d'aide ?

Si vous rencontrez des problèmes :

1. Consultez les logs : `logs/jarvis-agent.log`
2. Vérifiez la configuration : `config/config.yaml`
3. Testez la connexion API : `python3 jarvis_agent_cli.py info`

---

**Jarvis est prêt ! 🚀**

*Contrôlez votre PC depuis n'importe où avec Jarvis*

Version 1.2.0 - Installation rapide
