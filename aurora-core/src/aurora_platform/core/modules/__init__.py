# Aurora-Core Modular Architecture System
#
# This module provides a plugin-based architecture for advanced AI modules,
# enabling modular development and extension of Aurora-Core capabilities

from .config import (
    ConfigurationError,
    ConfigurationManager,
    get_config_manager,
    get_module_config,
    set_module_config,
)
from .discovery import (
    AuroraServiceDiscovery,
    DependencyInjectionError,
    ServiceContainer,
    ServiceNotFoundError,
    get_service,
    get_service_by_type,
    get_service_container,
    get_service_discovery,
    initialize_service_discovery,
)
from .registry import (
    AuroraModule,
    ModuleInfo,
    ModuleRegistry,
    ModuleStatus,
    ModuleType,
    get_module_registry,
    load_module,
    register_module,
)

__all__ = [
    # Module registry
    "AuroraModule",
    "ModuleInfo", 
    "ModuleRegistry",
    "ModuleType",
    "ModuleStatus",
    "get_module_registry",
    "register_module",
    "load_module",
    
    # Service discovery and DI
    "ServiceContainer",
    "AuroraServiceDiscovery", 
    "ServiceNotFoundError",
    "DependencyInjectionError",
    "get_service_container",
    "get_service_discovery",
    "initialize_service_discovery",
    "get_service",
    "get_service_by_type",
    
    # Configuration management
    "ConfigurationManager",
    "ConfigurationError",
    "get_config_manager",
    "get_module_config",
    "set_module_config",
]