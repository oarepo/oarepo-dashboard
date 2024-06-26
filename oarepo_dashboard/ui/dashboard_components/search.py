from oarepo_ui.resources.components import UIResourceComponent
from flask import current_app


class DashboardRecordsSearchComponent(UIResourceComponent):
    def before_ui_search(self, *, search_options, view_args, extra_context, **kwargs):
        search_options["overrides"]["dashboardRecordsCreateUrl"] = (
            current_app.config.get("DASHBOARD_RECORD_CREATE_URL", "")
        )


class DashboardRequestsSearchComponent(UIResourceComponent):
    def before_ui_search(self, *, search_options, view_args, **kwargs):
        search_options["initial_filters"] = [["is_open", "true"], ["mine", "true"]]
