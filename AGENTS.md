# Repository working rules

1. Before changing code, read `docs/analyse.md`, `docs/architecture.md`, `docs/integration-contract.md`, `README.md`, and `isAkis.md`.
2. `docs/analyse.md` is the canonical record of permanent product decisions.
3. `isAkis.md` is the canonical Codex/GitHub setup and operational workflow.
4. The core pipeline must remain usable without a GPU and without heavyweight AI dependencies.
5. Sport-specific behavior belongs under `src/vtaa/adapters/`; shared planning and rendering contracts must not contain football-only assumptions.
6. Integration with FootballAnalysisAI is file/JSON based. Do not copy its internal modules or create a runtime dependency on that repository.
7. Never commit source match footage, generated videos, model weights, credentials, or copyrighted character assets.
8. The target visual language is original clean 2D cel animation. Do not encode requests to reproduce protected characters, logos, or a named franchise exactly.
9. Every code change must include or update tests. Run `python -m unittest discover -s tests -v` before committing.
10. Keep Windows paths and the user's GTX 1050 environment in mind; optional acceleration must have a CPU-safe fallback.
