import os
import logging

import sentry_sdk
from sentry_sdk.integrations.fastapi import FastApiIntegration
from sentry_sdk.integrations.logging import LoggingIntegration

logger = logging.getLogger(__name__)


def init_error_tracking():
    """
    Initialize Sentry for error tracking and performance monitoring.
    """
    sentry_dsn = os.getenv("SENTRY_DSN")
    environment = os.getenv("ENVIRONMENT", "development")
    
    if not sentry_dsn:
        logger.warning("SENTRY_DSN not configured - error tracking disabled")
        return
    
    # Configure logging integration
    logging_integration = LoggingIntegration(
        level=logging.INFO,        # Capture info and above as breadcrumbs
        event_level=logging.ERROR  # Send errors as events
    )
    
    try:
        sentry_sdk.init(
            dsn=sentry_dsn,
            integrations=[
                FastApiIntegration(auto_enabling_integrations=False),
                logging_integration,
            ],
            traces_sample_rate=0.1 if environment == "production" else 1.0,
            environment=environment,
            release=os.getenv("PROJECT_VERSION", "1.0.0"),
            # Performance monitoring
            profiles_sample_rate=0.1 if environment == "production" else 1.0,
            # Filter out health check noise
            before_send=_before_send_filter,
        )
        logger.info(f"Sentry initialized for environment: {environment}")
    except Exception as e:
        logger.error(f"Failed to initialize Sentry: {e}")


def _before_send_filter(event, hint):
    """
    Filter out noise from Sentry events.
    """
    # Skip health check requests
    if event.get("request", {}).get("url", "").endswith("/health"):
        return None
    
    # Skip certain error types in development
    if os.getenv("ENVIRONMENT") == "development":
        if event.get("exception", {}).get("values", [{}])[0].get("type") == "KeyboardInterrupt":
            return None
    
    return event
