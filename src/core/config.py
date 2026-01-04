"""
Module de gestion de la configuration de l'agent AMIKAL.
"""

import os
import yaml
from pathlib import Path
from typing import Dict, Any, List
from dataclasses import dataclass


@dataclass
class LLMConfig:
    """Configuration du modèle LLM."""
    provider: str
    model: str
    temperature: float
    max_tokens: int


@dataclass
class SecurityConfig:
    """Configuration de sécurité."""
    require_confirmation_for_critical_actions: bool
    sandbox_mode: bool
    backup_before_modification: bool
    allowed_directories: List[str]


@dataclass
class KnowledgeBaseConfig:
    """Configuration de la base de connaissances."""
    path: str
    vector_db_enabled: bool
    auto_save: bool


@dataclass
class LoggingConfig:
    """Configuration de la journalisation."""
    level: str
    file: str
    console_output: bool


@dataclass
class InterfaceConfig:
    """Configuration des interfaces."""
    cli_enabled: bool
    api_enabled: bool
    api_port: int
    web_ui_enabled: bool
    web_ui_port: int


@dataclass
class ModulesConfig:
    """Configuration des modules."""
    builder: bool
    fixer: bool
    learner: bool


@dataclass
class TemplatesConfig:
    """Configuration des templates."""
    web_static: bool
    web_dynamic: bool
    api_rest: bool
    cli_tool: bool
    mobile_app: bool


class Config:
    """Classe principale de gestion de la configuration."""
    
    def __init__(self, config_path: str = None):
        """
        Initialise la configuration.
        
        Args:
            config_path: Chemin vers le fichier de configuration YAML
        """
        if config_path is None:
            # Chemin par défaut
            base_dir = Path(__file__).parent.parent.parent
            config_path = base_dir / "config" / "config.yaml"
        
        self.config_path = Path(config_path)
        self._raw_config = self._load_config()
        self._parse_config()
    
    def _load_config(self) -> Dict[str, Any]:
        """Charge le fichier de configuration YAML."""
        if not self.config_path.exists():
            raise FileNotFoundError(f"Fichier de configuration non trouvé : {self.config_path}")
        
        with open(self.config_path, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)
    
    def _parse_config(self):
        """Parse la configuration et crée les objets de configuration."""
        # Configuration LLM
        llm_config = self._raw_config.get('llm', {})
        self.llm = LLMConfig(
            provider=llm_config.get('provider', 'openai'),
            model=llm_config.get('model', 'gpt-4.1-mini'),
            temperature=llm_config.get('temperature', 0.7),
            max_tokens=llm_config.get('max_tokens', 4000)
        )
        
        # Configuration de sécurité
        security_config = self._raw_config.get('security', {})
        self.security = SecurityConfig(
            require_confirmation_for_critical_actions=security_config.get('require_confirmation_for_critical_actions', True),
            sandbox_mode=security_config.get('sandbox_mode', True),
            backup_before_modification=security_config.get('backup_before_modification', True),
            allowed_directories=security_config.get('allowed_directories', [])
        )
        
        # Configuration de la base de connaissances
        kb_config = self._raw_config.get('knowledge_base', {})
        self.knowledge_base = KnowledgeBaseConfig(
            path=kb_config.get('path', './knowledge_base'),
            vector_db_enabled=kb_config.get('vector_db_enabled', True),
            auto_save=kb_config.get('auto_save', True)
        )
        
        # Configuration de la journalisation
        logging_config = self._raw_config.get('logging', {})
        self.logging = LoggingConfig(
            level=logging_config.get('level', 'INFO'),
            file=logging_config.get('file', './logs/amikal-agent.log'),
            console_output=logging_config.get('console_output', True)
        )
        
        # Configuration des interfaces
        interface_config = self._raw_config.get('interface', {})
        self.interface = InterfaceConfig(
            cli_enabled=interface_config.get('cli_enabled', True),
            api_enabled=interface_config.get('api_enabled', False),
            api_port=interface_config.get('api_port', 8000),
            web_ui_enabled=interface_config.get('web_ui_enabled', False),
            web_ui_port=interface_config.get('web_ui_port', 3000)
        )
        
        # Configuration des modules
        modules_config = self._raw_config.get('modules', {})
        self.modules = ModulesConfig(
            builder=modules_config.get('builder', True),
            fixer=modules_config.get('fixer', True),
            learner=modules_config.get('learner', True)
        )
        
        # Configuration des templates
        templates_config = self._raw_config.get('templates', {})
        self.templates = TemplatesConfig(
            web_static=templates_config.get('web_static', True),
            web_dynamic=templates_config.get('web_dynamic', True),
            api_rest=templates_config.get('api_rest', True),
            cli_tool=templates_config.get('cli_tool', True),
            mobile_app=templates_config.get('mobile_app', True)
        )
    
    def get_base_dir(self) -> Path:
        """Retourne le répertoire de base de l'agent."""
        return self.config_path.parent.parent
    
    def get_knowledge_base_path(self) -> Path:
        """Retourne le chemin absolu de la base de connaissances."""
        base_dir = self.get_base_dir()
        return base_dir / self.knowledge_base.path
    
    def get_logs_dir(self) -> Path:
        """Retourne le répertoire des logs."""
        base_dir = self.get_base_dir()
        log_file = Path(self.logging.file)
        return base_dir / log_file.parent
    
    def is_directory_allowed(self, directory: str) -> bool:
        """
        Vérifie si un répertoire est autorisé pour les opérations.
        
        Args:
            directory: Chemin du répertoire à vérifier
            
        Returns:
            True si le répertoire est autorisé, False sinon
        """
        dir_path = Path(directory).resolve()
        
        for allowed_dir in self.security.allowed_directories:
            allowed_path = Path(allowed_dir).resolve()
            try:
                dir_path.relative_to(allowed_path)
                return True
            except ValueError:
                continue
        
        return False
    
    def save(self):
        """Sauvegarde la configuration actuelle dans le fichier YAML."""
        config_dict = {
            'llm': {
                'provider': self.llm.provider,
                'model': self.llm.model,
                'temperature': self.llm.temperature,
                'max_tokens': self.llm.max_tokens
            },
            'security': {
                'require_confirmation_for_critical_actions': self.security.require_confirmation_for_critical_actions,
                'sandbox_mode': self.security.sandbox_mode,
                'backup_before_modification': self.security.backup_before_modification,
                'allowed_directories': self.security.allowed_directories
            },
            'knowledge_base': {
                'path': self.knowledge_base.path,
                'vector_db_enabled': self.knowledge_base.vector_db_enabled,
                'auto_save': self.knowledge_base.auto_save
            },
            'logging': {
                'level': self.logging.level,
                'file': self.logging.file,
                'console_output': self.logging.console_output
            },
            'interface': {
                'cli_enabled': self.interface.cli_enabled,
                'api_enabled': self.interface.api_enabled,
                'api_port': self.interface.api_port,
                'web_ui_enabled': self.interface.web_ui_enabled,
                'web_ui_port': self.interface.web_ui_port
            },
            'modules': {
                'builder': self.modules.builder,
                'fixer': self.modules.fixer,
                'learner': self.modules.learner
            },
            'templates': {
                'web_static': self.templates.web_static,
                'web_dynamic': self.templates.web_dynamic,
                'api_rest': self.templates.api_rest,
                'cli_tool': self.templates.cli_tool,
                'mobile_app': self.templates.mobile_app
            }
        }
        
        with open(self.config_path, 'w', encoding='utf-8') as f:
            yaml.dump(config_dict, f, default_flow_style=False, allow_unicode=True)


# Instance globale de configuration
_config_instance = None


def get_config(config_path: str = None) -> Config:
    """
    Retourne l'instance globale de configuration.
    
    Args:
        config_path: Chemin vers le fichier de configuration (optionnel)
        
    Returns:
        Instance de Config
    """
    global _config_instance
    
    if _config_instance is None:
        _config_instance = Config(config_path)
    
    return _config_instance
