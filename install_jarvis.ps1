# ============================================================================
# Jarvis Auto-Installer pour Windows (PowerShell)
# Installation automatique en une seule commande
# ============================================================================

# Activer les couleurs
$Host.UI.RawUI.ForegroundColor = "White"

# Variables
$JarvisUrl = "https://github.com/votre-repo/jarvis-agent/releases/latest/download/jarvis-agent.zip"
$JarvisDir = "$env:USERPROFILE\jarvis-agent"
$TempDir = "$env:TEMP\jarvis-install-$(Get-Random)"

# Fonctions d'affichage
function Print-Header {
    Write-Host ""
    Write-Host "╔════════════════════════════════════════════════════════════════════╗" -ForegroundColor Magenta
    Write-Host "║                    🤖 Jarvis Auto-Installer                        ║" -ForegroundColor Magenta
    Write-Host "║              Installation automatique de Jarvis Agent              ║" -ForegroundColor Magenta
    Write-Host "╚════════════════════════════════════════════════════════════════════╝" -ForegroundColor Magenta
    Write-Host ""
}

function Print-Step {
    param($Message)
    Write-Host "▶ $Message" -ForegroundColor Cyan
}

function Print-Success {
    param($Message)
    Write-Host "✓ $Message" -ForegroundColor Green
}

function Print-Error {
    param($Message)
    Write-Host "✗ $Message" -ForegroundColor Red
}

function Print-Warning {
    param($Message)
    Write-Host "⚠ $Message" -ForegroundColor Yellow
}

# Fonction pour vérifier Python
function Check-Python {
    Print-Step "Vérification de Python..."
    
    try {
        $pythonVersion = python --version 2>&1
        if ($pythonVersion -match "Python (\d+\.\d+\.\d+)") {
            Print-Success "Python $($Matches[1]) trouvé"
            return "python"
        }
    } catch {
        Print-Error "Python n'est pas installé"
        Write-Host ""
        Write-Host "Téléchargez Python depuis: https://www.python.org/downloads/"
        Write-Host "⚠ Cochez 'Add Python to PATH' pendant l'installation"
        exit 1
    }
}

# Fonction pour vérifier pip
function Check-Pip {
    Print-Step "Vérification de pip..."
    
    try {
        $pipVersion = pip --version 2>&1
        if ($pipVersion) {
            Print-Success "pip trouvé"
            return "pip"
        }
    } catch {
        Print-Error "pip n'est pas installé"
        Write-Host ""
        Write-Host "Réinstallez Python en cochant 'pip' dans les options"
        exit 1
    }
}

# Fonction pour créer le répertoire temporaire
function Create-TempDir {
    Print-Step "Création du répertoire temporaire..."
    New-Item -ItemType Directory -Path $TempDir -Force | Out-Null
    Print-Success "Répertoire créé: $TempDir"
}

# Fonction pour télécharger Jarvis
function Download-Jarvis {
    Print-Step "Téléchargement de Jarvis..."
    
    # Pour le moment, on utilise l'archive locale
    # Dans une vraie installation, on téléchargerait depuis GitHub
    
    $localArchive = "C:\Users\$env:USERNAME\Downloads\jarvis-agent-v1.3.0-final.tar.gz"
    
    if (Test-Path $localArchive) {
        Copy-Item $localArchive "$TempDir\jarvis-agent.tar.gz"
        Print-Success "Archive copiée"
    } else {
        Print-Error "Archive non trouvée"
        Write-Host ""
        Write-Host "Téléchargez l'archive depuis:"
        Write-Host "  https://votre-serveur.com/jarvis-agent.tar.gz"
        Write-Host ""
        Write-Host "Et placez-la dans: $env:USERPROFILE\Downloads\"
        exit 1
    }
}

# Fonction pour extraire l'archive
function Extract-Jarvis {
    Print-Step "Extraction de l'archive..."
    
    # Vérifier si tar est disponible (Windows 10+)
    if (Get-Command tar -ErrorAction SilentlyContinue) {
        Set-Location $TempDir
        tar -xzf jarvis-agent.tar.gz
        Print-Success "Archive extraite"
    } else {
        Print-Error "tar n'est pas disponible"
        Write-Host ""
        Write-Host "Installez 7-Zip depuis: https://www.7-zip.org/"
        Write-Host "Puis extrayez manuellement l'archive"
        exit 1
    }
}

# Fonction pour installer Jarvis
function Install-Jarvis {
    Print-Step "Installation de Jarvis dans $JarvisDir..."
    
    # Sauvegarder l'ancienne installation
    if (Test-Path $JarvisDir) {
        Print-Warning "Installation existante détectée"
        $backupDir = "$JarvisDir.backup.$(Get-Date -Format 'yyyyMMdd_HHmmss')"
        Move-Item $JarvisDir $backupDir
        Print-Success "Sauvegarde créée: $backupDir"
    }
    
    # Copier les fichiers
    Move-Item "$TempDir\jarvis-agent" $JarvisDir
    Print-Success "Fichiers installés"
}

# Fonction pour installer les dépendances
function Install-Dependencies {
    Print-Step "Installation des dépendances Python..."
    
    Set-Location $JarvisDir
    pip install -r requirements.txt --quiet
    
    if ($LASTEXITCODE -eq 0) {
        Print-Success "Dépendances installées"
    } else {
        Print-Error "Échec de l'installation des dépendances"
        exit 1
    }
}

# Fonction pour configurer la clé API
function Configure-ApiKey {
    Write-Host ""
    Write-Host "════════════════════════════════════════════════════════════════════" -ForegroundColor Blue
    Write-Host "                    Configuration de la clé API                     " -ForegroundColor Blue
    Write-Host "════════════════════════════════════════════════════════════════════" -ForegroundColor Blue
    Write-Host ""
    Write-Host "Jarvis a besoin d'une clé API OpenAI pour fonctionner."
    Write-Host ""
    Write-Host "Si vous n'en avez pas encore:"
    Write-Host "  1. Allez sur https://platform.openai.com/"
    Write-Host "  2. Créez un compte (si nécessaire)"
    Write-Host "  3. Allez dans 'API Keys'"
    Write-Host "  4. Créez une nouvelle clé"
    Write-Host ""
    
    $apiKey = Read-Host "Entrez votre clé API OpenAI (sk-...)"
    
    if ([string]::IsNullOrWhiteSpace($apiKey)) {
        Print-Warning "Clé API non fournie"
        Write-Host "Vous pourrez la configurer plus tard avec:"
        Write-Host '  $env:OPENAI_API_KEY="votre-clé"'
        return
    }
    
    # Créer le fichier .env
    "OPENAI_API_KEY=$apiKey" | Out-File -FilePath "$JarvisDir\.env" -Encoding UTF8
    Print-Success "Clé API sauvegardée dans .env"
    
    # Ajouter aux variables d'environnement utilisateur
    Write-Host ""
    $addToEnv = Read-Host "Ajouter la clé API aux variables d'environnement? (o/n)"
    if ($addToEnv -eq "o" -or $addToEnv -eq "O") {
        [System.Environment]::SetEnvironmentVariable("OPENAI_API_KEY", $apiKey, "User")
        Print-Success "Clé ajoutée aux variables d'environnement"
    }
}

# Fonction pour créer un alias
function Create-Alias {
    Write-Host ""
    $createAlias = Read-Host "Créer un alias 'jarvis' dans PowerShell? (o/n)"
    
    if ($createAlias -eq "o" -or $createAlias -eq "O") {
        $profilePath = $PROFILE.CurrentUserAllHosts
        
        if (!(Test-Path $profilePath)) {
            New-Item -Path $profilePath -ItemType File -Force | Out-Null
        }
        
        $aliasLine = "function jarvis { python `"$JarvisDir\jarvis_agent_cli.py`" @args }"
        
        if (!(Select-String -Path $profilePath -Pattern "function jarvis" -Quiet)) {
            Add-Content -Path $profilePath -Value "`n# Jarvis Agent Alias"
            Add-Content -Path $profilePath -Value $aliasLine
            Print-Success "Alias créé dans $profilePath"
            Write-Host ""
            Print-Warning "Rechargez PowerShell pour utiliser l'alias 'jarvis'"
        } else {
            Print-Warning "Alias déjà présent dans $profilePath"
        }
    }
}

# Fonction pour tester l'installation
function Test-Installation {
    Print-Step "Test de l'installation..."
    
    Set-Location $JarvisDir
    
    # Charger la clé API si elle existe
    if (Test-Path ".env") {
        Get-Content ".env" | ForEach-Object {
            if ($_ -match "^([^=]+)=(.*)$") {
                [System.Environment]::SetEnvironmentVariable($matches[1], $matches[2], "Process")
            }
        }
    }
    
    python jarvis_agent_cli.py info | Out-Null
    
    if ($LASTEXITCODE -eq 0) {
        Print-Success "Test réussi"
    } else {
        Print-Warning "Le test a échoué (peut-être dû à la clé API)"
    }
}

# Fonction pour nettoyer
function Cleanup {
    Print-Step "Nettoyage..."
    Remove-Item -Path $TempDir -Recurse -Force
    Print-Success "Nettoyage terminé"
}

# Fonction pour afficher le résumé
function Print-Summary {
    Write-Host ""
    Write-Host "╔════════════════════════════════════════════════════════════════════╗" -ForegroundColor Green
    Write-Host "║              ✓ Installation terminée avec succès !                ║" -ForegroundColor Green
    Write-Host "╚════════════════════════════════════════════════════════════════════╝" -ForegroundColor Green
    Write-Host ""
    Write-Host "📍 Jarvis installé dans: $JarvisDir" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "🚀 Pour utiliser Jarvis:" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "  python `"$JarvisDir\jarvis_agent_cli.py`" build `"Votre commande`""
    Write-Host ""
    
    if (Select-String -Path $PROFILE.CurrentUserAllHosts -Pattern "function jarvis" -Quiet -ErrorAction SilentlyContinue) {
        Write-Host "Ou simplement (après avoir rechargé PowerShell):" -ForegroundColor Yellow
        Write-Host ""
        Write-Host "  jarvis build `"Votre commande`""
        Write-Host ""
    }
    
    Write-Host "📚 Documentation:" -ForegroundColor Cyan
    Write-Host "  - $JarvisDir\README_INSTALLATION.md"
    Write-Host "  - $JarvisDir\INSTALLATION_RAPIDE.md"
    Write-Host "  - $JarvisDir\GUIDE_UTILISATION.md"
    Write-Host "  - $JarvisDir\GUIDE_WEBHOOK.md"
    Write-Host ""
    Write-Host "💡 Exemples:" -ForegroundColor Cyan
    Write-Host "  jarvis build `"Crée un site web pour mon portfolio`""
    Write-Host "  jarvis ask `"Comment créer une API REST ?`""
    Write-Host "  jarvis fix .\mon-projet `"Bug au démarrage`""
    Write-Host ""
}

# ============================================================================
# Script principal
# ============================================================================

function Main {
    Print-Header
    
    Check-Python
    Check-Pip
    Create-TempDir
    Download-Jarvis
    Extract-Jarvis
    Install-Jarvis
    Install-Dependencies
    Configure-ApiKey
    Create-Alias
    Test-Installation
    Cleanup
    Print-Summary
}

# Gestion des erreurs
trap {
    Print-Error "Installation interrompue"
    if (Test-Path $TempDir) {
        Remove-Item -Path $TempDir -Recurse -Force
    }
    exit 1
}

# Lancer l'installation
Main
