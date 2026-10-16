# Harness entry points. CI runs exactly these targets — nothing else.
# The project's Python (.python-version) from .venv, never the system python3 (RULE-0010). uv makes it on first use.
PY := .venv/bin/python
GATE := harness/gates/harness_check.py

# The two apps, each its own git repository inside this workspace.
API := online-delivery-api
API_PROJ := OnlineDelivery.Api.csproj
APP := online-delivery-app

# Run a command inside an app, or skip it where that app is not checked out (the root repo's CI).
in = @if [ -d $(1) ]; then cd $(1) && $(2); else echo "skip: $(1) is not checked out"; fi

.PHONY: help install harness-check registry index id new fix linkfix hooks \
	fmt fmt-harness fmt-api fmt-app lint lint-harness lint-api lint-app \
	typecheck typecheck-api build build-api build-app test test-api test-app check \
	db-up db-down run-api run-app

help:
	@echo "make install         .venv, dotnet restore and npm ci"
	@echo "make harness-check   run every context gate"
	@echo "make registry        regenerate context/registry.yaml"
	@echo "make index           regenerate context/INDEX.md"
	@echo "make id TYPE=BPM     print the next free ID"
	@echo "make new TYPE=BPM TITLE=\"...\"  scaffold an artefact and log it"
	@echo "make fix             regenerate everything and link bare references"
	@echo "make linkfix         turn bare artefact references into links"
	@echo "make hooks           use harness/hooks in the root repo and both app repos"
	@echo "make fmt             format Python, C# and the React app"
	@echo "make lint            formatting and lint checks, every stack"
	@echo "make typecheck       compile the API with warnings as errors"
	@echo "make build           build the API and the React bundle"
	@echo "make test            every test suite. Run it after lint and typecheck (RULE-0019)"
	@echo "make check           lint, typecheck, build, then test"
	@echo "make db-up / db-down start or stop PostgreSQL in Docker (RULE-0010)"
	@echo "make run-api / run-app  start the API on :5154 or the app on :5173"

install: $(PY)
	$(call in,$(API),dotnet restore $(API_PROJ))
	$(call in,$(APP),npm ci)

harness-check: $(PY)
	@$(PY) $(GATE) check

registry: $(PY)
	@$(PY) $(GATE) registry

index: $(PY)
	@$(PY) $(GATE) index

id: $(PY)
	@$(PY) $(GATE) id $(TYPE)

new: $(PY)
	@$(PY) $(GATE) new $(TYPE) $(TITLE)

# The local loop. CI never runs this — it runs harness-check, which fails on stale output.
fix: registry index linkfix

linkfix: $(PY)
	@$(PY) $(GATE) linkfix

# Once per clone. Git does not carry hook settings, so each checkout opts in.
# A relative hooksPath resolves from each repository's top level.
hooks:
	@git config core.hooksPath harness/hooks && echo "hooks: root repo uses harness/hooks"
	$(call in,$(API),git config core.hooksPath ../harness/hooks && echo "hooks: $(API) uses ../harness/hooks")
	$(call in,$(APP),git config core.hooksPath ../harness/hooks && echo "hooks: $(APP) uses ../harness/hooks")

$(PY):
	@uv sync

# Format, lint and types, before the tests (RULE-0019).
fmt: fmt-harness fmt-api fmt-app

fmt-harness: $(PY)
	@uv run ruff check --fix --select I --quiet .
	@uv run ruff format --quiet .

fmt-api:
	$(call in,$(API),dotnet format $(API_PROJ))

fmt-app:
	$(call in,$(APP),npm run --silent format)

lint: lint-harness lint-api lint-app

lint-harness: $(PY)
	@uv run ruff check .
	@uv run ruff format --check .

lint-api:
	$(call in,$(API),dotnet format $(API_PROJ) --verify-no-changes)

lint-app:
	$(call in,$(APP),npm run --silent format:check && npm run --silent lint)

# The React app is JavaScript, so the API compile is the only type check.
typecheck: typecheck-api

typecheck-api:
	$(call in,$(API),dotnet build $(API_PROJ) -warnaserror --nologo -v q)

build: build-api build-app

build-api:
	$(call in,$(API),dotnet build $(API_PROJ) --nologo -v q)

build-app:
	$(call in,$(APP),npm run --silent build)

test: test-api test-app

# Test projects live under online-delivery-api/tests/ and are named *Tests.csproj.
test-api:
	$(call in,$(API),projs=$$(find tests -name '*Tests.csproj' 2>/dev/null); \
		if [ -n "$$projs" ]; then for p in $$projs; do dotnet test $$p --nologo -v q || exit 1; done; \
		else echo "test-api: no test project yet"; fi)

test-app:
	$(call in,$(APP),npm run --silent test --if-present -- --run)

check: lint typecheck build test

db-up:
	$(call in,$(API),docker compose up -d)

db-down:
	$(call in,$(API),docker compose down)

run-api:
	$(call in,$(API),dotnet run --project $(API_PROJ) --launch-profile http)

run-app:
	$(call in,$(APP),npm run dev)
