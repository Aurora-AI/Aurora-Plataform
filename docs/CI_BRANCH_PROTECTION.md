# Branch Protection Configuration - Aurora Platform

## Phase 2: Branch Protection Requirements

This document outlines the branch protection configuration requirements for the Aurora Platform repository as per technical plan AUR-PLATFORM-CI-002.

### Main Branch Protection Settings

The `main` branch should be configured with the following protection rules:

#### Required Status Checks
- **test-core**: Must pass before merge
- **test-crawler**: Must pass before merge

#### Configuration Steps
1. Navigate to the repository Settings → Branches
2. Add rule for `main` branch
3. Enable "Require status checks to pass before merging"
4. Add the following required checks:
   - `test-core`
   - `test-crawler`
5. Enable "Require branches to be up to date before merging"

#### Additional Recommended Settings
- Enable "Require pull request reviews before merging"
- Enable "Dismiss stale PR approvals when new commits are pushed"
- Enable "Restrict pushes that create files larger than 100 MB"

### Implementation Notes
- These settings must be configured through the GitHub web interface or API
- Status check names correspond to the job names in `.github/workflows/continuous_integration.yml`
- This ensures that both aurora-core and aurora-crawler tests must pass before any merge to main

### Related Documentation
- CI/CD Workflow: `.github/workflows/continuous_integration.yml`
- Technical Plan: AUR-PLATFORM-CI-002
- Resilience Plan: CI_Resilience_Plan