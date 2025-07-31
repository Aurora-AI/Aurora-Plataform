# Aurora-Core Router Module
# 
# This module implements the HybridIntentRouter architecture
# with fallback mechanisms and modular routing strategies

from .hybrid_router import AuroraRouter, HybridIntentRouter, route_intent
from .interfaces import (
    BaseIntentRouter,
    IntentContext,
    IntentRouter,
    RouteConfidence,
    RoutingResult,
)
from .rule_based_router import RuleBasedRouter

__all__ = [
    # Main router classes
    "AuroraRouter",
    "HybridIntentRouter", 
    "RuleBasedRouter",
    
    # Interfaces and protocols
    "BaseIntentRouter",
    "IntentRouter",
    "IntentContext",
    "RoutingResult",
    "RouteConfidence",
    
    # Convenience functions
    "route_intent",
]