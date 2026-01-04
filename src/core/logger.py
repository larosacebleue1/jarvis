"""
Module de gestion de la journalisation de l'agent AMIKAL.
"""

import logging
import sys
from pathlib import Path
from datetime import datetime
from typing import Optional
from rich.console import Console
from rich.logging import RichHandler


class Logger:
    """Gestionnaire de journalisation pour l'agent AMIKAL."""
    
    def __init__(self, name: str = "amikal-agent", log_file: Optional[str] = None, 
                 level: str = "INFO", console_output: bool = True):
        """
        Initialise le logger.
        
        Args:
            name: Nom du logger
            log_file: Chemin vers le fichier de log
            level: Niveau de journalisation (DEBUG, INFO, WARNING, ERROR)
            console_output: Afficher les logs dans la console
        """
        self.name = name
        self.log_file = log_file
        self.level = getattr(logging, level.upper(), logging.INFO)
        self.console_output = console_output
        
        # Console Rich pour un affichage amélioré
        self.console = Console()
        
        # Configuration du logger
        self.logger = logging.getLogger(name)
        self.logger.setLevel(self.level)
        self.logger.handlers.clear()
        
        # Handler pour la console avec Rich
        if console_output:
            console_handler = RichHandler(
                console=self.console,
                show_time=True,
                show_path=False,
                rich_tracebacks=True
            )
            console_handler.setLevel(self.level)
            console_formatter = logging.Formatter(
                "%(message)s",
                datefmt="[%X]"
            )
            console_handler.setFormatter(console_formatter)
            self.logger.addHandler(console_handler)
        
        # Handler pour le fichier
        if log_file:
            log_path = Path(log_file)
            log_path.parent.mkdir(parents=True, exist_ok=True)
            
            file_handler = logging.FileHandler(log_file, encoding='utf-8')
            file_handler.setLevel(self.level)
            file_formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                datefmt='%Y-%m-%d %H:%M:%S'
            )
            file_handler.setFormatter(file_formatter)
            self.logger.addHandler(file_handler)
    
    def debug(self, message: str):
        """Log un message de debug."""
        self.logger.debug(message)
    
    def info(self, message: str):
        """Log un message d'information."""
        self.logger.info(message)
    
    def warning(self, message: str):
        """Log un avertissement."""
        self.logger.warning(message)
    
    def error(self, message: str):
        """Log une erreur."""
        self.logger.error(message)
    
    def critical(self, message: str):
        """Log une erreur critique."""
        self.logger.critical(message)
    
    def success(self, message: str):
        """Log un message de succès (info avec style)."""
        self.logger.info(f"✓ {message}")
    
    def action(self, message: str):
        """Log une action en cours."""
        self.logger.info(f"→ {message}")
    
    def section(self, title: str):
        """Log un titre de section."""
        separator = "=" * 60
        self.logger.info(f"\n{separator}")
        self.logger.info(f"  {title}")
        self.logger.info(f"{separator}\n")


# Instance globale du logger
_logger_instance: Optional[Logger] = None


def get_logger(name: str = "amikal-agent", log_file: Optional[str] = None,
               level: str = "INFO", console_output: bool = True) -> Logger:
    """
    Retourne l'instance globale du logger.
    
    Args:
        name: Nom du logger
        log_file: Chemin vers le fichier de log
        level: Niveau de journalisation
        console_output: Afficher les logs dans la console
        
    Returns:
        Instance de Logger
    """
    global _logger_instance
    
    if _logger_instance is None:
        _logger_instance = Logger(name, log_file, level, console_output)
    
    return _logger_instance


def init_logger_from_config(config):
    """
    Initialise le logger à partir de la configuration.
    
    Args:
        config: Instance de Config
        
    Returns:
        Instance de Logger
    """
    log_file = config.get_base_dir() / config.logging.file
    return get_logger(
        name="amikal-agent",
        log_file=str(log_file),
        level=config.logging.level,
        console_output=config.logging.console_output
    )
