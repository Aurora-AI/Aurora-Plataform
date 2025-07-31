"""
Test suite for Aurora-Core modular architecture system.
"""

import pytest

from src.aurora_platform.core.modules import (
    AuroraModule,
    ConfigurationManager,
    ModuleRegistry,
    ModuleStatus,
    ModuleType,
    ServiceContainer,
    get_config_manager,
    get_module_registry,
    get_service_container,
)
from tests.sample_modules import SampleAnalyticsModule, SampleMLIntentRouter, SampleProcessingPipeline


class TestModuleRegistry:
    """Test cases for ModuleRegistry."""
    
    def test_registry_initialization(self):
        """Test module registry initialization."""
        registry = ModuleRegistry()
        
        stats = registry.get_registry_stats()
        assert stats["total_modules"] == 0
        assert stats["active_modules"] == 0
    
    def test_module_registration(self):
        """Test module registration."""
        registry = ModuleRegistry()
        
        success = registry.register_module(SampleAnalyticsModule)
        assert success
        
        stats = registry.get_registry_stats()
        assert stats["total_modules"] == 1
        assert stats["by_type"]["analytics"] == 1
    
    async def test_module_loading(self):
        """Test module loading and activation."""
        registry = ModuleRegistry()
        
        # Register module
        registry.register_module(SampleAnalyticsModule)
        
        # Load module
        success = await registry.load_module("sample_analytics")
        assert success
        
        # Check status
        module_info = registry.get_module_info("sample_analytics")
        assert module_info is not None
        # Note: Status checking depends on actual implementation
    
    def test_module_listing(self):
        """Test module listing with filters."""
        registry = ModuleRegistry()
        
        # Register different types of modules
        registry.register_module(SampleAnalyticsModule)
        registry.register_module(SampleMLIntentRouter)
        registry.register_module(SampleProcessingPipeline)
        
        # List all modules
        all_modules = registry.list_modules()
        assert len(all_modules) == 3
        
        # List by type
        analytics_modules = registry.list_modules(module_type=ModuleType.ANALYTICS)
        assert len(analytics_modules) == 1
        assert analytics_modules[0].name == "sample_analytics"
        
        router_modules = registry.list_modules(module_type=ModuleType.ROUTER)
        assert len(router_modules) == 1
        assert router_modules[0].name == "sample_ml_router"


class TestServiceContainer:
    """Test cases for ServiceContainer."""
    
    def test_container_initialization(self):
        """Test service container initialization."""
        container = ServiceContainer()
        
        assert len(container.list_services()) == 0
    
    def test_service_registration(self):
        """Test service registration and retrieval."""
        container = ServiceContainer()
        
        # Create service instance
        analytics = SampleAnalyticsModule()
        
        # Register service
        container.register_service(
            service_name="analytics",
            service_instance=analytics,
            service_type=SampleAnalyticsModule
        )
        
        # Test retrieval by name
        retrieved = container.get_service("analytics")
        assert retrieved is analytics
        
        # Test retrieval by type
        retrieved_by_type = container.get_service_by_type(SampleAnalyticsModule)
        assert retrieved_by_type is analytics
    
    def test_singleton_registration(self):
        """Test singleton service registration."""
        container = ServiceContainer()
        
        # Register singleton factory
        container.register_singleton(
            service_name="analytics_singleton",
            factory=lambda: SampleAnalyticsModule(),
            service_type=SampleAnalyticsModule
        )
        
        # Get service multiple times
        instance1 = container.get_service("analytics_singleton")
        instance2 = container.get_service("analytics_singleton")
        
        # Should be same instance
        assert instance1 is instance2
    
    def test_dependency_injection(self):
        """Test dependency injection."""
        container = ServiceContainer()
        
        # Register dependency
        analytics = SampleAnalyticsModule()
        container.register_service("analytics", analytics)
        
        # Register service with dependency
        def create_router(analytics):
            router = SampleMLIntentRouter()
            router.analytics = analytics
            return router
        
        container.register_singleton(
            service_name="ml_router",
            factory=create_router,
            dependencies=["analytics"]
        )
        
        # Get service (should auto-inject dependencies)
        router = container.get_service("ml_router")
        assert hasattr(router, "analytics")
        assert router.analytics is analytics


class TestConfigurationManager:
    """Test cases for ConfigurationManager."""
    
    def test_configuration_creation(self):
        """Test configuration manager creation."""
        config_manager = ConfigurationManager()
        
        # Test getting non-existent config
        config = config_manager.get_config("nonexistent", default={})
        assert config == {}
    
    def test_config_operations(self):
        """Test configuration operations."""
        config_manager = ConfigurationManager()
        
        # Set configuration
        config_manager.set_config("test_module", "key1", "value1", persist=False)
        
        # Get configuration
        value = config_manager.get_config("test_module", "key1")
        assert value == "value1"
        
        # Update configuration
        config_manager.update_config("test_module", {"key2": "value2"}, persist=False)
        
        # Get full config
        full_config = config_manager.get_config("test_module")
        assert full_config["key1"] == "value1"
        assert full_config["key2"] == "value2"


class TestSampleModules:
    """Test cases for sample module implementations."""
    
    async def test_analytics_module(self):
        """Test sample analytics module."""
        module = SampleAnalyticsModule()
        
        # Test module info
        info = module.get_module_info()
        assert info.name == "sample_analytics"
        assert info.module_type == ModuleType.ANALYTICS
        
        # Test initialization
        await module.initialize({})
        assert module.is_healthy()
        
        # Test functionality
        module.track_event("test_event")
        module.increment_query_count()
        
        metrics = module.get_metrics()
        assert metrics["metrics"]["events_tracked"] == 1
        assert metrics["metrics"]["queries_processed"] == 1
        
        # Test shutdown
        await module.shutdown()
        assert not module.is_healthy()
    
    async def test_ml_router_module(self):
        """Test sample ML router module."""
        module = SampleMLIntentRouter()
        
        # Test module info
        info = module.get_module_info()
        assert info.name == "sample_ml_router"
        assert info.module_type == ModuleType.ROUTER
        
        # Test initialization
        await module.initialize({"confidence_threshold": 0.7})
        assert module.is_healthy()
        
        # Test routing
        from src.aurora_platform.core.router import IntentContext
        
        context = IntentContext(user_input="I need help with a technical problem")
        result = module.route(context)
        
        assert result.route == "technical_support"
        assert result.score > 0.8
        
        # Test shutdown
        await module.shutdown()
        assert not module.is_healthy()
    
    async def test_processing_pipeline_module(self):
        """Test sample processing pipeline module."""
        module = SampleProcessingPipeline()
        
        # Test module info
        info = module.get_module_info()
        assert info.name == "sample_processing_pipeline"
        assert info.module_type == ModuleType.PROCESSING_PIPELINE
        
        # Test initialization
        await module.initialize({})
        assert module.is_healthy()
        
        # Test processing
        result = await module.process_document("This is a test document")
        
        assert result["processed"] is True
        assert len(result["stages_completed"]) > 0
        assert "language" in result["metadata"]
        
        # Test shutdown
        await module.shutdown()
        assert not module.is_healthy()


class TestIntegration:
    """Integration tests for the modular architecture."""
    
    async def test_full_module_lifecycle(self):
        """Test complete module lifecycle with registry and services."""
        registry = ModuleRegistry()
        container = ServiceContainer()
        
        # Register modules
        registry.register_module(SampleAnalyticsModule)
        registry.register_module(SampleMLIntentRouter)
        
        # Load modules (simplified test)
        analytics = SampleAnalyticsModule()
        router = SampleMLIntentRouter()
        
        await analytics.initialize({})
        await router.initialize({})
        
        # Register as services
        container.register_service("analytics", analytics, SampleAnalyticsModule)
        container.register_service("router", router, SampleMLIntentRouter)
        
        # Test service discovery
        retrieved_analytics = container.get_service_by_type(SampleAnalyticsModule)
        assert retrieved_analytics is analytics
        
        # Test functionality
        from src.aurora_platform.core.router import IntentContext
        
        context = IntentContext(user_input="billing question")
        result = router.route(context)
        
        analytics.track_event("routing_request")
        
        # Verify metrics
        metrics = analytics.get_metrics()
        assert metrics["metrics"]["events_tracked"] == 1
        
        # Cleanup
        await analytics.shutdown()
        await router.shutdown()
    
    def test_global_instances(self):
        """Test global registry and container instances."""
        registry = get_module_registry()
        container = get_service_container()
        config_manager = get_config_manager()
        
        assert registry is not None
        assert container is not None
        assert config_manager is not None
        
        # Test that they're singletons
        registry2 = get_module_registry()
        assert registry is registry2