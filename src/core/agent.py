"""
Agent Jarvis - Orchestrateur principal.
"""

from pathlib import Path
from typing import Dict, Any, Optional

from .config import get_config
from .logger import init_logger_from_config
from .llm import LLMClient
from .knowledge_base import KnowledgeBase
from ..modules.builder import Builder
from ..modules.fixer import Fixer
from ..modules.deployer import Deployer


class JarvisAgent:
    """Agent principal Jarvis."""
    
    def __init__(self, config_path: Optional[str] = None):
        """
        Initialise l'agent Jarvis.
        
        Args:
            config_path: Chemin vers le fichier de configuration (optionnel)
        """
        # Charger la configuration
        self.config = get_config(config_path)
        
        # Initialiser le logger
        self.logger = init_logger_from_config(self.config)
        
        self.logger.section("Initialisation de l'Agent Jarvis")
        
        # Initialiser le client LLM
        self.logger.action("Initialisation du client LLM...")
        self.llm = LLMClient(self.config)
        self.logger.success(f"Client LLM initialisé (modèle: {self.config.llm.model})")
        
        # Initialiser la base de connaissances
        self.logger.action("Initialisation de la base de connaissances...")
        self.kb = KnowledgeBase(self.config, self.llm)
        self.logger.success("Base de connaissances initialisée")
        
        # Initialiser les modules
        self.logger.action("Initialisation des modules...")
        
        self.builder = None
        if self.config.modules.builder:
            self.builder = Builder(self.config, self.llm, self.kb, self.logger)
            self.logger.success("✓ Module Builder activé")
        
        self.fixer = None
        if self.config.modules.fixer:
            self.fixer = Fixer(self.config, self.llm, self.kb, self.logger)
            self.logger.success("✓ Module Fixer activé")
        
        self.deployer = Deployer(self.config, self.llm, self.kb, self.logger)
        self.logger.success("✓ Module Deployer activé")
        
        self.logger.success("Agent Jarvis prêt !")
    
    def process_request(self, request: str) -> Dict[str, Any]:
        """
        Traite une demande utilisateur.
        
        Args:
            request: Demande de l'utilisateur
            
        Returns:
            Résultat du traitement
        """
        self.logger.section("Traitement de la demande")
        self.logger.info(f"Demande : {request}")
        
        # Analyser la demande pour déterminer le type d'action
        action_type = self._classify_request(request)
        
        self.logger.info(f"Type d'action identifié : {action_type}")
        
        if action_type == "build":
            return self._handle_build_request(request)
        elif action_type == "fix":
            return self._handle_fix_request(request)
        elif action_type == "question":
            return self._handle_question(request)
        else:
            return {
                "success": False,
                "error": "Type de demande non reconnu",
                "suggestion": "Essayez de reformuler votre demande"
            }
    
    def build(self, request: str, output_dir: Optional[str] = None) -> Dict[str, Any]:
        """
        Construit un outil informatique.
        
        Args:
            request: Description de l'outil à construire
            output_dir: Répertoire de sortie (optionnel)
            
        Returns:
            Résultat de la construction
        """
        if not self.builder:
            return {"success": False, "error": "Module Builder non activé"}
        
        # Analyser la demande
        analysis = self.builder.analyze_request(request)
        
        # Déterminer le répertoire de sortie
        if output_dir is None:
            base_dir = self.config.get_base_dir()
            output_dir = str(base_dir / "projects" / analysis.get("project_name", "nouveau_projet"))
        
        # Construire selon le type d'outil
        tool_type = analysis.get("tool_type", "").lower()
        
        if "site" in tool_type or "web" in tool_type:
            if "statique" in tool_type or "static" in tool_type:
                return self.builder.build_website_static(
                    project_name=analysis.get("project_name", "site_web"),
                    description=request,
                    features=analysis.get("features", []),
                    output_dir=output_dir
                )
        
        elif "api" in tool_type:
            # Extraire les endpoints de la demande
            endpoints = self._extract_endpoints(request, analysis)
            return self.builder.build_api_rest(
                project_name=analysis.get("project_name", "api"),
                description=request,
                endpoints=endpoints,
                output_dir=output_dir
            )
        
        elif "cli" in tool_type or "commande" in tool_type:
            # Extraire les commandes de la demande
            commands = self._extract_commands(request, analysis)
            return self.builder.build_cli_tool(
                project_name=analysis.get("project_name", "cli_tool"),
                description=request,
                commands=commands,
                output_dir=output_dir
            )
        
        else:
            # Type d'outil non supporté, construire un site web par défaut
            self.logger.warning(f"Type d'outil '{tool_type}' non supporté, construction d'un site web statique")
            return self.builder.build_website_static(
                project_name=analysis.get("project_name", "projet"),
                description=request,
                features=analysis.get("features", []),
                output_dir=output_dir
            )
    
    def fix(self, project_path: str, issue_description: str) -> Dict[str, Any]:
        """
        Répare un problème dans un projet.
        
        Args:
            project_path: Chemin vers le projet
            issue_description: Description du problème
            
        Returns:
            Résultat de la réparation
        """
        if not self.fixer:
            return {"success": False, "error": "Module Fixer non activé"}
        
        return self.fixer.fix_issue(project_path, issue_description)
    
    def analyze(self, project_path: str) -> Dict[str, Any]:
        """
        Analyse un projet.
        
        Args:
            project_path: Chemin vers le projet
            
        Returns:
            Analyse du projet
        """
        if not self.fixer:
            return {"success": False, "error": "Module Fixer non activé"}
        
        return self.fixer.analyze_project(project_path)
    
    def refactor(self, file_path: str, objective: str = "améliorer la qualité") -> Dict[str, Any]:
        """
        Refactorise un fichier.
        
        Args:
            file_path: Chemin vers le fichier
            objective: Objectif du refactoring
            
        Returns:
            Résultat du refactoring
        """
        if not self.fixer:
            return {"success": False, "error": "Module Fixer non activé"}
        
        return self.fixer.refactor_code(file_path, objective)
    
    def ask(self, question: str, context: Optional[str] = None) -> str:
        """
        Pose une question à l'agent.
        
        Args:
            question: Question à poser
            context: Contexte additionnel (optionnel)
            
        Returns:
            Réponse de l'agent
        """
        # Rechercher dans la base de connaissances
        solutions = self.kb.search_solutions(question, limit=3)
        
        kb_context = ""
        if solutions:
            kb_context = "\n\nSolutions similaires trouvées dans la base de connaissances :\n"
            for i, solution in enumerate(solutions, 1):
                kb_context += f"\n{i}. {solution.get('problem', 'N/A')}\n   Solution : {solution.get('solution', 'N/A')[:200]}...\n"
        
        full_context = f"{context}\n{kb_context}" if context else kb_context
        
        return self.llm.answer_question(question, full_context if full_context else None)
    
    def deploy(
        self,
        project_path: str,
        method: str = "ssh",
        config: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Déploie un projet.
        
        Args:
            project_path: Chemin vers le projet
            method: Méthode de déploiement (ssh, docker, cloud, ftp)
            config: Configuration de déploiement
            
        Returns:
            Résultat du déploiement
        """
        if not self.deployer:
            return {"success": False, "error": "Module Deployer non activé"}
        
        return self.deployer.deploy(project_path, method, config or {})
    
    def learn(self, content: str, content_type: str = "solution", 
              tags: Optional[list] = None) -> str:
        """
        Apprend une nouvelle connaissance.
        
        Args:
            content: Contenu à apprendre
            content_type: Type de contenu (solution, template, pattern)
            tags: Tags pour la recherche
            
        Returns:
            ID de la connaissance sauvegardée
        """
        self.logger.action(f"Apprentissage d'une nouvelle {content_type}...")
        
        if content_type == "solution":
            # Extraire le problème et la solution
            parts = content.split("Solution:", 1)
            if len(parts) == 2:
                problem = parts[0].replace("Problème:", "").strip()
                solution = parts[1].strip()
            else:
                problem = "Connaissance générale"
                solution = content
            
            knowledge_id = self.kb.save_solution(
                problem=problem,
                solution=solution,
                tags=tags or []
            )
        else:
            # Pour l'instant, sauvegarder comme solution
            knowledge_id = self.kb.save_solution(
                problem=f"Connaissance de type {content_type}",
                solution=content,
                tags=tags or [content_type]
            )
        
        self.logger.success(f"Connaissance sauvegardée : {knowledge_id}")
        return knowledge_id
    
    def _classify_request(self, request: str) -> str:
        """Classifie une demande utilisateur."""
        request_lower = request.lower()
        
        # Mots-clés pour la construction
        build_keywords = ["crée", "construis", "génère", "développe", "fais", "build", "create"]
        
        # Mots-clés pour la réparation
        fix_keywords = ["répare", "corrige", "fix", "debug", "résous", "problème", "erreur", "bug"]
        
        # Vérifier les mots-clés
        if any(keyword in request_lower for keyword in build_keywords):
            return "build"
        elif any(keyword in request_lower for keyword in fix_keywords):
            return "fix"
        else:
            return "question"
    
    def _handle_build_request(self, request: str) -> Dict[str, Any]:
        """Gère une demande de construction."""
        return self.build(request)
    
    def _handle_fix_request(self, request: str) -> Dict[str, Any]:
        """Gère une demande de réparation."""
        # Extraire le chemin du projet de la demande
        # Pour l'instant, retourner une erreur demandant plus d'informations
        return {
            "success": False,
            "error": "Veuillez spécifier le chemin du projet à réparer",
            "suggestion": "Utilisez la méthode fix() avec le chemin du projet"
        }
    
    def _handle_question(self, request: str) -> Dict[str, Any]:
        """Gère une question."""
        answer = self.ask(request)
        return {
            "success": True,
            "answer": answer
        }
    
    def _extract_endpoints(self, request: str, analysis: Dict[str, Any]) -> list:
        """Extrait les endpoints d'une demande d'API."""
        # Utiliser le LLM pour extraire les endpoints
        prompt = f"""À partir de cette demande d'API :

"{request}"

Extrais les endpoints à créer au format JSON :
[
  {{"method": "GET", "path": "/endpoint", "description": "Description"}},
  ...
]

Retourne uniquement le JSON."""
        
        response = self.llm.answer_question(prompt)
        
        import json
        try:
            start = response.find('[')
            end = response.rfind(']') + 1
            if start != -1 and end > start:
                json_str = response[start:end]
                return json.loads(json_str)
        except:
            pass
        
        # Valeurs par défaut
        return [
            {"method": "GET", "path": "/", "description": "Endpoint racine"},
            {"method": "GET", "path": "/health", "description": "Vérification de santé"}
        ]
    
    def _extract_commands(self, request: str, analysis: Dict[str, Any]) -> list:
        """Extrait les commandes d'une demande d'outil CLI."""
        # Utiliser le LLM pour extraire les commandes
        prompt = f"""À partir de cette demande d'outil CLI :

"{request}"

Extrais les commandes à créer au format JSON :
[
  {{"name": "command", "description": "Description de la commande"}},
  ...
]

Retourne uniquement le JSON."""
        
        response = self.llm.answer_question(prompt)
        
        import json
        try:
            start = response.find('[')
            end = response.rfind(']') + 1
            if start != -1 and end > start:
                json_str = response[start:end]
                return json.loads(json_str)
        except:
            pass
        
        # Valeurs par défaut
        return [
            {"name": "run", "description": "Exécute l'action principale"},
            {"name": "help", "description": "Affiche l'aide"}
        ]
