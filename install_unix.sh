#!/bin/bash

echo "========================================"
echo "  Installation de Jarvis pour Mac/Linux"
echo "========================================"
echo ""

# Vérifier Python
if ! command -v python3 &> /dev/null; then
    echo "[ERREUR] Python 3 n'est pas installé"
    echo ""
    echo "Installation:"
    echo "  - Mac: brew install python3"
    echo "  - Ubuntu/Debian: sudo apt install python3 python3-pip"
    echo "  - Fedora: sudo dnf install python3 python3-pip"
    exit 1
fi

echo "[OK] Python est installé"
python3 --version
echo ""

# Vérifier pip
if ! command -v pip3 &> /dev/null; then
    echo "[ERREUR] pip3 n'est pas installé"
    echo ""
    echo "Installation:"
    echo "  - Mac: brew install python3"
    echo "  - Ubuntu/Debian: sudo apt install python3-pip"
    echo "  - Fedora: sudo dnf install python3-pip"
    exit 1
fi

echo "[OK] pip3 est installé"
pip3 --version
echo ""

# Installer les dépendances
echo "Installation des dépendances..."
pip3 install --user -r requirements.txt

if [ $? -ne 0 ]; then
    echo "[ERREUR] Échec de l'installation des dépendances"
    exit 1
fi

echo ""
echo "[OK] Dépendances installées avec succès"
echo ""

# Demander la clé API
echo "========================================"
echo "  Configuration de la clé API"
echo "========================================"
echo ""
echo "Vous avez besoin d'une clé API OpenAI pour utiliser Jarvis."
echo ""
echo "Si vous n'en avez pas encore:"
echo "1. Allez sur https://platform.openai.com/"
echo "2. Créez un compte"
echo "3. Allez dans API Keys"
echo "4. Créez une nouvelle clé"
echo ""
read -p "Entrez votre clé API OpenAI (sk-...): " API_KEY

if [ -z "$API_KEY" ]; then
    echo "[ERREUR] Clé API vide"
    exit 1
fi

# Créer le fichier .env
echo "OPENAI_API_KEY=$API_KEY" > .env
chmod 600 .env

echo ""
echo "[OK] Clé API sauvegardée dans .env"
echo ""

# Ajouter au .bashrc ou .zshrc
SHELL_RC=""
if [ -f "$HOME/.zshrc" ]; then
    SHELL_RC="$HOME/.zshrc"
elif [ -f "$HOME/.bashrc" ]; then
    SHELL_RC="$HOME/.bashrc"
fi

if [ -n "$SHELL_RC" ]; then
    read -p "Voulez-vous ajouter un alias 'jarvis' à votre shell? (o/n): " ADD_ALIAS
    if [ "$ADD_ALIAS" = "o" ] || [ "$ADD_ALIAS" = "O" ]; then
        JARVIS_PATH="$(pwd)/jarvis_agent_cli.py"
        echo "" >> "$SHELL_RC"
        echo "# Jarvis Agent" >> "$SHELL_RC"
        echo "alias jarvis='python3 $JARVIS_PATH'" >> "$SHELL_RC"
        echo "export OPENAI_API_KEY='$API_KEY'" >> "$SHELL_RC"
        echo ""
        echo "[OK] Alias ajouté à $SHELL_RC"
        echo "Rechargez votre shell avec: source $SHELL_RC"
    fi
fi

# Tester l'installation
echo ""
echo "========================================"
echo "  Test de l'installation"
echo "========================================"
echo ""

export OPENAI_API_KEY="$API_KEY"
python3 jarvis_agent_cli.py info

if [ $? -ne 0 ]; then
    echo "[ERREUR] Le test a échoué"
    exit 1
fi

echo ""
echo "========================================"
echo "  Installation terminée avec succès !"
echo "========================================"
echo ""
echo "Pour utiliser Jarvis, tapez:"
echo "  python3 jarvis_agent_cli.py build \"Votre commande\""
echo ""
if [ -n "$SHELL_RC" ] && [ "$ADD_ALIAS" = "o" ]; then
    echo "Ou simplement (après avoir rechargé votre shell):"
    echo "  jarvis build \"Votre commande\""
    echo ""
fi
echo "Documentation:"
echo "  - INSTALLATION_RAPIDE.md"
echo "  - GUIDE_UTILISATION.md"
echo "  - GUIDE_WEBHOOK.md"
echo ""
