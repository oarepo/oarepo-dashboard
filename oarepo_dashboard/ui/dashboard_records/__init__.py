from oarepo_ui.resources.resource import RecordsUIResource
from flask_menu import current_menu
from flask_login import current_user
from oarepo_runtime.i18n import lazy_gettext as _
from oarepo_global_search.ui.config import GlobalSearchUIResourceConfig


class DashboardRecordsUIResourceConfig(GlobalSearchUIResourceConfig):
    url_prefix = "/me/records/"
    blueprint_name = "records_dashboard"
    template_folder = "templates"
    application_id = "records_dashboard"
    templates = {
        "search": "DashboardRecordsPage",
    }

    routes = {
        "search": "/",
    }
    api_service = "records"

    def search_endpoint_url(self, identity, api_config, overrides={}, **kwargs):
        return f"/api/user/search"


class DashboardRecordsUIResource(RecordsUIResource):
    pass


def create_blueprint(app):
    """Register blueprint for this resource."""
    app_blueprint = DashboardRecordsUIResource(
        DashboardRecordsUIResourceConfig()
    ).as_blueprint()

    @app_blueprint.before_app_first_request
    def init_menu():
        user_dashboard = current_menu.submenu("user_dashboard")
        user_dashboard.submenu("records").register(
            "records_dashboard.search",
            text=_("Records"),
            order=1,
            visible_when=lambda: current_user and current_user.is_authenticated,
        )

        # if you add dashboard to your project, the library adds itself to the main menu
        main_menu_dashboard = current_menu.submenu("main.dashboard")
        main_menu_dashboard.register(
            "records_dashboard.search",
            _("Dashboard"),
            order=1,
            visible_when=lambda: current_user and current_user.is_authenticated,
        )

    return app_blueprint
