# Sandbox Container Isolation & Fallback Policy

## Isolation Boundaries

- **Docker Sandbox**: Container memory limit `512MB`, non-root execution (`UID 1000`), disabled network stack (`network_mode="none"`).
- **Synthetic Sandbox**: Fallback in-memory guard intercepting path traversal, SQL injections, and network calls deterministically.
