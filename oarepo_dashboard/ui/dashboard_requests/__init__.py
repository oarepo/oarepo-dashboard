from oarepo_ui.resources.config import (
    RecordsUIResourceConfig,
)
from oarepo_ui.resources.resource import RecordsUIResource
from flask_menu import current_menu
from oarepo_runtime.i18n import lazy_gettext as _
from oarepo_dashboard.ui.dashboard_components.search import (
    DashboardRequestsSearchComponent,
)
from flask import current_app
from flask_security import login_required


class DashboardRequestsUIResourceConfig(RecordsUIResourceConfig):
    url_prefix = "/me/requests/"
    blueprint_name = "requests_dashboard"
    template_folder = "templates"
    application_id = "requests_dashboard"
    templates = {
        "search": "DashboardRequestsPage",
    }

    routes = {
        "search": "/",
    }
    api_service = "requests"

    components = [DashboardRequestsSearchComponent]

    # object where we can store default result list items for various requests types
    default_results_list_items = {}

    def search_endpoint_url(self, identity, api_config, overrides={}, **kwargs):
        return "/api/user/requests"

    @property
    def default_components(self):
        requests_result_list_items = current_app.config.get(
            "REQUESTS_RESULT_LIST_ITEMS", {}
        )
        # make it possible to override these components from invenio.cfg
        return {**self.default_results_list_items, **requests_result_list_items}


class DashboardRequestsUIResource(RecordsUIResource):
    @login_required
    def search(self):
        return super().search()


def create_blueprint(app):
    """Register blueprint for this resource."""
    app_blueprint = DashboardRequestsUIResource(
        DashboardRequestsUIResourceConfig()
    ).as_blueprint()

    @app_blueprint.before_app_first_request
    def init_menu():
        user_dashboard = current_menu.submenu("user_dashboard")
        user_dashboard.submenu("requests").register(
            "requests_dashboard.search",
            text=_("Requests"),
            order=3,
        )

    return app_blueprint
