# Agent Directives & Project Rules

## Monorepo Navigation

- **Frontend Code:** Located in './frontend'
- **Backend Code:** Located in './backend'

## Frontend Rules (`./frontend`)

- **Stack:** React with TypeScript, Vite, React Router, and TanStack Query.
- **TypeScript:** Keep strict mode enabled. Do not use `any` unless there is no practical typed alternative. Use `import type` for type-only imports and keep unused locals and parameters out of the codebase.
- **Imports:** Prefer the `@/*` alias for imports from `src` instead of long relative paths.

### Frontend Structure

- `src/pages`: Route-level composition. Pages should coordinate feature components and page state, not contain reusable domain logic.
- `src/features/<domain>`: Domain-specific components, hooks, adapters, and utilities. Keep problem-solving and interview behavior here rather than in shared components.
- `src/components`: Reusable, domain-neutral UI components such as layout, navigation, cards, modals, and loading indicators.
- `src/routes/AppRouter.tsx`: Keep route definitions and the shared layout boundary here. Use React Router navigation and links instead of manually changing `window.location`.
- `src/services/api`: The only place that should make backend requests. Reuse `requestJson`, `parseJson`, `buildAuthHeaders`, and the existing API modules instead of duplicating fetch and authentication logic.
- `src/services/auth.ts`: Keep token persistence and authentication-token helpers centralized here. Do not read or write auth tokens directly from components.
- `src/types`: Define shared frontend domain and API types. Keep API response shapes aligned with backend schemas.

### React and State

- Keep state immutable. Use functional state updates (`setState(prev => ...)`) whenever the next value depends on the previous value.
- Keep transient UI state local to the smallest component or feature that owns it. Lift state only when multiple consumers genuinely need it.
- Use TanStack Query for server state, caching, loading, and request errors. Do not duplicate the same server data in unrelated local state without a clear reason.
- Use `useMemo` and `useCallback` only when they preserve stable dependencies or prevent meaningful work; do not add them automatically.
- Keep effects focused on synchronization with an external system. Do not use `useEffect` for values that can be derived during render.
- Cancel or ignore stale asynchronous results when a component unmounts or its request context changes.
- Keep components focused and composable. Move reusable behavior into a hook or utility rather than creating large page components.
- Preserve controlled input behavior for editors, forms, filters, and tabs. Trim and validate user input at the interaction boundary.
- ALWAYS use direct value initialization for state via `useState` unless computing heavy operations. Examples:
  - PREFER: `const [code, setCode] = useState<string>(starterCode[selectedLanguage] ?? '');`
  - AVOID: `const [code, setCode] = useState<string>(() => ...);` (No lazy arrow callbacks for simple assignments).
- Ensure no duplicate variable declarations or dangling code fragments exist in custom hooks.

### API and Error Handling

- Type API request and response payloads. Do not silently cast unknown response data to a domain type without validating or normalizing it.
- Handle loading, error, empty, and success states for every asynchronous view.
- Show user-safe error messages in the UI and log only appropriate diagnostic information. Never expose tokens, passwords, or raw sensitive server responses.
- Use the existing backend routes and response contracts. Update the relevant API module and frontend type together when a contract changes.
- Keep optimistic updates reversible and remove or reconcile optimistic records when a request fails.

### UI, Accessibility, and Styling

- Use semantic HTML and accessible labels, names, focus states, keyboard interaction, and ARIA attributes where native HTML is insufficient.
- Buttons should be actual `button` elements and navigation should use `Link` or `NavLink`; do not use clickable `div` elements.
- Provide visible feedback for loading, submission progress, disabled actions, validation errors, and empty data.
- Keep styling consistent with the existing CSS and CSS-module conventions. Co-locate component styles where practical and avoid one-off inline styles except for genuinely dynamic values.
- Preserve responsive behavior across narrow and wide viewports. Do not introduce fixed dimensions that cause content, controls, or editor panels to overflow.

### Frontend Verification

- Run commands from `./frontend`.
- Before completing frontend work, run `npm run lint` and `npm run build`.
- The project does not currently define an `npm test` script or a frontend test runner. Do not claim frontend tests pass until a test runner is added.
- When tests are introduced, add them near the relevant feature or under `src/__tests__`, cover user-visible behavior and important hook/API states, mock network requests, and avoid relying on real backend data or external services.

## Backend Rules (`./backend`)

- Run backend commands from the `./backend` directory.
- Use the existing Python virtual environment when available:
  `source .venv/bin/activate`
- Start the API with:
  `uvicorn app.main:app --reload`
- Keep secrets and environment-specific configuration in `.env`; update `.env.example` when adding new variables.

### Architecture

- `app/api/routers`: Define HTTP routes, dependencies, authentication, request parsing, response models, and HTTP status errors.
- Keep router functions thin. Business logic and multi-step workflows belong in `app/services`.
- `app/services`: Implement business rules and coordinate CRUD operations, external APIs, AI services, and transactions.
- `app/crud`: Contain database queries and persistence operations only. Do not put HTTP logic or AI calls here.
- `app/schemas`: Define Pydantic request and response contracts. Do not expose SQLAlchemy models directly from API endpoints.
- `app/db/models`: Define SQLAlchemy tables, relationships, constraints, and database-level defaults.
- `app/core`: Contain shared configuration, authentication, security helpers, constants, and cross-cutting utilities.
- Do not duplicate business logic between routers, services, and CRUD modules.
- Prefer domain/service exceptions in service code and translate them into `HTTPException` responses at the API boundary.
- Use FastAPI dependency injection for database sessions and authenticated users.
- Never trust a user ID supplied by the client when an authenticated user ID is available.
- User-owned resources must verify ownership before returning or modifying data.
- Never return passwords, password hashes, access tokens, private test cases, or other sensitive fields in API responses.
- Keep AI and external-service calls isolated behind services so they can be mocked in tests.
- Use Alembic for all database schema changes. Do not rely on `Base.metadata.create_all()` to update an existing database or add ad-hoc SQL migrations.
- New migrations should be reversible where practical and must be tested with `alembic upgrade head`.

### Backend Testing

- Store backend tests under `backend/tests/`.
- Name test files `test_*.py` and use shared fixtures from `backend/tests/conftest.py`.
- Every new endpoint should test:
  - the successful response
  - invalid input and validation errors
  - unauthenticated access where relevant
  - forbidden access or ownership failures
  - missing resources
  - important persistence side effects
- Test services and pure business logic independently from HTTP.
- Test routers with FastAPI's test client and override database/auth dependencies.
- Use an isolated test database. Tests must not modify development or production data.
- Mock Gemini, code evaluation, and other external services. Tests must not require real API keys or network access.
- Add regression tests for bug fixes.
- Test edge cases in authentication, pagination, transactions, empty results, duplicate records, and failed external-service calls.
- Run backend tests from `./backend` with:
  `python -m pytest -q`
- Run migrations separately with:
  `alembic upgrade head`

## Execution Workflow

1. **Plan First:** Before editing, outline the proposed file changes in 3 concise bullet points. If the user has already provided or approved a plan, use that plan without repeating it.
2. **Directory Isolation:** Do not modify backend files during frontend work unless explicitly instructed or a shared API contract requires it. Call out any cross-boundary changes before making them.
3. **Verification:** After making changes, run the strongest relevant checks available in the affected directory, such as unit tests, integration tests, linting, type-checking, or a production build. Report unavailable test commands rather than pretending they passed.
