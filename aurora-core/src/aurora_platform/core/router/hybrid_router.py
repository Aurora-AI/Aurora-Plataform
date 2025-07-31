"""
Hybrid Intent Router for Aurora-Core.

This is the main router implementation that combines multiple routing
strategies with fallback mechanisms and confidence-based decision making.
"""

import logging
from typing import List, Optional

from .interfaces import BaseIntentRouter, IntentContext, RouteConfidence, RoutingResult
from .rule_based_router import RuleBasedRouter

logger = logging.getLogger(__name__)


class HybridIntentRouter(BaseIntentRouter):
    """
    Hybrid intent router that combines multiple routing strategies.
    
    This router uses a primary strategy (e.g., ML-based) and falls back
    to rule-based routing when confidence is low or primary fails.
    """
    
    def __init__(self, name: str = "hybrid_intent_router"):
        super().__init__(name)
        self._primary_router: Optional[BaseIntentRouter] = None
        self._fallback_router: RuleBasedRouter = RuleBasedRouter("fallback_rule_router")
        self._confidence_threshold = 0.6
        self._available_routes: List[str] = []
        self._update_available_routes()
    
    def set_primary_router(self, router: BaseIntentRouter) -> None:
        """Set the primary router (e.g., ML-based router)."""
        self._primary_router = router
        self._update_available_routes()
        logger.info(f"Primary router set to: {router.get_router_name()}")
    
    def set_confidence_threshold(self, threshold: float) -> None:
        """Set the confidence threshold for fallback decisions."""
        if 0.0 <= threshold <= 1.0:
            self._confidence_threshold = threshold
            logger.info(f"Confidence threshold set to: {threshold}")
        else:
            raise ValueError("Confidence threshold must be between 0.0 and 1.0")
    
    def _update_available_routes(self) -> None:
        """Update the list of available routes from all routers."""
        routes = set(self._fallback_router.get_available_routes())
        
        if self._primary_router:
            routes.update(self._primary_router.get_available_routes())
        
        self._available_routes = list(routes)
    
    def route(self, context: IntentContext) -> RoutingResult:
        """Route intent using hybrid strategy with fallback."""
        logger.debug(f"Routing request: {context.user_input[:100]}...")
        
        primary_result = None
        fallback_used = False
        
        # Try primary router first (if available)
        if self._primary_router:
            try:
                primary_result = self._primary_router.route(context)
                logger.debug(f"Primary router result: {primary_result.route} (confidence: {primary_result.confidence}, score: {primary_result.score})")
                
                # Use primary result if confidence is high enough
                if self._is_confident_enough(primary_result):
                    primary_result.metadata = primary_result.metadata or {}
                    primary_result.metadata.update({
                        "hybrid_router_decision": "primary",
                        "primary_router": self._primary_router.get_router_name(),
                        "fallback_available": True
                    })
                    return primary_result
                else:
                    logger.debug(f"Primary router confidence too low ({primary_result.score} < {self._confidence_threshold}), falling back to rule-based")
                    
            except Exception as e:
                logger.warning(f"Primary router failed: {e}, falling back to rule-based")
                primary_result = None
        
        # Use fallback router
        fallback_result = self._fallback_router.route(context)
        fallback_used = True
        
        logger.debug(f"Fallback router result: {fallback_result.route} (confidence: {fallback_result.confidence}, score: {fallback_result.score})")
        
        # Enhance result metadata with hybrid routing information
        fallback_result.metadata = fallback_result.metadata or {}
        fallback_result.metadata.update({
            "hybrid_router_decision": "fallback",
            "fallback_router": self._fallback_router.get_router_name(),
            "primary_available": self._primary_router is not None,
            "primary_failed": primary_result is None,
            "primary_low_confidence": primary_result is not None and not self._is_confident_enough(primary_result)
        })
        
        if primary_result:
            fallback_result.metadata["primary_result"] = {
                "route": primary_result.route,
                "confidence": primary_result.confidence.value,
                "score": primary_result.score
            }
        
        # Update reasoning to include hybrid decision info
        hybrid_reasoning = f"Hybrid routing: Used fallback router ({self._fallback_router.get_router_name()})"
        if fallback_result.reasoning:
            fallback_result.reasoning = f"{hybrid_reasoning} | {fallback_result.reasoning}"
        else:
            fallback_result.reasoning = hybrid_reasoning
        
        return fallback_result
    
    def _is_confident_enough(self, result: RoutingResult) -> bool:
        """Check if a routing result meets the confidence threshold."""
        return (
            result.confidence in [RouteConfidence.HIGH, RouteConfidence.MEDIUM] and
            result.score >= self._confidence_threshold
        )
    
    def get_available_routes(self) -> List[str]:
        """Get all available routes from both primary and fallback routers."""
        return self._available_routes.copy()
    
    def get_router_info(self) -> dict:
        """Get information about the hybrid router configuration."""
        return {
            "name": self.name,
            "primary_router": self._primary_router.get_router_name() if self._primary_router else None,
            "fallback_router": self._fallback_router.get_router_name(),
            "confidence_threshold": self._confidence_threshold,
            "available_routes": len(self._available_routes),
            "routes": self._available_routes
        }


class AuroraRouter:
    """
    Main Aurora routing facade that provides a simple interface to the hybrid routing system.
    
    This is the primary entry point for intent routing in the Aurora platform.
    """
    
    def __init__(self):
        self._hybrid_router = HybridIntentRouter("aurora_main_router")
        logger.info("Aurora Router initialized with hybrid intent routing")
    
    def route_intent(self, user_input: str, session_id: Optional[str] = None, 
                    user_id: Optional[str] = None, **kwargs) -> RoutingResult:
        """
        Route a user intent to the appropriate service/handler.
        
        Args:
            user_input: The user's input text
            session_id: Optional session identifier
            user_id: Optional user identifier
            **kwargs: Additional context parameters
            
        Returns:
            RoutingResult with routing decision and metadata
        """
        context = IntentContext(
            user_input=user_input,
            session_id=session_id,
            user_id=user_id,
            additional_context=kwargs
        )
        
        return self._hybrid_router.route(context)
    
    def set_primary_router(self, router: BaseIntentRouter) -> None:
        """Set a custom primary router (e.g., ML-based router)."""
        self._hybrid_router.set_primary_router(router)
    
    def set_confidence_threshold(self, threshold: float) -> None:
        """Set the confidence threshold for fallback decisions."""
        self._hybrid_router.set_confidence_threshold(threshold)
    
    def get_available_routes(self) -> List[str]:
        """Get all available routes."""
        return self._hybrid_router.get_available_routes()
    
    def get_router_info(self) -> dict:
        """Get router configuration information."""
        return self._hybrid_router.get_router_info()


# Convenience function for quick routing
def route_intent(user_input: str, **kwargs) -> RoutingResult:
    """
    Quick convenience function for intent routing.
    
    Creates a temporary AuroraRouter instance for one-off routing needs.
    For production use, create and reuse an AuroraRouter instance.
    """
    router = AuroraRouter()
    return router.route_intent(user_input, **kwargs)