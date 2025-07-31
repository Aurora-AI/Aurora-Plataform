"""
Rule-based intent router implementation for Aurora-Core.

This router uses predefined rules and patterns to route intents,
serving as a reliable fallback mechanism for more complex routers.
"""

import re
from typing import Dict, List, Pattern

from .interfaces import BaseIntentRouter, IntentContext, RouteConfidence, RoutingResult


class RuleBasedRouter(BaseIntentRouter):
    """
    Rule-based intent router using pattern matching and keyword detection.
    
    This router serves as a fallback mechanism when more sophisticated
    ML-based routers fail or have low confidence.
    """
    
    def __init__(self, name: str = "rule_based_router"):
        super().__init__(name)
        self._rules: Dict[str, List[Pattern[str]]] = {}
        self._keyword_rules: Dict[str, List[str]] = {}
        self._setup_default_rules()
    
    def _setup_default_rules(self) -> None:
        """Setup default routing rules for common Aurora platform intents."""
        
        # Knowledge base queries
        self.add_pattern_rule(
            "knowledge_search",
            [
                r"\b(search|find|look for|query|what is|tell me about)\b",
                r"\b(documentation|docs|information|info)\b",
                r"\b(how to|tutorial|guide|help)\b"
            ]
        )
        
        # Authentication and user management
        self.add_pattern_rule(
            "auth",
            [
                r"\b(login|logout|sign in|sign out|authenticate)\b",
                r"\b(password|user|account|profile)\b",
                r"\b(register|signup|create account)\b"
            ]
        )
        
        # File and document operations
        self.add_pattern_rule(
            "document_processing",
            [
                r"\b(upload|download|file|document|pdf)\b",
                r"\b(extract|parse|analyze document)\b",
                r"\b(ingestion|ingest|add document)\b"
            ]
        )
        
        # ETP generation (specific to Aurora platform)
        self.add_pattern_rule(
            "etp_generation",
            [
                r"\b(etp|technical study|technical project)\b",
                r"\b(generate|create|build) (study|project|etp)\b",
                r"\b(technical specification|spec)\b"
            ]
        )
        
        # General conversation and assistance
        self.add_pattern_rule(
            "general_assistance",
            [
                r"\b(hello|hi|help|assist|support)\b",
                r"\b(thank you|thanks|bye|goodbye)\b",
                r"\b(what can you do|capabilities)\b"
            ]
        )
    
    def add_pattern_rule(self, route: str, patterns: List[str]) -> None:
        """Add pattern-based rules for a specific route."""
        if route not in self._rules:
            self._rules[route] = []
            if route not in self._routes:
                self._routes.append(route)
        
        compiled_patterns = [re.compile(pattern, re.IGNORECASE) for pattern in patterns]
        self._rules[route].extend(compiled_patterns)
    
    def add_keyword_rule(self, route: str, keywords: List[str]) -> None:
        """Add keyword-based rules for a specific route."""
        if route not in self._keyword_rules:
            self._keyword_rules[route] = []
            if route not in self._routes:
                self._routes.append(route)
        
        self._keyword_rules[route].extend([kw.lower() for kw in keywords])
    
    def route(self, context: IntentContext) -> RoutingResult:
        """Route intent using rule-based pattern matching."""
        user_input = context.user_input.lower()
        best_route = "general_assistance"  # Default fallback
        best_score = 0.0
        best_confidence = RouteConfidence.LOW
        reasoning_parts = []
        
        # Check pattern-based rules
        for route, patterns in self._rules.items():
            matches = 0
            total_patterns = len(patterns)
            
            for pattern in patterns:
                if pattern.search(user_input):
                    matches += 1
            
            if matches > 0:
                score = matches / total_patterns
                if score > best_score:
                    best_score = score
                    best_route = route
                    reasoning_parts.append(f"Pattern match for '{route}': {matches}/{total_patterns}")
        
        # Check keyword-based rules
        for route, keywords in self._keyword_rules.items():
            matches = 0
            for keyword in keywords:
                if keyword in user_input:
                    matches += 1
            
            if matches > 0:
                score = matches / len(keywords)
                if score > best_score:
                    best_score = score
                    best_route = route
                    reasoning_parts.append(f"Keyword match for '{route}': {matches}/{len(keywords)}")
        
        # Determine confidence level based on score
        if best_score >= 0.7:
            best_confidence = RouteConfidence.HIGH
        elif best_score >= 0.4:
            best_confidence = RouteConfidence.MEDIUM
        elif best_score > 0:
            best_confidence = RouteConfidence.LOW
        else:
            best_confidence = RouteConfidence.UNKNOWN
        
        reasoning = " | ".join(reasoning_parts) if reasoning_parts else "No specific patterns matched, using default route"
        
        return RoutingResult(
            route=best_route,
            confidence=best_confidence,
            score=best_score,
            metadata={
                "router_name": self.name,
                "rule_type": "pattern_and_keyword",
                "input_length": len(context.user_input)
            },
            reasoning=reasoning
        )
    
    def get_available_routes(self) -> List[str]:
        """Get all available routes this router can handle."""
        return self._routes.copy()
    
    def get_rules_summary(self) -> Dict[str, Dict[str, int]]:
        """Get a summary of configured rules for debugging."""
        return {
            "pattern_rules": {route: len(patterns) for route, patterns in self._rules.items()},
            "keyword_rules": {route: len(keywords) for route, keywords in self._keyword_rules.items()},
            "total_routes": len(self._routes)
        }