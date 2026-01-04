#!/usr/bin/env python3
"""
Script webhook pour l'agent Jarvis.
Récupère et exécute automatiquement les commandes depuis l'API Remote Control.
"""

import os
import sys
import time
import json
import requests
from typing import Dict, Any, List
from pathlib import Path

# Ajouter le répertoire parent au path pour importer l'agent
sys.path.insert(0, str(Path(__file__).parent))

from src.core.agent import JarvisAgent
from src.core.logger import init_logger_from_config
from src.core.config import get_config


class JarvisWebhook:
    """Webhook pour récupérer et exécuter les commandes depuis l'API."""
    
    def __init__(
        self,
        api_url: str,
        session_cookie: str,
        poll_interval: int = 5
    ):
        """
        Initialise le webhook.
        
        Args:
            api_url: URL de l'API Remote Control
            session_cookie: Cookie de session pour l'authentification
            poll_interval: Intervalle de polling en secondes (défaut: 5)
        """
        self.api_url = api_url.rstrip('/')
        self.session_cookie = session_cookie
        self.poll_interval = poll_interval
        
        # Initialiser l'agent Jarvis
        self.config = get_config()
        self.logger = init_logger_from_config(self.config)
        self.agent = JarvisAgent()
        
        self.logger.info("🔗 Webhook Jarvis initialisé")
        self.logger.info(f"   API: {self.api_url}")
        self.logger.info(f"   Polling: toutes les {self.poll_interval}s")
    
    def get_pending_commands(self) -> List[Dict[str, Any]]:
        """
        Récupère les commandes en attente depuis l'API.
        
        Returns:
            Liste des commandes en attente
        """
        try:
            response = requests.post(
                f"{self.api_url}/api/trpc/jarvis.getPendingCommands",
                headers={
                    "Content-Type": "application/json",
                    "Cookie": f"jarvis_session={self.session_cookie}"
                },
                json={},
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                # tRPC retourne les données dans result.data
                if "result" in data and "data" in data["result"]:
                    return data["result"]["data"]
                return []
            else:
                self.logger.error(f"Erreur API: {response.status_code}")
                return []
                
        except Exception as e:
            self.logger.error(f"Erreur lors de la récupération des commandes: {e}")
            return []
    
    def update_command_status(
        self,
        command_id: int,
        status: str,
        result: str = None,
        error: str = None
    ) -> bool:
        """
        Met à jour le statut d'une commande.
        
        Args:
            command_id: ID de la commande
            status: Nouveau statut (pending, processing, completed, failed)
            result: Résultat de l'exécution (optionnel)
            error: Message d'erreur (optionnel)
            
        Returns:
            True si la mise à jour a réussi
        """
        try:
            payload = {
                "commandId": command_id,
                "status": status
            }
            
            if result is not None:
                payload["result"] = result
            if error is not None:
                payload["error"] = error
            
            response = requests.post(
                f"{self.api_url}/api/trpc/jarvis.updateCommandStatus",
                headers={
                    "Content-Type": "application/json",
                    "Cookie": f"jarvis_session={self.session_cookie}"
                },
                json=payload,
                timeout=10
            )
            
            return response.status_code == 200
            
        except Exception as e:
            self.logger.error(f"Erreur lors de la mise à jour du statut: {e}")
            return False
    
    def execute_command(self, command: Dict[str, Any]) -> Dict[str, Any]:
        """
        Exécute une commande avec l'agent Jarvis.
        
        Args:
            command: Dictionnaire contenant les détails de la commande
            
        Returns:
            Résultat de l'exécution
        """
        command_id = command["id"]
        command_text = command["command"]
        command_type = command["commandType"]
        
        self.logger.section(f"Exécution de la commande #{command_id}")
        self.logger.info(f"Type: {command_type}")
        self.logger.info(f"Commande: {command_text}")
        
        try:
            # Marquer comme "en cours"
            self.update_command_status(command_id, "processing")
            
            # Exécuter selon le type
            if command_type == "build":
                result = self.agent.build(command_text)
            elif command_type == "fix":
                result = self.agent.fix(command_text)
            elif command_type == "analyze":
                result = self.agent.analyze(command_text)
            elif command_type == "refactor":
                result = self.agent.refactor(command_text)
            elif command_type == "ask":
                result = self.agent.ask(command_text)
            elif command_type == "learn":
                result = self.agent.learn(command_text)
            else:
                result = f"Type de commande non supporté: {command_type}"
            
            # Convertir le résultat en chaîne si nécessaire
            if isinstance(result, dict):
                result_str = json.dumps(result, indent=2, ensure_ascii=False)
            else:
                result_str = str(result)
            
            # Marquer comme "terminé"
            self.update_command_status(command_id, "completed", result=result_str)
            
            self.logger.success(f"✓ Commande #{command_id} terminée avec succès")
            
            return {
                "success": True,
                "result": result_str
            }
            
        except Exception as e:
            error_msg = str(e)
            self.logger.error(f"✗ Erreur lors de l'exécution: {error_msg}")
            
            # Marquer comme "échoué"
            self.update_command_status(command_id, "failed", error=error_msg)
            
            return {
                "success": False,
                "error": error_msg
            }
    
    def run(self):
        """Lance le webhook en mode polling continu."""
        self.logger.success("🚀 Webhook Jarvis démarré")
        self.logger.info("En attente de commandes...")
        
        try:
            while True:
                # Récupérer les commandes en attente
                commands = self.get_pending_commands()
                
                if commands:
                    self.logger.info(f"📥 {len(commands)} commande(s) en attente")
                    
                    # Exécuter chaque commande
                    for command in commands:
                        self.execute_command(command)
                
                # Attendre avant le prochain polling
                time.sleep(self.poll_interval)
                
        except KeyboardInterrupt:
            self.logger.info("\n⏹️  Arrêt du webhook...")
        except Exception as e:
            self.logger.error(f"Erreur fatale: {e}")
            raise


def main():
    """Point d'entrée principal."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Webhook pour l'agent Jarvis - Récupère et exécute les commandes depuis l'API"
    )
    parser.add_argument(
        "--api-url",
        type=str,
        required=True,
        help="URL de l'API Remote Control (ex: https://jarvis-api.manus.space)"
    )
    parser.add_argument(
        "--session-cookie",
        type=str,
        required=True,
        help="Cookie de session pour l'authentification"
    )
    parser.add_argument(
        "--interval",
        type=int,
        default=5,
        help="Intervalle de polling en secondes (défaut: 5)"
    )
    
    args = parser.parse_args()
    
    # Créer et lancer le webhook
    webhook = JarvisWebhook(
        api_url=args.api_url,
        session_cookie=args.session_cookie,
        poll_interval=args.interval
    )
    
    webhook.run()


if __name__ == "__main__":
    main()
