# Repository working rules

1. `docs/analyse.md` is the canonical record of permanent product decisions.
2. The core pipeline must remain usable without a GPU and without heavyweight AI dependencies.
3. Sport-specific behavior belongs under `src/vtaa/adapters/`; shared planning and rendering contracts must not contain football-only assumptions.
4. Integration with FootballAnalysisAI is file/JSON based. Do not copy its internal modules or create a runtime dependency on that repository.
5. Never commit source match footage, generated videos, model weights, credentials, or copyrighted character assets.
6. The target visual language is original clean 2D cel animation. Do not encode requests to reproduce protected characters, logos, or a named franchise exactly.
7. Every code change must include or update tests. Run `python -m unittest discover -s tests -v` before committing.
8. Keep Windows paths and the user's GTX 1050 environment in mind; optional acceleration must have a CPU-safe fallback.

