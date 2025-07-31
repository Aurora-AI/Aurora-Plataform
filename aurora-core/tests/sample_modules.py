"""
Sample module implementations demonstrating the Aurora-Core modular architecture.

These modules show how to implement and integrate with the module system.
"""

import asyncio
import logging
from typing import Any, Dict

from src.aurora_platform.core.modules.registry import AuroraModule, ModuleInfo, ModuleStatus, ModuleType
from src.aurora_platform.core.router import BaseIntentRouter, IntentContext, RouteConfidence, RoutingResult

logger = logging.getLogger(__name__)


class SampleAnalyticsModule(AuroraModule):
    """Sample analytics module for tracking and metrics."""
    
    def __init__(self):
        self.metrics: Dict[str, int] = {}
        self.is_initialized = False
    
    def get_module_info(self) -> ModuleInfo:
        """Return module information."""
        return ModuleInfo(
            name="sample_analytics",
            module_type=ModuleType.ANALYTICS,
            version="1.0.0",
            description="Sample analytics module for tracking system metrics",
            author="Aurora Team",
            capabilities=["event_tracking", "metrics_collection", "performance_monitoring"]
        )
    
    async def initialize(self, config: Dict[str, Any]) -> None:
        """Initialize the analytics module."""
        logger.info("Initializing sample analytics module")
        
        # Simulate initialization work
        await asyncio.sleep(0.1)
        
        self.metrics = {
            "events_tracked": 0,
            "queries_processed": 0,
            "errors_logged": 0
        }
        
        self.is_initialized = True
        logger.info("Sample analytics module initialized successfully")
    
    async def shutdown(self) -> None:
        """Shutdown the module."""
        logger.info("Shutting down sample analytics module")
        self.is_initialized = False
        self.metrics.clear()
    
    def is_healthy(self) -> bool:
        """Check module health."""
        return self.is_initialized
    
    def track_event(self, event_name: str, data: Dict[str, Any] = None) -> None:
        """Track an event."""
        if not self.is_initialized:
            return
        
        self.metrics["events_tracked"] += 1
        logger.debug(f"Tracked event: {event_name}")
    
    def increment_query_count(self) -> None:
        """Increment query counter."""
        if self.is_initialized:
            self.metrics["queries_processed"] += 1
    
    def log_error(self, error: str) -> None:
        """Log an error."""
        if self.is_initialized:
            self.metrics["errors_logged"] += 1
            logger.warning(f"Analytics module logged error: {error}")
    
    def get_metrics(self) -> Dict[str, Any]:
        """Get current metrics."""
        return {
            "metrics": self.metrics.copy(),
            "health": self.is_healthy(),
            "initialized": self.is_initialized
        }


class SampleMLIntentRouter(BaseIntentRouter, AuroraModule):
    """Sample ML-based intent router module."""
    
    def __init__(self):
        BaseIntentRouter.__init__(self, "sample_ml_router")
        self.model_loaded = False
        self.confidence_threshold = 0.8
        self._routes = [
            "technical_support",
            "billing_inquiry", 
            "product_information",
            "general_conversation"
        ]
    
    def get_module_info(self) -> ModuleInfo:
        """Return module information."""
        return ModuleInfo(
            name="sample_ml_router",
            module_type=ModuleType.ROUTER,
            version="1.0.0",
            description="Sample ML-based intent router using mock predictions",
            author="Aurora Team",
            dependencies=["sample_analytics"],
            capabilities=["intent_classification", "confidence_scoring", "multi_language"]
        )
    
    async def initialize(self, config: Dict[str, Any]) -> None:
        """Initialize the ML router."""
        logger.info("Initializing sample ML intent router")
        
        # Simulate model loading
        await asyncio.sleep(0.2)
        
        self.confidence_threshold = config.get("confidence_threshold", 0.8)
        self.model_loaded = True
        
        logger.info("Sample ML intent router initialized successfully")
    
    async def shutdown(self) -> None:
        """Shutdown the module."""
        logger.info("Shutting down sample ML intent router")
        self.model_loaded = False
    
    def is_healthy(self) -> bool:
        """Check module health."""
        return self.model_loaded
    
    def route(self, context: IntentContext) -> RoutingResult:
        """Route intent using mock ML predictions."""
        if not self.model_loaded:
            return RoutingResult(
                route="general_conversation",
                confidence=RouteConfidence.UNKNOWN,
                score=0.0,
                reasoning="ML model not loaded"
            )
        
        # Mock ML prediction based on simple keywords
        user_input = context.user_input.lower()
        
        if any(word in user_input for word in ["support", "help", "problem", "issue"]):
            return RoutingResult(
                route="technical_support",
                confidence=RouteConfidence.HIGH,
                score=0.92,
                metadata={"model": "mock_ml", "features_used": ["keywords"]},
                reasoning="High confidence technical support classification"
            )
        elif any(word in user_input for word in ["billing", "payment", "invoice", "charge"]):
            return RoutingResult(
                route="billing_inquiry",
                confidence=RouteConfidence.HIGH,
                score=0.88,
                metadata={"model": "mock_ml", "features_used": ["keywords"]},
                reasoning="High confidence billing inquiry classification"
            )
        elif any(word in user_input for word in ["product", "feature", "pricing", "demo"]):
            return RoutingResult(
                route="product_information",
                confidence=RouteConfidence.MEDIUM,
                score=0.75,
                metadata={"model": "mock_ml", "features_used": ["keywords"]},
                reasoning="Medium confidence product information classification"
            )
        else:
            return RoutingResult(
                route="general_conversation",
                confidence=RouteConfidence.LOW,
                score=0.45,
                metadata={"model": "mock_ml", "features_used": ["default"]},
                reasoning="Low confidence, defaulting to general conversation"
            )
    
    def get_available_routes(self) -> list:
        """Get available routes."""
        return self._routes.copy()
    
    def get_metrics(self) -> Dict[str, Any]:
        """Get router metrics."""
        return {
            "model_loaded": self.model_loaded,
            "confidence_threshold": self.confidence_threshold,
            "available_routes": len(self._routes),
            "health": self.is_healthy()
        }


class SampleProcessingPipeline(AuroraModule):
    """Sample document processing pipeline module."""
    
    def __init__(self):
        self.processors = []
        self.is_active = False
    
    def get_module_info(self) -> ModuleInfo:
        """Return module information."""
        return ModuleInfo(
            name="sample_processing_pipeline",
            module_type=ModuleType.PROCESSING_PIPELINE,
            version="1.0.0",
            description="Sample document processing pipeline with multiple stages",
            author="Aurora Team",
            capabilities=["text_extraction", "preprocessing", "enrichment", "validation"]
        )
    
    async def initialize(self, config: Dict[str, Any]) -> None:
        """Initialize the processing pipeline."""
        logger.info("Initializing sample processing pipeline")
        
        # Setup processing stages
        self.processors = [
            "text_extractor",
            "language_detector", 
            "preprocessor",
            "enricher",
            "validator"
        ]
        
        self.is_active = True
        logger.info("Sample processing pipeline initialized successfully")
    
    async def shutdown(self) -> None:
        """Shutdown the module."""
        logger.info("Shutting down sample processing pipeline")
        self.is_active = False
        self.processors.clear()
    
    def is_healthy(self) -> bool:
        """Check module health."""
        return self.is_active and len(self.processors) > 0
    
    async def process_document(self, document: str) -> Dict[str, Any]:
        """Process a document through the pipeline."""
        if not self.is_active:
            raise RuntimeError("Processing pipeline not active")
        
        result = {
            "original": document,
            "processed": True,
            "stages_completed": [],
            "metadata": {}
        }
        
        # Simulate processing stages
        for processor in self.processors:
            await asyncio.sleep(0.01)  # Simulate processing time
            result["stages_completed"].append(processor)
            
            # Add some mock metadata
            if processor == "language_detector":
                result["metadata"]["language"] = "en"
            elif processor == "preprocessor":
                result["metadata"]["word_count"] = len(document.split())
        
        logger.debug(f"Document processed through {len(self.processors)} stages")
        return result
    
    def get_metrics(self) -> Dict[str, Any]:
        """Get pipeline metrics."""
        return {
            "active": self.is_active,
            "processors_count": len(self.processors),
            "processors": self.processors.copy(),
            "health": self.is_healthy()
        }