# CI/CD

The CI/CD workflow is defined in .github/workflows/cicd.yaml, it comprises:

- Python Code Quality checks
- Docker image build, as check, and upload to GHCR
- Helm quality checks
- **DISABLED** Helm upload to Helm repository