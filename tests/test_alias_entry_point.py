# SPDX-FileCopyrightText: 2025 CESNET z.s.p.o
# SPDX-License-Identifier: MIT

from __future__ import annotations

import json
from pathlib import Path

from oarepo_ui.webpack import project


def test_overridable_bundle_project_init(app):
    project.clean()
    project.create()
    with app.app_context():
        assert project.config_path.endswith("build/config.json")
        with Path.open(project.config_path) as f:
            config_data = json.load(f)
            assert "@js/dashboard_components" in config_data["aliases"]
            assert "invenio-app-rdm-user-communities" in config_data["entry"]
            assert "invenio-app-rdm-user-requests" in config_data["entry"]
            assert "invenio-app-rdm-user-uploads" in config_data["entry"]
