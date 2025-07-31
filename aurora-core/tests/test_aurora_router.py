"""
Test suite for Aurora-Core router implementation.
"""

import pytest

from src.aurora_platform.core.router import (
    AuroraRouter,
    HybridIntentRouter,
    IntentContext,
    RouteConfidence,
    RuleBasedRouter,
    route_intent,
)


class TestRuleBasedRouter:
    """Test cases for RuleBasedRouter."""
    
    def test_initialization(self):
        """Test router initialization."""
        router = RuleBasedRouter()
        assert router.get_router_name() == "rule_based_router"
        assert len(router.get_available_routes()) > 0
    
    def test_knowledge_search_routing(self):
        """Test routing for knowledge search queries."""
        router = RuleBasedRouter()
        context = IntentContext(user_input="search for documentation about API")
        
        result = router.route(context)
        
        assert result.route == "knowledge_search"
        assert result.confidence in [RouteConfidence.MEDIUM, RouteConfidence.HIGH]
        assert result.score > 0
    
    def test_auth_routing(self):
        """Test routing for authentication queries."""
        router = RuleBasedRouter()
        context = IntentContext(user_input="I need to login to my account")
        
        result = router.route(context)
        
        assert result.route == "auth"
        assert result.confidence in [RouteConfidence.MEDIUM, RouteConfidence.HIGH]
    
    def test_etp_generation_routing(self):
        """Test routing for ETP generation queries."""
        router = RuleBasedRouter()
        context = IntentContext(user_input="generate a technical study ETP")
        
        result = router.route(context)
        
        assert result.route == "etp_generation"
        assert result.confidence in [RouteConfidence.MEDIUM, RouteConfidence.HIGH]
    
    def test_fallback_routing(self):
        """Test fallback for unrecognized inputs."""
        router = RuleBasedRouter()
        context = IntentContext(user_input="xyz random unknown input 123")
        
        result = router.route(context)
        
        assert result.route == "general_assistance"
        assert result.confidence == RouteConfidence.UNKNOWN
        assert result.score == 0.0
    
    def test_custom_rules(self):
        """Test adding custom rules."""
        router = RuleBasedRouter()
        router.add_pattern_rule("custom_route", [r"\bcustom\b"])
        
        context = IntentContext(user_input="this is a custom request")
        result = router.route(context)
        
        assert result.route == "custom_route"
        assert "custom_route" in router.get_available_routes()


class TestHybridIntentRouter:
    """Test cases for HybridIntentRouter."""
    
    def test_initialization(self):
        """Test hybrid router initialization."""
        router = HybridIntentRouter()
        assert router.get_router_name() == "hybrid_intent_router"
        assert len(router.get_available_routes()) > 0
    
    def test_fallback_only_routing(self):
        """Test routing with only fallback router."""
        router = HybridIntentRouter()
        context = IntentContext(user_input="search for help documentation")
        
        result = router.route(context)
        
        assert result.route == "knowledge_search"
        assert result.metadata["hybrid_router_decision"] == "fallback"
        assert result.metadata["fallback_router"] == "fallback_rule_router"
    
    def test_confidence_threshold(self):
        """Test confidence threshold setting."""
        router = HybridIntentRouter()
        
        # Test valid threshold
        router.set_confidence_threshold(0.8)
        assert router._confidence_threshold == 0.8
        
        # Test invalid threshold
        with pytest.raises(ValueError):
            router.set_confidence_threshold(1.5)
    
    def test_router_info(self):
        """Test router information retrieval."""
        router = HybridIntentRouter()
        info = router.get_router_info()
        
        assert info["name"] == "hybrid_intent_router"
        assert info["primary_router"] is None
        assert info["fallback_router"] == "fallback_rule_router"
        assert "available_routes" in info
        assert "routes" in info


class TestAuroraRouter:
    """Test cases for AuroraRouter facade."""
    
    def test_initialization(self):
        """Test Aurora router initialization."""
        router = AuroraRouter()
        assert len(router.get_available_routes()) > 0
    
    def test_simple_routing(self):
        """Test simple intent routing."""
        router = AuroraRouter()
        
        result = router.route_intent("search for API documentation")
        
        assert result.route == "knowledge_search"
        assert isinstance(result.score, float)
        assert result.metadata is not None
    
    def test_routing_with_context(self):
        """Test routing with additional context."""
        router = AuroraRouter()
        
        result = router.route_intent(
            "help me login",
            session_id="test_session",
            user_id="test_user"
        )
        
        assert result.route == "auth"
        assert result.metadata is not None
    
    def test_convenience_function(self):
        """Test convenience routing function."""
        result = route_intent("generate ETP for construction project")
        
        assert result.route == "etp_generation"
        assert isinstance(result, type(route_intent("test")))


class TestIntegration:
    """Integration tests for the router system."""
    
    def test_multiple_queries(self):
        """Test routing multiple different queries."""
        router = AuroraRouter()
        
        test_cases = [
            ("search documentation", "knowledge_search"),
            ("login please", "auth"),
            ("upload a PDF file", "document_processing"),
            ("create technical study", "etp_generation"),
            ("hello", "general_assistance"),
        ]
        
        for query, expected_route in test_cases:
            result = router.route_intent(query)
            assert result.route == expected_route, f"Failed for query: {query}"
    
    def test_router_consistency(self):
        """Test that multiple calls with same input return consistent results."""
        router = AuroraRouter()
        query = "search for technical documentation"
        
        results = [router.route_intent(query) for _ in range(3)]
        
        # All results should have the same route
        routes = [r.route for r in results]
        assert len(set(routes)) == 1, "Inconsistent routing results"