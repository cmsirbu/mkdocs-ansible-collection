#!/usr/bin/env bash

set -o errexit
set -o pipefail

# -----------------------------------------------------------------------------
# Helper functions start with _ and aren't listed in this script's help menu.
# -----------------------------------------------------------------------------

function _uvr {
    uv run "$@"
}

# -----------------------------------------------------------------------------

function setup {
    echo "---------- Installing python environment via uv"
    _uvr uv sync
    echo "---------- Installing ansible collections from docs/requirements.yaml"
    _uvr uv run ansible-galaxy collection install -r docs/requirements.yaml
}

function lint {
    echo "---------- LINTING WITH RUFF"
    _uvr ruff check mkdocs_ansible_collection
    echo "---------- CHECKING FORMATTING WITH RUFF"
    _uvr ruff format --check --diff mkdocs_ansible_collection
    echo "---------- LINTING WITH YAMLLINT"
    _uvr yamllint .
}

function autofix {
    echo "---------- RUFF CHECK AUTOFIX"
    _uvr ruff check --fix mkdocs_ansible_collection
    echo "---------- FORMATTING WITH RUFF"
    _uvr ruff format mkdocs_ansible_collection
}

function serve {
    echo "---------- BUILDING AND SERVING DOCS"
    _uvr mkdocs serve "$@"
}

function test-build {
    echo "---------- BUILDING DOCS"
    _uvr mkdocs build --strict
}

# TODO: function test

# -----------------------------------------------------------------------------

function help {
  printf "%s <task> [args]\n\nTasks:\n" "${0}"

  compgen -A function | grep -v "^_" | cat -n

  printf "\nExtended help:\n  Each task has comments for general usage\n"
}

TIMEFORMAT=$'\nTask completed in %3lR'
time "${@:-help}"
