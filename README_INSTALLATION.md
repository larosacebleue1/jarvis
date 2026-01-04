# 🤖 Jarvis - Agent Intelligent

Jarvis est un agent autonome qui construit des outils informatiques, répare du code, et peut être contrôlé depuis votre portable.

---

## ⚡ Installation en 3 étapes

### Windows

1. **Extraire l'archive** avec 7-Zip
2. **Double-cliquer** sur `install_windows.bat`
3. **Suivre les instructions** à l'écran

### Mac / Linux

```bash
# 1. Extraire l'archive
tar -xzf jarvis-agent-v1.2.0-with-webhook.tar.gz

# 2. Aller dans le dossier
cd jarvis-agent

# 3. Lancer l'installation
./install_unix.sh
```

---

## 🚀 Premier test

```bash
# Windows
python jarvis_agent_cli.py build "Crée une page HTML avec un titre"

# Mac / Linux
python3 jarvis_agent_cli.py build "Crée une page HTML avec un titre"
```

---

## 📱 Contrôle depuis votre portable

1. **Ouvrez l'API Remote Control** dans votre navigateur
2. **Connectez-vous** avec votre compte Manus
3. **Lancez le webhook** sur votre PC :

```bash
# Windows
python jarvis_webhook.py --api-url https://votre-api.manus.space --session-cookie "votre-cookie"

# Mac / Linux
python3 jarvis_webhook.py --api-url https://votre-api.manus.space --session-cookie "votre-cookie"
```

4. **Envoyez des commandes** depuis votre portable !

---

## 📚 Documentation

- **Installation détaillée** : `INSTALLATION_RAPIDE.md`
- **Guide d'utilisation** : `GUIDE_UTILISATION.md`
- **Connexion portable** : `GUIDE_WEBHOOK.md`
- **Déploiement** : `GUIDE_DEPLOIEMENT.md`
- **Architecture** : `jarvis_agent_architecture.md`

---

## 💡 Exemples de commandes

```bash
# Construire un site web
jarvis build "Crée un site web pour mon portfolio"

# Réparer un bug
jarvis fix ./mon-projet "Le serveur ne démarre pas"

# Poser une question
jarvis ask "Comment créer une API REST ?"

# Apprendre quelque chose
jarvis learn "Docker est un outil de conteneurisation"

# Analyser un projet
jarvis analyze ./mon-projet

# Déployer un site
jarvis deploy ./mon-site --method ssh --host serveur.com
```

---

## 🎯 Fonctionnalités

✅ **Construction automatique** de sites web, APIs, outils CLI  
✅ **Réparation de code** avec diagnostic automatique  
✅ **Base de connaissances** évolutive avec recherche sémantique  
✅ **Déploiement** via SSH, Docker, Cloud (Vercel/Netlify), FTP  
✅ **Contrôle à distance** depuis votre portable  
✅ **Webhook** pour exécution automatique des commandes  
✅ **Sauvegardes automatiques** avant modification  
✅ **Journalisation complète** de toutes les actions  

---

## 🔧 Prérequis

- Python 3.8+
- pip
- Clé API OpenAI (ou autre LLM)

---

## 🆘 Besoin d'aide ?

Consultez `INSTALLATION_RAPIDE.md` pour un guide détaillé avec captures d'écran et dépannage.

---

**Jarvis - Votre assistant de développement intelligent 🚀**

*Version 1.2.0 - Avec webhook et déploiement automatique*
