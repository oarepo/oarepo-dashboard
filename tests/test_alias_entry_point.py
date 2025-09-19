#
# Copyright (c) 2025 CESNET z.s.p.o.
#
# This file is a part of oarepo-dashboard (see https://github.com/oarepo/oarepo-dashboard).
#
# oarepo-dashboard is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#
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
