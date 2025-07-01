---
hide:
  - navigation
---

# Release Notes

This document describes all new features and changes in this project's releases. The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/) and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [v1.1.0 (2025-07-01)](https://github.com/cmsirbu/mkdocs-ansible-collection/releases/tag/v1.1.0)

### Changed

- [#27](https://github.com/cmsirbu/mkdocs-ansible-collection/pull/27) Improved the template that renders the parameters table for plugins:
    - Added data type to the parameter column.
    - Moved env vars to the comments column.
    - Added defaults and choices column to the parameters table.
    - Added suboptions when a parameter has dictionary sub-values.
    - Changed parameters table to inline HTML since Markdown tables break with any errant newlines.

### Documentation

- [#27](https://github.com/cmsirbu/mkdocs-ansible-collection/pull/27) Added `opsmill.infrahub` and `nokia.srlinux` collections to showcase.
- [#27](https://github.com/cmsirbu/mkdocs-ansible-collection/pull/27) Fixed page view/edit github links.
- Added Release Notes and Release Checklist to documentation.

### Fixed

- [#23](https://github.com/cmsirbu/mkdocs-ansible-collection/pull/23) Fixed template to account for the plugin description not always being a list.

### Housekeeping

- [#30](https://github.com/cmsirbu/mkdocs-ansible-collection/pull/30) Updated `uv` to `0.7.17`.

## [v1.0.0 (2025-05-10)](https://github.com/cmsirbu/mkdocs-ansible-collection/releases/tag/v1.0.0)

All Ansible plugin types have been enabled and are now rendered with the generic template. While certain plugins would benefit from having dedicated templates, this is now good enough to bump to version `1.0.0`!

The project has also moved to `uv` and now has user and developer documentation.

### Added

- [#19](https://github.com/cmsirbu/mkdocs-ansible-collection/pull/19) Enabled remaining Ansible plugin types.

### Documentation

- [#21](https://github.com/cmsirbu/mkdocs-ansible-collection/pull/21) Added User and Developer Guides to project docs and simplified README.

### Housekeeping

- [#11](https://github.com/cmsirbu/mkdocs-ansible-collection/pull/11) Updated project metadata to allow uv to run alongside poetry 2.0.
- [#13](https://github.com/cmsirbu/mkdocs-ansible-collection/pull/13) Removed poetry as front-end tool.
- [#14](https://github.com/cmsirbu/mkdocs-ansible-collection/pull/14) Changed to `uv` in RTD builds.
- [#15](https://github.com/cmsirbu/mkdocs-ansible-collection/pull/15) Added CI workflow and run.sh tasks file.
- [#21](https://github.com/cmsirbu/mkdocs-ansible-collection/pull/21) Enabled CI testing the mkdocs build on all supported Python versions.
- [#21](https://github.com/cmsirbu/mkdocs-ansible-collection/pull/21) Enabled strict mode in RTD builds.

## [v0.2.1 (2024-11-16)](https://github.com/cmsirbu/mkdocs-ansible-collection/releases/tag/v0.2.1)

### Fixed

- Fixed issues with HTML escaped YAML in code blocks which broke plugin examples.
- [#9](https://github.com/cmsirbu/mkdocs-ansible-collection/pull/9) Enabled auto-escaping only for html and xml templates.

## [v0.2.0 (2024-11-01)](https://github.com/cmsirbu/mkdocs-ansible-collection/releases/tag/v0.2.0)

### Added

- [#6](https://github.com/cmsirbu/mkdocs-ansible-collection/pull/6) Added ability to specify collection tree placement in the nav.
- [#8](https://github.com/cmsirbu/mkdocs-ansible-collection/pull/8) Added quick start steps to README and other instructions.

### Changed

- [#7](https://github.com/cmsirbu/mkdocs-ansible-collection/pull/7) Skip disabled plugin types in index pages.

## [v0.1.4 (2024-10-17)](https://github.com/cmsirbu/mkdocs-ansible-collection/releases/tag/v0.1.4)

### Changed

- Tweaked and used generic plugin template for: filter, lookup, inventory, and module plugins.

## [v0.1.3 (2024-09-24)](https://github.com/cmsirbu/mkdocs-ansible-collection/releases/tag/v0.1.3)

### Added

- [#5](https://github.com/cmsirbu/mkdocs-ansible-collection/pull/5) - Adds templates.
- Integrated `inventory` plugin template.
- Added `networktocode.nautobot` collection to project docs example build.

### Changed

- Tweaked theme width to allow for wider tables on project docs.

## [v0.1.2 (2024-08-16)](https://github.com/cmsirbu/mkdocs-ansible-collection/releases/tag/v0.1.2)

Initial release testing to PyPI.
