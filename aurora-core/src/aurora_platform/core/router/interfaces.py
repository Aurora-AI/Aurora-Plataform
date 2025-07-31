"""
Interface definitions for Aurora-Core routing system.

This module defines the base interfaces for intent routing, providing
a foundation for hybrid routing strategies and fallback mechanisms.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum
from typing import Any, Dict, List, Optional, Protocol


class RouteConfidence(Enum):
    """Enum representing confidence levels for routing decisions."""
    
    HIGH = "high"
    MEDIUM = "medium"  
    LOW = "low"
    UNKNOWN = "unknown"


@dataclass
class RoutingResult:
    """Result of a routing decision."""
    
    route: str
    confidence: RouteConfidence
    score: float
    metadata: Optional[Dict[str, Any]] = None
    reasoning: Optional[str] = None


@dataclass
class IntentContext:
    """Context information for intent routing."""
    
    user_input: str
    session_id: Optional[str] = None
    user_id: Optional[str] = None
    conversation_history: Optional[List[Dict[str, Any]]] = None
    additional_context: Optional[Dict[str, Any]] = None


class IntentRouter(Protocol):
    """Protocol for intent routing implementations."""
    
    def route(self, context: IntentContext) -> RoutingResult:
        """Route an intent based on context and return routing decision."""
        ...
    
    def get_available_routes(self) -> List[str]:
        """Get list of available routes this router can handle."""
        ...


class BaseIntentRouter(ABC):
    """Abstract base class for intent routers."""
    
    def __init__(self, name: str):
        self.name = name
        self._routes: List[str] = []
    
    @abstractmethod
    def route(self, context: IntentContext) -> RoutingResult:
        """Route an intent based on context."""
        pass
    
    @abstractmethod
    def get_available_routes(self) -> List[str]:
        """Get available routes."""
        pass
    
    def get_router_name(self) -> str:
        """Get the name of this router."""
        return self.name