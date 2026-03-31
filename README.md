Creating a coding interview prep platform that simulates the technical rounds of an interview process as closely as possible.

Commands:

- `uvicorn app.manin:app --reload`to view endpoints _MUST be in /backend_
  - /docs: FastAPI APIs
- `.venv/bin/python -m pip install <package>`to download any packages
- `docker exec -it ai_interviewer_db psql -U postgres -d ai_interviewer` To view db via command line

TODOS:

- ProblemPageEditor/ProblemPageTerminal can be shorter. Move functions to utils
- Pre-baked hints: store structured nudges keyed by stage + detected issue (“still no edge cases after 3 turns”) so the first n nudges are deterministic. Save the AI for novel coaching moments.
- Cache static context: embed things like the full problem statement, constraints, and pseudocode once (maybe as a hashed key in Redis) so each stage call just references an ID. You can even use Gemini’s “system instruction cache” feature if/when it arrives.
- Stage-aware summarization: before each AI call, pre-summarize the relevant chat slice on the server (e.g., “Clarification highlights: …”). Send that digest plus the reference snippet instead of the entire transcript; you reduce tokens while giving the model a distilled view aligned with your rubric.
- Feature flags (particularly for voiceover functionality once it's time)
- Add more problems to Blind 75 list.
- If problems have 'Followups', include that as a field in the problem schema.

For distant future:

- Create algorithm/SD courses for new engineers
- Create system design interview capability
