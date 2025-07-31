# Legacy Configuration Files

This directory contains backup copies of configuration files that were consolidated during the monorepo unification process.

## Files Preserved:

### Docker Compose Configurations
- `aurora-core-docker-compose.yml.backup` - Original Aurora-Core docker-compose.yml
- `aurora-core-docker-compose.override.yml.backup` - Original Aurora-Core development override
- `aurora-crawler-docker-compose.yml.backup` - Original Aurora-Crawler docker-compose.yml

### CI/CD Configurations
- `aurora-core-ci.yml.backup` - Original Aurora-Core GitHub Actions workflow

## Why These Files Were Removed

These files were consolidated into unified configurations at the monorepo root:

1. **Docker Compose**: Individual service configurations were merged into a single `docker-compose.yaml` at the root, with a `docker-compose.override.yml` for development.

2. **CI/CD**: Individual workflows were combined into a comprehensive monorepo CI/CD pipeline in `.github/workflows/ci.yml`.

## Recovery Instructions

If you need to reference the original configurations:

1. **Individual Service Development**: The unified docker-compose configuration supports running individual services
2. **Legacy Configuration**: These backup files can be used as reference for any missing configurations
3. **Service-Specific Needs**: If a service needs its own docker-compose for some reason, these files can be restored

## Migration Notes

The unified configurations provide:
- Shared infrastructure (ChromaDB, Redis) to eliminate duplication
- Consistent development experience across services  
- Centralized CI/CD with proper service isolation
- Easier deployment and orchestration

All functionality from the original configurations has been preserved in the unified setup.