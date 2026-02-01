#!/bin/bash

# Script d'upload automatique vers GitHub
# Auteur: Yacine Abdi
# Dépôt cible: https://github.com/OEOEOEDZ/Python/Trading.git

echo "=========================================="
echo "Upload du projet Algorithmic Trading Simulator"
echo "Auteur: Yacine Abdi"
echo "=========================================="
echo ""

# Couleurs pour les messages
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Configuration
REPO_URL="https://github.com/OEOEOEDZ/Python.git"
TARGET_DIR="Trading"
PROJECT_DIR="algorithmic-trading-simulator"

# Fonction pour afficher les messages
info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

# Vérifier si git est installé
if ! command -v git &> /dev/null; then
    error "Git n'est pas installé. Installez git d'abord."
    exit 1
fi

info "Vérification de Git... OK"

# Demander confirmation
echo ""
echo "Ce script va :"
echo "1. Cloner votre dépôt GitHub"
echo "2. Copier le projet dans le dossier Trading"
echo "3. Commit et push les changements"
echo ""
read -p "Voulez-vous continuer ? (y/n) " -n 1 -r
echo ""

if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    warning "Opération annulée."
    exit 0
fi

# Créer un dossier temporaire
TEMP_DIR=$(mktemp -d)
info "Dossier temporaire créé: $TEMP_DIR"

# Cloner le dépôt
info "Clonage du dépôt..."
cd "$TEMP_DIR"
git clone "$REPO_URL" repo
if [ $? -ne 0 ]; then
    error "Échec du clonage. Vérifiez l'URL et vos accès GitHub."
    exit 1
fi

cd repo
info "Dépôt cloné avec succès"

# Créer le dossier Trading s'il n'existe pas
if [ ! -d "$TARGET_DIR" ]; then
    info "Création du dossier $TARGET_DIR..."
    mkdir -p "$TARGET_DIR"
fi

# Copier les fichiers du projet
info "Copie des fichiers du projet..."
cp -r "$OLDPWD/$PROJECT_DIR"/* "$TARGET_DIR/" 2>/dev/null || {
    # Si le chemin ne fonctionne pas, demander le chemin
    echo ""
    read -p "Entrez le chemin complet vers le dossier $PROJECT_DIR: " PROJECT_PATH
    cp -r "$PROJECT_PATH"/* "$TARGET_DIR/"
}

if [ $? -ne 0 ]; then
    error "Échec de la copie des fichiers."
    exit 1
fi

info "Fichiers copiés avec succès"

# Configurer git (si nécessaire)
echo ""
read -p "Voulez-vous configurer votre nom et email pour ce commit ? (y/n) " -n 1 -r
echo ""
if [[ $REPLY =~ ^[Yy]$ ]]; then
    read -p "Votre nom (ex: Yacine Abdi): " GIT_NAME
    read -p "Votre email: " GIT_EMAIL
    git config user.name "$GIT_NAME"
    git config user.email "$GIT_EMAIL"
    info "Configuration Git mise à jour"
fi

# Ajouter les fichiers
info "Ajout des fichiers au commit..."
git add "$TARGET_DIR"

# Créer le commit
COMMIT_MESSAGE="Add algorithmic trading simulator by Yacine Abdi

- 5 trading strategies (RSI, MACD, MA Crossover, Bollinger Bands, Mean Reversion)
- Complete backtesting engine with portfolio management
- Advanced performance metrics (Sharpe, Sortino, VaR, etc.)
- Interactive dashboard with Streamlit
- Comprehensive documentation and tests
- 2,500+ lines of professional Python code"

info "Création du commit..."
git commit -m "$COMMIT_MESSAGE"

if [ $? -ne 0 ]; then
    warning "Rien à commiter (peut-être déjà présent)"
fi

# Push vers GitHub
info "Push vers GitHub..."
echo ""
echo "Tentative de push vers le dépôt distant..."
echo "Vous devrez peut-être entrer vos identifiants GitHub."
echo ""

# Essayer main d'abord, puis master si ça échoue
git push origin main 2>/dev/null || git push origin master

if [ $? -eq 0 ]; then
    echo ""
    echo "=========================================="
    echo -e "${GREEN}✅ Upload réussi !${NC}"
    echo "=========================================="
    echo ""
    echo "Votre projet est maintenant disponible sur :"
    echo "https://github.com/OEOEOEDZ/Python/tree/main/$TARGET_DIR"
    echo ""
    echo "Prochaines étapes :"
    echo "1. Vérifiez que tout est bien sur GitHub"
    echo "2. Ajoutez une description au dépôt"
    echo "3. Ajoutez des topics: python, trading, finance"
    echo "4. Partagez le projet sur LinkedIn !"
    echo ""
else
    error "Échec du push. Vérifiez vos droits d'accès GitHub."
    echo ""
    echo "Pour pousser manuellement :"
    echo "cd $TEMP_DIR/repo"
    echo "git push origin main"
    exit 1
fi

# Nettoyer
info "Nettoyage du dossier temporaire..."
cd "$OLDPWD"
rm -rf "$TEMP_DIR"

echo ""
echo "=========================================="
echo "Script terminé !"
echo "=========================================="
