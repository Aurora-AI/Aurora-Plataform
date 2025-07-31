"""
Configuration management system for Aurora-Core modules.

This module provides centralized configuration management with validation,
environment-based overrides, and dynamic reconfiguration capabilities.
"""

import json
import logging
import os
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

logger = logging.getLogger(__name__)


class ConfigurationError(Exception):
    """Raised when configuration validation fails."""
    pass


class ConfigurationManager:
    """
    Centralized configuration manager for Aurora modules.
    
    Supports:
    - JSON and environment variable configuration
    - Schema validation
    - Environment-based overrides
    - Dynamic reconfiguration
    """
    
    def __init__(self, config_dir: Optional[Union[str, Path]] = None):
        """
        Initialize configuration manager.
        
        Args:
            config_dir: Directory containing configuration files
        """
        self.config_dir = Path(config_dir) if config_dir else Path("config")
        self._configs: Dict[str, Dict[str, Any]] = {}
        self._schemas: Dict[str, Dict[str, Any]] = {}
        self._watchers: List[callable] = []
        
        logger.info(f"Configuration manager initialized with config dir: {self.config_dir}")
    
    def load_config(self, module_name: str, 
                   config_file: Optional[str] = None) -> Dict[str, Any]:
        """
        Load configuration for a module.
        
        Args:
            module_name: Name of the module
            config_file: Optional config file path (defaults to {module_name}.json)
            
        Returns:
            Configuration dictionary
        """
        if not config_file:
            config_file = f"{module_name}.json"
        
        config_path = self.config_dir / config_file
        config = {}
        
        # Load from file if exists
        if config_path.exists():
            try:
                with open(config_path, 'r') as f:
                    config = json.load(f)
                logger.debug(f"Loaded config for {module_name} from {config_path}")
            except Exception as e:
                logger.error(f"Failed to load config file {config_path}: {e}")
                raise ConfigurationError(f"Invalid config file: {e}")
        
        # Apply environment overrides
        config = self._apply_env_overrides(module_name, config)
        
        # Validate against schema if available
        if module_name in self._schemas:
            self._validate_config(module_name, config)
        
        # Cache configuration
        self._configs[module_name] = config
        
        return config
    
    def save_config(self, module_name: str, config: Dict[str, Any],
                   config_file: Optional[str] = None) -> None:
        """
        Save configuration for a module.
        
        Args:
            module_name: Name of the module
            config: Configuration dictionary
            config_file: Optional config file path
        """
        if not config_file:
            config_file = f"{module_name}.json"
        
        config_path = self.config_dir / config_file
        
        # Ensure config directory exists
        config_path.parent.mkdir(parents=True, exist_ok=True)
        
        try:
            with open(config_path, 'w') as f:
                json.dump(config, f, indent=2)
            
            logger.info(f"Saved config for {module_name} to {config_path}")
            
        except Exception as e:
            logger.error(f"Failed to save config file {config_path}: {e}")
            raise ConfigurationError(f"Failed to save config: {e}")
    
    def register_schema(self, module_name: str, schema: Dict[str, Any]) -> None:
        """
        Register a configuration schema for validation.
        
        Args:
            module_name: Name of the module
            schema: JSON schema for validation
        """
        self._schemas[module_name] = schema
        logger.debug(f"Registered config schema for {module_name}")
    
    def get_config(self, module_name: str, key: Optional[str] = None,
                  default: Any = None) -> Any:
        """
        Get configuration value(s) for a module.
        
        Args:
            module_name: Name of the module
            key: Optional specific key to retrieve
            default: Default value if key not found
            
        Returns:
            Configuration value or full config dict
        """
        if module_name not in self._configs:
            self.load_config(module_name)
        
        config = self._configs.get(module_name, {})
        
        if key is None:
            return config
        
        return config.get(key, default)
    
    def set_config(self, module_name: str, key: str, value: Any,
                  persist: bool = True) -> None:
        """
        Set a configuration value for a module.
        
        Args:
            module_name: Name of the module
            key: Configuration key
            value: Configuration value
            persist: Whether to save to file
        """
        if module_name not in self._configs:
            self._configs[module_name] = {}
        
        self._configs[module_name][key] = value
        
        if persist:
            self.save_config(module_name, self._configs[module_name])
        
        # Notify watchers
        self._notify_watchers(module_name, key, value)
    
    def update_config(self, module_name: str, updates: Dict[str, Any],
                     persist: bool = True) -> None:
        """
        Update multiple configuration values for a module.
        
        Args:
            module_name: Name of the module
            updates: Dictionary of updates
            persist: Whether to save to file
        """
        if module_name not in self._configs:
            self._configs[module_name] = {}
        
        self._configs[module_name].update(updates)
        
        if persist:
            self.save_config(module_name, self._configs[module_name])
        
        # Notify watchers
        for key, value in updates.items():
            self._notify_watchers(module_name, key, value)
    
    def _apply_env_overrides(self, module_name: str, 
                           config: Dict[str, Any]) -> Dict[str, Any]:
        """Apply environment variable overrides to configuration."""
        env_prefix = f"AURORA_{module_name.upper().replace('-', '_')}_"
        
        for key, value in os.environ.items():
            if key.startswith(env_prefix):
                config_key = key[len(env_prefix):].lower()
                
                # Try to parse as JSON, fall back to string
                try:
                    parsed_value = json.loads(value)
                except (json.JSONDecodeError, ValueError):
                    parsed_value = value
                
                config[config_key] = parsed_value
                logger.debug(f"Applied env override: {config_key} = {parsed_value}")
        
        return config
    
    def _validate_config(self, module_name: str, config: Dict[str, Any]) -> None:
        """Validate configuration against registered schema."""
        schema = self._schemas.get(module_name)
        if not schema:
            return
        
        # Simple validation - in production would use jsonschema library
        required_fields = schema.get("required", [])
        
        for field in required_fields:
            if field not in config:
                raise ConfigurationError(f"Required field '{field}' missing in {module_name} config")
        
        logger.debug(f"Config validation passed for {module_name}")
    
    def add_watcher(self, callback: callable) -> None:
        """Add a configuration change watcher."""
        self._watchers.append(callback)
    
    def _notify_watchers(self, module_name: str, key: str, value: Any) -> None:
        """Notify watchers of configuration changes."""
        for watcher in self._watchers:
            try:
                watcher(module_name, key, value)
            except Exception as e:
                logger.error(f"Configuration watcher failed: {e}")
    
    def get_all_configs(self) -> Dict[str, Dict[str, Any]]:
        """Get all loaded configurations."""
        return self._configs.copy()
    
    def reload_config(self, module_name: str) -> Dict[str, Any]:
        """Reload configuration from file."""
        if module_name in self._configs:
            del self._configs[module_name]
        
        return self.load_config(module_name)


# Global configuration manager instance
_global_config_manager = ConfigurationManager()


def get_config_manager() -> ConfigurationManager:
    """Get the global configuration manager instance."""
    return _global_config_manager


def get_module_config(module_name: str, key: Optional[str] = None,
                     default: Any = None) -> Any:
    """Convenience function to get module configuration."""
    return _global_config_manager.get_config(module_name, key, default)


def set_module_config(module_name: str, key: str, value: Any,
                     persist: bool = True) -> None:
    """Convenience function to set module configuration."""
    _global_config_manager.set_config(module_name, key, value, persist)