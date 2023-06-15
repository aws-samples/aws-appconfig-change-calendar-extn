.PHONY: linting

PY_FILES=app.py lambda/ cdk_appconfig_change_calendar_extn/

linting:
	ruff check $(PY_FILES)
	black --check $(PY_FILES)
	bandit -r $(PY_FILES)
