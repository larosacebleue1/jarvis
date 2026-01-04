#!/bin/bash

# ============================================================================
# Jarvis Auto-Installer
# Installation automatique en une seule commande
# ============================================================================

set -e

# Couleurs pour l'affichage
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# URL de l'archive Jarvis
JARVIS_URL="https://github.com/votre-repo/jarvis-agent/releases/latest/download/jarvis-agent.tar.gz"
JARVIS_DIR="$HOME/jarvis-agent"
TEMP_DIR="/tmp/jarvis-install-$$"

# Fonction pour afficher les messages
print_header() {
    echo -e "${PURPLE}"
    echo "╔════════════════════════════════════════════════════════════════════╗"
    echo "║                    🤖 Jarvis Auto-Installer                        ║"
    echo "║              Installation automatique de Jarvis Agent              ║"
    echo "╚════════════════════════════════════════════════════════════════════╝"
    echo -e "${NC}"
}

print_step() {
    echo -e "${CYAN}▶ $1${NC}"
}

print_success() {
    echo -e "${GREEN}✓ $1${NC}"
}

print_error() {
    echo -e "${RED}✗ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠ $1${NC}"
}

# Fonction pour détecter l'OS
detect_os() {
    if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        OS="linux"
    elif [[ "$OSTYPE" == "darwin"* ]]; then
        OS="macos"
    else
        print_error "Système d'exploitation non supporté: $OSTYPE"
        exit 1
    fi
    print_success "Système détecté: $OS"
}

# Fonction pour vérifier Python
check_python() {
    print_step "Vérification de Python..."
    
    if command -v python3 &> /dev/null; then
        PYTHON_CMD="python3"
        PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
        print_success "Python $PYTHON_VERSION trouvé"
    else
        print_error "Python 3 n'est pas installé"
        echo ""
        echo "Installation de Python:"
        if [[ "$OS" == "macos" ]]; then
            echo "  brew install python3"
        else
            echo "  sudo apt install python3 python3-pip    # Ubuntu/Debian"
            echo "  sudo dnf install python3 python3-pip    # Fedora"
            echo "  sudo pacman -S python python-pip        # Arch"
        fi
        exit 1
    fi
}

# Fonction pour vérifier pip
check_pip() {
    print_step "Vérification de pip..."
    
    if command -v pip3 &> /dev/null; then
        PIP_CMD="pip3"
        print_success "pip3 trouvé"
    else
        print_error "pip3 n'est pas installé"
        echo ""
        echo "Installation de pip:"
        if [[ "$OS" == "macos" ]]; then
            echo "  brew install python3"
        else
            echo "  sudo apt install python3-pip    # Ubuntu/Debian"
            echo "  sudo dnf install python3-pip    # Fedora"
        fi
        exit 1
    fi
}

# Fonction pour créer le répertoire temporaire
create_temp_dir() {
    print_step "Création du répertoire temporaire..."
    mkdir -p "$TEMP_DIR"
    print_success "Répertoire créé: $TEMP_DIR"
}

# Fonction pour télécharger Jarvis
download_jarvis() {
    print_step "Téléchargement de Jarvis..."
    
    # Pour le moment, on utilise l'archive locale
    # Dans une vraie installation, on téléchargerait depuis GitHub ou un serveur
    
    # Simuler le téléchargement avec l'archive locale
    if [ -f "/home/ubuntu/jarvis-agent-v1.3.0-final.tar.gz" ]; then
        cp /home/ubuntu/jarvis-agent-v1.3.0-final.tar.gz "$TEMP_DIR/jarvis-agent.tar.gz"
        print_success "Archive téléchargée"
    else
        # En production, utiliser curl ou wget
        print_error "Archive non trouvée"
        echo ""
        echo "L'installeur doit être configuré avec l'URL de téléchargement."
        echo "Téléchargez manuellement l'archive depuis:"
        echo "  https://votre-serveur.com/jarvis-agent.tar.gz"
        exit 1
    fi
}

# Fonction pour extraire l'archive
extract_jarvis() {
    print_step "Extraction de l'archive..."
    
    cd "$TEMP_DIR"
    tar -xzf jarvis-agent.tar.gz
    
    if [ ! -d "jarvis-agent" ]; then
        print_error "Échec de l'extraction"
        exit 1
    fi
    
    print_success "Archive extraite"
}

# Fonction pour installer Jarvis
install_jarvis() {
    print_step "Installation de Jarvis dans $JARVIS_DIR..."
    
    # Sauvegarder l'ancienne installation si elle existe
    if [ -d "$JARVIS_DIR" ]; then
        print_warning "Installation existante détectée"
        BACKUP_DIR="$JARVIS_DIR.backup.$(date +%Y%m%d_%H%M%S)"
        mv "$JARVIS_DIR" "$BACKUP_DIR"
        print_success "Sauvegarde créée: $BACKUP_DIR"
    fi
    
    # Copier les fichiers
    mv "$TEMP_DIR/jarvis-agent" "$JARVIS_DIR"
    print_success "Fichiers installés"
}

# Fonction pour installer les dépendances
install_dependencies() {
    print_step "Installation des dépendances Python..."
    
    cd "$JARVIS_DIR"
    $PIP_CMD install --user -r requirements.txt > /dev/null 2>&1
    
    if [ $? -eq 0 ]; then
        print_success "Dépendances installées"
    else
        print_error "Échec de l'installation des dépendances"
        exit 1
    fi
}

# Fonction pour configurer la clé API
configure_api_key() {
    echo ""
    echo -e "${BLUE}════════════════════════════════════════════════════════════════════${NC}"
    echo -e "${BLUE}                    Configuration de la clé API                     ${NC}"
    echo -e "${BLUE}════════════════════════════════════════════════════════════════════${NC}"
    echo ""
    echo "Jarvis a besoin d'une clé API OpenAI pour fonctionner."
    echo ""
    echo "Si vous n'en avez pas encore:"
    echo "  1. Allez sur https://platform.openai.com/"
    echo "  2. Créez un compte (si nécessaire)"
    echo "  3. Allez dans 'API Keys'"
    echo "  4. Créez une nouvelle clé"
    echo ""
    
    read -p "Entrez votre clé API OpenAI (sk-...): " API_KEY
    
    if [ -z "$API_KEY" ]; then
        print_warning "Clé API non fournie"
        echo "Vous pourrez la configurer plus tard avec:"
        echo "  export OPENAI_API_KEY='votre-clé'"
        return
    fi
    
    # Créer le fichier .env
    echo "OPENAI_API_KEY=$API_KEY" > "$JARVIS_DIR/.env"
    chmod 600 "$JARVIS_DIR/.env"
    print_success "Clé API sauvegardée dans .env"
    
    # Ajouter au shell RC
    SHELL_RC=""
    if [ -f "$HOME/.zshrc" ]; then
        SHELL_RC="$HOME/.zshrc"
    elif [ -f "$HOME/.bashrc" ]; then
        SHELL_RC="$HOME/.bashrc"
    fi
    
    if [ -n "$SHELL_RC" ]; then
        echo ""
        read -p "Ajouter la clé API à votre shell ($SHELL_RC)? (o/n): " ADD_TO_SHELL
        if [[ "$ADD_TO_SHELL" == "o" ]] || [[ "$ADD_TO_SHELL" == "O" ]]; then
            if ! grep -q "OPENAI_API_KEY" "$SHELL_RC"; then
                echo "" >> "$SHELL_RC"
                echo "# Jarvis API Key" >> "$SHELL_RC"
                echo "export OPENAI_API_KEY='$API_KEY'" >> "$SHELL_RC"
                print_success "Clé ajoutée à $SHELL_RC"
            else
                print_warning "Clé déjà présente dans $SHELL_RC"
            fi
        fi
    fi
}

# Fonction pour créer un alias
create_alias() {
    SHELL_RC=""
    if [ -f "$HOME/.zshrc" ]; then
        SHELL_RC="$HOME/.zshrc"
    elif [ -f "$HOME/.bashrc" ]; then
        SHELL_RC="$HOME/.bashrc"
    fi
    
    if [ -n "$SHELL_RC" ]; then
        echo ""
        read -p "Créer un alias 'jarvis' pour faciliter l'utilisation? (o/n): " CREATE_ALIAS
        if [[ "$CREATE_ALIAS" == "o" ]] || [[ "$CREATE_ALIAS" == "O" ]]; then
            if ! grep -q "alias jarvis=" "$SHELL_RC"; then
                echo "" >> "$SHELL_RC"
                echo "# Jarvis Agent Alias" >> "$SHELL_RC"
                echo "alias jarvis='$PYTHON_CMD $JARVIS_DIR/jarvis_agent_cli.py'" >> "$SHELL_RC"
                print_success "Alias créé dans $SHELL_RC"
                echo ""
                echo -e "${YELLOW}Rechargez votre shell avec: source $SHELL_RC${NC}"
            else
                print_warning "Alias déjà présent dans $SHELL_RC"
            fi
        fi
    fi
}

# Fonction pour tester l'installation
test_installation() {
    print_step "Test de l'installation..."
    
    cd "$JARVIS_DIR"
    
    # Charger la clé API si elle existe
    if [ -f ".env" ]; then
        export $(cat .env | xargs)
    fi
    
    $PYTHON_CMD jarvis_agent_cli.py info > /dev/null 2>&1
    
    if [ $? -eq 0 ]; then
        print_success "Test réussi"
    else
        print_warning "Le test a échoué (peut-être dû à la clé API)"
    fi
}

# Fonction pour nettoyer
cleanup() {
    print_step "Nettoyage..."
    rm -rf "$TEMP_DIR"
    print_success "Nettoyage terminé"
}

# Fonction pour afficher le résumé
print_summary() {
    echo ""
    echo -e "${GREEN}╔════════════════════════════════════════════════════════════════════╗${NC}"
    echo -e "${GREEN}║              ✓ Installation terminée avec succès !                ║${NC}"
    echo -e "${GREEN}╚════════════════════════════════════════════════════════════════════╝${NC}"
    echo ""
    echo -e "${CYAN}📍 Jarvis installé dans: $JARVIS_DIR${NC}"
    echo ""
    echo -e "${YELLOW}🚀 Pour utiliser Jarvis:${NC}"
    echo ""
    echo "  $PYTHON_CMD $JARVIS_DIR/jarvis_agent_cli.py build \"Votre commande\""
    echo ""
    if grep -q "alias jarvis=" "$HOME/.zshrc" 2>/dev/null || grep -q "alias jarvis=" "$HOME/.bashrc" 2>/dev/null; then
        echo -e "${YELLOW}Ou simplement (après avoir rechargé votre shell):${NC}"
        echo ""
        echo "  jarvis build \"Votre commande\""
        echo ""
    fi
    echo -e "${CYAN}📚 Documentation:${NC}"
    echo "  - $JARVIS_DIR/README_INSTALLATION.md"
    echo "  - $JARVIS_DIR/INSTALLATION_RAPIDE.md"
    echo "  - $JARVIS_DIR/GUIDE_UTILISATION.md"
    echo "  - $JARVIS_DIR/GUIDE_WEBHOOK.md"
    echo ""
    echo -e "${CYAN}💡 Exemples:${NC}"
    echo "  jarvis build \"Crée un site web pour mon portfolio\""
    echo "  jarvis ask \"Comment créer une API REST ?\""
    echo "  jarvis fix ./mon-projet \"Bug au démarrage\""
    echo ""
}

# ============================================================================
# Script principal
# ============================================================================

main() {
    print_header
    
    detect_os
    check_python
    check_pip
    create_temp_dir
    download_jarvis
    extract_jarvis
    install_jarvis
    install_dependencies
    configure_api_key
    create_alias
    test_installation
    cleanup
    print_summary
}

# Gestion des erreurs
trap 'print_error "Installation interrompue"; cleanup; exit 1' ERR INT TERM

# Lancer l'installation
main
