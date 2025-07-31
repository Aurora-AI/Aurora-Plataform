"""
Module registry and plugin system for Aurora-Core.

This module provides the foundation for a modular, extensible architecture
that allows dynamic loading and management of AI modules.
"""

import logging
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional, Type

logger = logging.getLogger(__name__)


class ModuleType(Enum):
    """Types of Aurora modules."""
    ROUTER = "router"
    KNOWLEDGE_PROVIDER = "knowledge_provider"
    SEARCH_PROVIDER = "search_provider"
    RERANKING_PROVIDER = "reranking_provider"
    LLM_ADAPTER = "llm_adapter"
    PROCESSING_PIPELINE = "processing_pipeline"
    ANALYTICS = "analytics"
    INTEGRATION = "integration"


class ModuleStatus(Enum):
    """Module status indicators."""
    UNLOADED = "unloaded"
    LOADING = "loading"
    LOADED = "loaded"
    ACTIVE = "active"
    ERROR = "error"
    DISABLED = "disabled"


@dataclass
class ModuleInfo:
    """Information about a registered module."""
    name: str
    module_type: ModuleType
    version: str
    description: str
    author: Optional[str] = None
    dependencies: List[str] = field(default_factory=list)
    config_schema: Optional[Dict[str, Any]] = None
    capabilities: List[str] = field(default_factory=list)
    status: ModuleStatus = ModuleStatus.UNLOADED
    instance: Optional[Any] = None
    error_message: Optional[str] = None


class AuroraModule(ABC):
    """Base class for all Aurora modules."""
    
    @abstractmethod
    def get_module_info(self) -> ModuleInfo:
        """Return module information."""
        pass
    
    @abstractmethod
    async def initialize(self, config: Dict[str, Any]) -> None:
        """Initialize the module with configuration."""
        pass
    
    @abstractmethod
    async def shutdown(self) -> None:
        """Shutdown the module and clean up resources."""
        pass
    
    @abstractmethod
    def is_healthy(self) -> bool:
        """Check if the module is healthy and ready to serve requests."""
        pass
    
    def validate_config(self, config: Dict[str, Any]) -> bool:
        """Validate module configuration. Override if needed."""
        return True
    
    def get_metrics(self) -> Dict[str, Any]:
        """Get module performance metrics. Override if needed."""
        return {}


class ModuleRegistry:
    """Registry for managing Aurora modules."""
    
    def __init__(self):
        self._modules: Dict[str, ModuleInfo] = {}
        self._active_modules: Dict[str, AuroraModule] = {}
        self._module_types: Dict[ModuleType, List[str]] = {}
        
        # Initialize module type lists
        for module_type in ModuleType:
            self._module_types[module_type] = []
        
        logger.info("Module registry initialized")
    
    def register_module(self, module_class: Type[AuroraModule], 
                       config: Optional[Dict[str, Any]] = None) -> bool:
        """
        Register a module class.
        
        Args:
            module_class: The module class to register
            config: Optional configuration for the module
            
        Returns:
            True if registration successful, False otherwise
        """
        try:
            # Create temporary instance to get module info
            temp_instance = module_class()
            module_info = temp_instance.get_module_info()
            
            # Validate module info
            if not module_info.name:
                logger.error("Module name cannot be empty")
                return False
            
            if module_info.name in self._modules:
                logger.warning(f"Module {module_info.name} already registered, updating")
            
            # Store module info
            self._modules[module_info.name] = module_info
            self._module_types[module_info.module_type].append(module_info.name)
            
            logger.info(f"Registered module: {module_info.name} ({module_info.module_type.value})")
            return True
            
        except Exception as e:
            logger.error(f"Failed to register module {module_class.__name__}: {e}")
            return False
    
    async def load_module(self, module_name: str, 
                         config: Optional[Dict[str, Any]] = None) -> bool:
        """
        Load and initialize a module.
        
        Args:
            module_name: Name of the module to load
            config: Configuration for the module
            
        Returns:
            True if loading successful, False otherwise
        """
        if module_name not in self._modules:
            logger.error(f"Module {module_name} not found in registry")
            return False
        
        module_info = self._modules[module_name]
        
        if module_info.status == ModuleStatus.ACTIVE:
            logger.warning(f"Module {module_name} already active")
            return True
        
        try:
            module_info.status = ModuleStatus.LOADING
            
            # Create module instance
            # Note: In a real implementation, this would use a module factory
            # or dynamic loading mechanism
            logger.info(f"Loading module: {module_name}")
            
            # For now, we'll use a placeholder that marks the module as loaded
            # In production, this would instantiate the actual module class
            module_info.status = ModuleStatus.LOADED
            
            # Initialize module
            if config and hasattr(module_info, 'instance') and module_info.instance:
                await module_info.instance.initialize(config)
            
            module_info.status = ModuleStatus.ACTIVE
            logger.info(f"Module {module_name} loaded and activated successfully")
            return True
            
        except Exception as e:
            module_info.status = ModuleStatus.ERROR
            module_info.error_message = str(e)
            logger.error(f"Failed to load module {module_name}: {e}")
            return False
    
    async def unload_module(self, module_name: str) -> bool:
        """
        Unload a module.
        
        Args:
            module_name: Name of the module to unload
            
        Returns:
            True if unloading successful, False otherwise
        """
        if module_name not in self._modules:
            logger.error(f"Module {module_name} not found")
            return False
        
        module_info = self._modules[module_name]
        
        try:
            if module_info.instance:
                await module_info.instance.shutdown()
                module_info.instance = None
            
            module_info.status = ModuleStatus.UNLOADED
            module_info.error_message = None
            
            if module_name in self._active_modules:
                del self._active_modules[module_name]
            
            logger.info(f"Module {module_name} unloaded successfully")
            return True
            
        except Exception as e:
            logger.error(f"Failed to unload module {module_name}: {e}")
            module_info.status = ModuleStatus.ERROR
            module_info.error_message = str(e)
            return False
    
    def get_module_info(self, module_name: str) -> Optional[ModuleInfo]:
        """Get information about a specific module."""
        return self._modules.get(module_name)
    
    def list_modules(self, module_type: Optional[ModuleType] = None, 
                    status: Optional[ModuleStatus] = None) -> List[ModuleInfo]:
        """
        List modules with optional filtering.
        
        Args:
            module_type: Filter by module type
            status: Filter by status
            
        Returns:
            List of module info objects
        """
        modules = list(self._modules.values())
        
        if module_type:
            modules = [m for m in modules if m.module_type == module_type]
        
        if status:
            modules = [m for m in modules if m.status == status]
        
        return modules
    
    def get_active_modules_by_type(self, module_type: ModuleType) -> List[AuroraModule]:
        """Get all active modules of a specific type."""
        active_modules = []
        
        for module_name in self._module_types.get(module_type, []):
            module_info = self._modules.get(module_name)
            if module_info and module_info.status == ModuleStatus.ACTIVE and module_info.instance:
                active_modules.append(module_info.instance)
        
        return active_modules
    
    def get_registry_stats(self) -> Dict[str, Any]:
        """Get statistics about the module registry."""
        stats = {
            "total_modules": len(self._modules),
            "by_type": {},
            "by_status": {},
            "active_modules": len(self._active_modules)
        }
        
        # Count by type
        for module_type in ModuleType:
            stats["by_type"][module_type.value] = len(self._module_types[module_type])
        
        # Count by status
        for status in ModuleStatus:
            count = sum(1 for m in self._modules.values() if m.status == status)
            stats["by_status"][status.value] = count
        
        return stats


# Global module registry instance
_global_registry = ModuleRegistry()


def get_module_registry() -> ModuleRegistry:
    """Get the global module registry instance."""
    return _global_registry


def register_module(module_class: Type[AuroraModule], 
                   config: Optional[Dict[str, Any]] = None) -> bool:
    """Convenience function to register a module."""
    return _global_registry.register_module(module_class, config)


async def load_module(module_name: str, 
                     config: Optional[Dict[str, Any]] = None) -> bool:
    """Convenience function to load a module."""
    return await _global_registry.load_module(module_name, config)