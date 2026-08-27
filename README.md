# OARepo Dashboard

Signed-in user's dashboard for [Invenio](https://inveniosoftware.org/) / InvenioRDM repositories built on the OARepo stack.

## Overview

This package provides the `/me` dashboard area where a user manages their own content. It is mainly a wrapper around the user dashboard shipped by [`invenio-app-rdm`](https://github.com/inveniosoftware/invenio-app-rdm), wiring its pages into an OARepo-based repository:

- Dashboard navigation (Uploads, Communities, Requests) registered into the app menus
- Customized dashboard header with avatar, user info, and context-aware actions
- Result-list rendering overrides for the user's uploads, driven by `oarepo-ui`
- A pluggable hook for registering per-schema result-item components
- React search components and dashboard styling shipped as a Webpack bundle
- Czech and English translations

The package registers itself with Invenio through entry points — no manual application wiring is required. The dashboard UI resource is served under the `/me` URL prefix.

## Installation

```bash
pip install oarepo-dashboard
```

### Requirements

- Python 3.14
- oarepo[rdm] 14.x
- oarepo-runtime >= 7.0.0
- oarepo-ui >= 13.0.0
- oarepo-rdm >= 8.0.0

## Key Features

### 1. Dashboard Menus

**Source:** [`oarepo_dashboard/ui/dashboard_components/__init__.py`](oarepo_dashboard/ui/dashboard_components/__init__.py)

On `finalize_app`, the package registers the dashboard navigation. A *My dashboard* entry is added to the main deposit menu (for authenticated users), and the dashboard submenu is built with three tabs pointing at the InvenioRDM user views:

- **Uploads** → `invenio_app_rdm_users.uploads`
- **Communities** → `invenio_app_rdm_users.communities`
- **Requests** → `invenio_app_rdm_users.requests`

The menu is configurable (see [Configuration](#configuration)) — you can suppress the main-menu entry and override individual submenu items.

### 2. Dashboard Header

**Source:** [`oarepo_dashboard/ui/dashboard_components/templates/oarepo/invenio_app_rdm/users/header.html`](oarepo_dashboard/ui/dashboard_components/templates/oarepo/invenio_app_rdm/users/header.html)

A template override for the user dashboard header. It renders the user's avatar, full name (falling back to username/email), and affiliations, the dashboard submenu tabs, and a context-aware primary action:

- *New upload* on the Uploads tab (links to `DASHBOARD_RECORD_CREATE_URL`)
- *New community* on the Communities tab

### 3. Result-List Overrides

**Source:** [`oarepo_dashboard/ui/dashboard_components/__init__.py`](oarepo_dashboard/ui/dashboard_components/__init__.py)

Using the `oarepo-ui` override system, the dashboard's *Uploads* results list is rendered with OARepo's `DynamicResultsListItem` component:

```python
from oarepo_ui.overrides import UIComponent, UIComponentOverride
from oarepo_ui.overrides.components import UIComponentImportMode

dynamic_result_list_item = UIComponent(
    "DynamicResultsListItem",
    "@js/oarepo_ui/search/DynamicResultsListItem",
    UIComponentImportMode.DEFAULT,
)
override = UIComponentOverride(
    "invenio_app_rdm_users.uploads",
    "InvenioAppRdm.DashboardUploads.ResultsList.item",
    dynamic_result_list_item,
)
```

The blueprint also appends a callback to `OAREPO_UI_RESULT_LIST_ITEM_REGISTRATION_CALLBACKS`, letting other libraries register per-schema result-item components for the dashboard uploads list.

### 4. React Search Components

**Source:** [`oarepo_dashboard/ui/dashboard_components/semantic-ui/js/dashboard_components/`](oarepo_dashboard/ui/dashboard_components/semantic-ui/js/dashboard_components/)

Front-end assets are shipped as a `WebpackThemeBundle`. Notably, `FacetsButtonGroupNameToggler` renders a Semantic UI button group for switching between mutually exclusive search facets (e.g. changing which facet a search is grouped by) while preserving the rest of the active query filters.

### 5. Translations

**Source:** [`oarepo_dashboard/i18n/`](oarepo_dashboard/i18n/)

Bundled Czech (`cs`) and English (`en`) message catalogs, registered through the `invenio_i18n.translations` entry point.

## Configuration

The following application config keys affect the dashboard:

| Key | Default | Description |
| --- | --- | --- |
| `REGISTER_DASHBOARD_IN_MAIN_MENU` | `True` | Whether to add the *My dashboard* entry to the main deposit menu. |
| `USER_DASHBOARD_MENU_OVERRIDES` | `{}` | Per-submenu overrides for the dashboard tabs. Keys must be one of `uploads`, `communities`, `requests`; values are merged into that submenu's registration kwargs (e.g. `text`, `order`, `endpoint`). Overriding an unknown submenu name raises `ValueError`. |
| `DASHBOARD_RECORD_CREATE_URL` | `""` | Target URL for the *New upload* button on the Uploads tab. |

## Development

```bash
git clone https://github.com/oarepo/oarepo-dashboard.git
cd oarepo-dashboard

./run.sh venv
./run.sh test
```

See [CONTRIBUTING.md](CONTRIBUTING.md) for the full contribution workflow.

## Entry Points

The package registers the following Invenio entry points:

```python
[project.entry-points."invenio_base.blueprints"]
oarepo_dashboard_components = "oarepo_dashboard.ui.dashboard_components:create_blueprint"

[project.entry-points."invenio_base.finalize_app"]
oarepo_dashboard_finalize_app = "oarepo_dashboard.ui.dashboard_components:finalize_app"

[project.entry-points."invenio_assets.webpack"]
oarepo_dashboard_i18n = "oarepo_dashboard.i18n.webpack:theme"
oarepo_dashboard_components_ui_theme = "oarepo_dashboard.ui.dashboard_components.webpack:theme"

[project.entry-points."invenio_i18n.translations"]
oarepo_dashboard_messages = "oarepo_dashboard"
```

## License

Copyright (c) 2025 CESNET z.s.p.o.

OARepo Dashboard is free software; you can redistribute it and/or modify it under the terms of the MIT License. See [LICENSE](LICENSE) file for more details.

## Links

- Repository: <https://github.com/oarepo/oarepo-dashboard>
- PyPI: <https://pypi.org/project/oarepo-dashboard/>
- Issues: <https://github.com/oarepo/oarepo-dashboard/issues>
- OARepo Project: <https://github.com/oarepo>

## Acknowledgments

This project builds upon [Invenio Framework](https://inveniosoftware.org/) and is developed as part of the OARepo ecosystem.
