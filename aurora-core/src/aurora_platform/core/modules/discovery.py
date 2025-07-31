"""
Service discovery and dependency injection system for Aurora-Core.

This module provides service discovery, dependency injection, and
lifecycle management for Aurora modules and services.
"""

import logging
from typing import Any, Dict, List, Optional, Type, TypeVar, Union

from .registry import AuroraModule, ModuleInfo, ModuleRegistry, ModuleStatus, ModuleType

logger = logging.getLogger(__name__)

T = TypeVar('T')


class ServiceNotFoundError(Exception):
    """Raised when a requested service is not found."""
    pass


class DependencyInjectionError(Exception):
    """Raised when dependency injection fails."""
    pass


class ServiceContainer:
    """
    Service container for dependency injection and service discovery.
    
    Provides:
    - Service registration and discovery
    - Dependency injection
    - Lifecycle management
    - Service health monitoring
    """
    
    def __init__(self, module_registry: Optional[ModuleRegistry] = None):
        """
        Initialize service container.
        
        Args:
            module_registry: Optional module registry instance
        """
        self.module_registry = module_registry
        self._services: Dict[str, Any] = {}
        self._service_types: Dict[Type, str] = {}
        self._dependencies: Dict[str, List[str]] = {}
        self._singletons: Dict[str, Any] = {}
        
        logger.info("Service container initialized")
    
    def register_service(self, service_name: str, service_instance: Any,
                        service_type: Optional[Type] = None,
                        dependencies: Optional[List[str]] = None) -> None:
        """
        Register a service instance.
        
        Args:
            service_name: Unique service name
            service_instance: Service instance
            service_type: Optional service type for type-based lookup
            dependencies: List of dependency service names
        """
        self._services[service_name] = service_instance
        
        if service_type:
            self._service_types[service_type] = service_name
        
        if dependencies:
            self._dependencies[service_name] = dependencies
        
        logger.info(f"Registered service: {service_name}")
    
    def register_singleton(self, service_name: str, factory: callable,
                          service_type: Optional[Type] = None,
                          dependencies: Optional[List[str]] = None) -> None:
        """
        Register a singleton service factory.
        
        Args:
            service_name: Unique service name
            factory: Factory function to create service instance
            service_type: Optional service type for type-based lookup
            dependencies: List of dependency service names
        """
        # Store factory function
        self._services[service_name] = factory
        
        if service_type:
            self._service_types[service_type] = service_name
        
        if dependencies:
            self._dependencies[service_name] = dependencies
        
        logger.info(f"Registered singleton factory: {service_name}")
    
    def get_service(self, service_name: str) -> Any:
        """
        Get a service instance by name.
        
        Args:
            service_name: Service name
            
        Returns:
            Service instance
            
        Raises:
            ServiceNotFoundError: If service not found
        """
        if service_name not in self._services:
            raise ServiceNotFoundError(f"Service '{service_name}' not found")
        
        service = self._services[service_name]
        
        # Handle singleton pattern
        if callable(service) and service_name not in self._singletons:
            # Create singleton instance
            try:
                instance = self._create_service_instance(service_name, service)
                self._singletons[service_name] = instance
                return instance
            except Exception as e:
                logger.error(f"Failed to create service instance {service_name}: {e}")
                raise DependencyInjectionError(f"Failed to create service: {e}")
        
        if service_name in self._singletons:
            return self._singletons[service_name]
        
        return service
    
    def get_service_by_type(self, service_type: Type[T]) -> T:
        """
        Get a service instance by type.
        
        Args:
            service_type: Service type class
            
        Returns:
            Service instance
            
        Raises:
            ServiceNotFoundError: If service not found
        """
        if service_type not in self._service_types:
            raise ServiceNotFoundError(f"Service of type '{service_type.__name__}' not found")
        
        service_name = self._service_types[service_type]
        return self.get_service(service_name)
    
    def _create_service_instance(self, service_name: str, factory: callable) -> Any:
        """Create service instance with dependency injection."""
        dependencies = self._dependencies.get(service_name, [])
        
        if not dependencies:
            # No dependencies, just call factory
            return factory()
        
        # Resolve dependencies
        resolved_deps = {}
        for dep_name in dependencies:
            try:
                resolved_deps[dep_name] = self.get_service(dep_name)
            except ServiceNotFoundError:
                logger.error(f"Dependency '{dep_name}' not found for service '{service_name}'")
                raise
        
        # Call factory with resolved dependencies
        try:
            return factory(**resolved_deps)
        except TypeError as e:
            # Try positional arguments
            try:
                return factory(*resolved_deps.values())
            except TypeError:
                logger.error(f"Failed to inject dependencies for {service_name}: {e}")
                raise DependencyInjectionError(f"Dependency injection failed: {e}")
    
    def has_service(self, service_name: str) -> bool:
        """Check if a service is registered."""
        return service_name in self._services
    
    def list_services(self) -> List[str]:
        """Get list of all registered services."""
        return list(self._services.keys())
    
    def get_service_dependencies(self, service_name: str) -> List[str]:
        """Get dependencies for a service."""
        return self._dependencies.get(service_name, [])
    
    def remove_service(self, service_name: str) -> bool:
        """
        Remove a service from the container.
        
        Args:
            service_name: Service name
            
        Returns:
            True if removed, False if not found
        """
        if service_name not in self._services:
            return False
        
        # Remove from services
        del self._services[service_name]
        
        # Remove from singletons
        if service_name in self._singletons:
            del self._singletons[service_name]
        
        # Remove from dependencies
        if service_name in self._dependencies:
            del self._dependencies[service_name]
        
        # Remove from type mappings
        type_to_remove = None
        for service_type, name in self._service_types.items():
            if name == service_name:
                type_to_remove = service_type
                break
        
        if type_to_remove:
            del self._service_types[type_to_remove]
        
        logger.info(f"Removed service: {service_name}")
        return True


class AuroraServiceDiscovery:
    """
    Service discovery system that integrates with the module registry.
    
    Provides automatic service registration from modules and
    health monitoring capabilities.
    """
    
    def __init__(self, service_container: ServiceContainer,
                 module_registry: ModuleRegistry):
        """
        Initialize service discovery.
        
        Args:
            service_container: Service container instance
            module_registry: Module registry instance
        """
        self.container = service_container
        self.registry = module_registry
        
        logger.info("Aurora service discovery initialized")
    
    def auto_register_modules(self) -> None:
        """Automatically register active modules as services."""
        active_modules = self.registry.list_modules(status=ModuleStatus.ACTIVE)
        
        for module_info in active_modules:
            if module_info.instance:
                service_name = f"module:{module_info.name}"
                self.container.register_service(
                    service_name=service_name,
                    service_instance=module_info.instance,
                    service_type=type(module_info.instance)
                )
                
                logger.debug(f"Auto-registered module as service: {service_name}")
    
    def discover_services_by_type(self, module_type: ModuleType) -> List[Any]:
        """
        Discover all services of a specific module type.
        
        Args:
            module_type: Type of modules to discover
            
        Returns:
            List of service instances
        """
        services = []
        modules = self.registry.list_modules(module_type=module_type, status=ModuleStatus.ACTIVE)
        
        for module_info in modules:
            if module_info.instance:
                services.append(module_info.instance)
        
        return services
    
    def get_healthy_services(self, service_type: Optional[Type] = None) -> List[Any]:
        """
        Get all healthy services, optionally filtered by type.
        
        Args:
            service_type: Optional service type filter
            
        Returns:
            List of healthy service instances
        """
        healthy_services = []
        
        for service_name in self.container.list_services():
            try:
                service = self.container.get_service(service_name)
                
                # Check type filter
                if service_type and not isinstance(service, service_type):
                    continue
                
                # Check health if module
                if isinstance(service, AuroraModule):
                    if service.is_healthy():
                        healthy_services.append(service)
                else:
                    # Assume healthy if not a module
                    healthy_services.append(service)
                    
            except Exception as e:
                logger.warning(f"Service {service_name} health check failed: {e}")
        
        return healthy_services
    
    def get_service_health_status(self) -> Dict[str, bool]:
        """Get health status for all services."""
        health_status = {}
        
        for service_name in self.container.list_services():
            try:
                service = self.container.get_service(service_name)
                
                if isinstance(service, AuroraModule):
                    health_status[service_name] = service.is_healthy()
                else:
                    health_status[service_name] = True  # Assume healthy
                    
            except Exception:
                health_status[service_name] = False
        
        return health_status


# Global service container and discovery instances
_global_container = ServiceContainer()
_global_discovery: Optional[AuroraServiceDiscovery] = None


def get_service_container() -> ServiceContainer:
    """Get the global service container instance."""
    return _global_container


def get_service_discovery() -> Optional[AuroraServiceDiscovery]:
    """Get the global service discovery instance."""
    return _global_discovery


def initialize_service_discovery(module_registry: ModuleRegistry) -> AuroraServiceDiscovery:
    """
    Initialize global service discovery.
    
    Args:
        module_registry: Module registry instance
        
    Returns:
        Service discovery instance
    """
    global _global_discovery
    _global_discovery = AuroraServiceDiscovery(_global_container, module_registry)
    return _global_discovery


def get_service(service_name: str) -> Any:
    """Convenience function to get a service."""
    return _global_container.get_service(service_name)


def get_service_by_type(service_type: Type[T]) -> T:
    """Convenience function to get a service by type."""
    return _global_container.get_service_by_type(service_type)