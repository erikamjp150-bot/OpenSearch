# Contributing to OpenSearch

Thanks for your interest in contributing to OpenSearch.

## Development workflow

1. Fork the repository and create a branch for your change.
2. Make your changes and keep them focused.
3. Run the relevant tests before opening a pull request.
4. Submit a pull request with a clear title and summary.

## Local setup

- Backend dependencies: install from [backend/requirements.txt](backend/requirements.txt)
- Frontend dependencies: install from [frontend/package.json](frontend/package.json)
- Docker-based setup: use [docker-compose.yml](docker-compose.yml)

## Testing

```bash
cd backend
PYTHONPATH=. pytest tests -q
```

## Code style

- Prefer clear, descriptive names.
- Keep changes small and easy to review.
- Avoid introducing unnecessary dependencies.

## Reporting issues

Please open an issue with as much detail as possible, including steps to reproduce and expected behavior.
