# CI/CD Caching and Branch Protection Documentation

## Cache Implementation in platform_ci.yml

This document describes the caching optimizations implemented in the Platform CI/CD pipeline to improve build performance and reliability.

### Poetry Dependencies Cache

**Purpose**: Reduces dependency installation time by caching Poetry and pip downloads.

**Cached Directories**:
- `~/.cache/pypoetry` - Poetry's package cache
- `~/.cache/pip` - Pip's package cache

**Cache Key Strategy**:
- Primary key: `${{ runner.os }}-poetry-${{ hashFiles('module/poetry.lock') }}`
- Fallback key: `${{ runner.os }}-poetry-`

**Benefits**:
- Faster dependency installation on subsequent builds
- Resilience against temporary package registry issues
- Reduced network bandwidth usage

### Hugging Face Models Cache

**Purpose**: Prevents repeated downloads of large ML models from Hugging Face Hub.

**Cached Directory**:
- `~/.cache/huggingface/hub` - Hugging Face model cache

**Cache Key Strategy**:
- Primary key: `${{ runner.os }}-huggingface-${{ hashFiles('module/poetry.lock') }}`
- Fallback key: `${{ runner.os }}-huggingface-`

**Benefits**:
- Significantly faster builds when using pre-trained models
- Reduced dependency on external model repositories
- Lower risk of build failures due to download timeouts

### Cache Invalidation

Caches are automatically invalidated when:
- The `poetry.lock` file changes (indicating dependency updates)
- The operating system changes (different runner environment)

### Implementation Details

1. **Cache Placement**: Cache steps are positioned after Python setup but before dependency installation
2. **Job Isolation**: Each job (test-core, test-crawler) maintains separate caches based on their respective poetry.lock files
3. **Restore Keys**: Fallback keys allow partial cache hits when exact matches aren't available

## Branch Protection Configuration

### Required Manual Configuration

The following branch protection rules must be configured manually in the GitHub repository settings:

**Branch**: `main`

**Required Status Checks**:
- `test-core` (from platform_ci.yml)
- `test-crawler` (from platform_ci.yml)

**Settings to Enable**:
- [x] Require status checks to pass before merging
- [x] Require branches to be up to date before merging
- [x] Require status checks: `test-core`, `test-crawler`

**Configuration Steps**:
1. Go to Repository Settings → Branches
2. Add branch protection rule for `main`
3. Enable "Require status checks to pass before merging"
4. Enable "Require branches to be up to date before merging"
5. Search for and select the required status checks: `test-core` and `test-crawler`
6. Save the protection rule

**Alternative Configuration via GitHub CLI** (if available):
```bash
# Enable branch protection with required status checks
gh api repos/:owner/:repo/branches/main/protection \
  --method PUT \
  --field required_status_checks='{"strict":true,"contexts":["test-core","test-crawler"]}' \
  --field enforce_admins=true \
  --field required_pull_request_reviews='{"required_approving_review_count":1}' \
  --field restrictions=null
```

### Impact

With these protections in place:
- Pull requests cannot be merged unless both test jobs pass
- This ensures code quality and prevents broken code from entering the main branch
- Developers must resolve any test failures before merging
- The pipeline will be more resilient due to caching, reducing failures from network issues

## Migration from continuous_integration.yml

This `platform_ci.yml` replaces the functionality of `continuous_integration.yml` with the following enhancements:
- Added Poetry dependency caching
- Added Hugging Face model caching  
- Maintained all existing test, lint, and formatting checks
- Preserved the same job names (`test-core`, `test-crawler`) for branch protection compatibility

The old `continuous_integration.yml` can be safely removed once this workflow is verified to work correctly.