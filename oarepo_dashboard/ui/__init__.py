from oarepo_ui.resources.config import TemplatePageUIResourceConfig
from oarepo_ui.resources.resource import TemplatePageUIResource
from invenio_search_ui.searchconfig import FacetsConfig, SearchAppConfig, SortConfig
from invenio_records_resources.proxies import current_service_registry
from flask_menu import current_menu
from oarepo_runtime.i18n import lazy_gettext as _
from flask_security import login_required


sort_options = {
    "title": dict(
        title=_("By Title"),
        fields=["metadata.title"],  # ES defaults to desc on `_score` field
    ),
    "bestmatch": dict(
        title=_("Best match"),
        fields=["_score"],  # ES defaults to desc on `_score` field
    ),
    "newest": dict(
        title=_("Newest"),
        fields=["-created"],
    ),
    "oldest": dict(
        title=_("Oldest"),
        fields=["created"],
    ),
}


class DashboardPageResourceConfig(TemplatePageUIResourceConfig):
    url_prefix = "/me/"
    blueprint_name = "dashboard"
    template_folder = "templates"
    pages = {
        "records": "DashboardRecordsPage",
        "communities": "DashboardCommunitiesPage",
        "requests": "DashboardRequestsPage",
    }
    records_app_id = "records_dashboard".capitalize()
    requests_app_id = "requests_dashboard".capitalize()
    communities_app_id = "communities_dashboard".capitalize()

    def records_search_app_config(self, overrides={}, **kwargs):
        documents_service = current_service_registry.get("documents")
        documents_config = documents_service.config
        search_facets = documents_config.search.facets
        facets = self.search_facets_config(search_facets, search_facets.keys())

        opts = dict(
            app_id=self.records_app_id,
            endpoint="/api/docs",
            headers={"Accept": "application/vnd.inveniordm.v1+json"},
            grid_view=False,
            sort=SortConfig(
                sort_options,
                sort_options,
                "newest",
                "newest",
            ),
            facets=facets,
        )
        opts.update(kwargs)
        return SearchAppConfig.generate(opts, **overrides)

    def requests_search_app_config(self, overrides={}, **kwargs):
        requests_service = current_service_registry.get("requests")
        requests_config = requests_service.config
        search_facets = requests_config.search.facets
        facets = self.search_facets_config(search_facets, search_facets.keys())
        opts = dict(
            app_id=self.requests_app_id,
            endpoint="/api/requests",
            headers={"Accept": "application/json"},
            # TODO: just for testing of button group in requests search app
            # initial_filters=[["is_open", "true"], ["is_mine", "true"]],
            initial_filters=[["is_open", "true"]],
            sort=SortConfig(
                sort_options,
                sort_options,
                "newest",
                "newest",
            ),
            facets=facets,
        )
        opts.update(kwargs)
        return SearchAppConfig.generate(opts, **overrides)

    def search_facets_config(self, available_facets, selected_facets=[]):
        facets_config = {}
        for facet_key, facet in available_facets.items():
            facets_config[facet_key] = {
                "facet": facet,
                "ui": {
                    "field": facet._params.get("field", facet_key),
                },
            }

        return FacetsConfig(facets_config, selected_facets)

    def communities_search_app_config(self, overrides={}, **kwargs):
        community_service = current_service_registry.get("communities")
        community_config = community_service.config
        search_facets = community_config.search.facets
        facets = self.search_facets_config(search_facets, search_facets.keys())
        opts = dict(
            app_id=self.communities_app_id,
            endpoint="/api/user/communities",
            headers={"Accept": "application/vnd.inveniordm.v1+json"},
            grid_view=False,
            sort=SortConfig(
                sort_options,
                sort_options,
                "newest",
                "newest",
            ),
            facets=facets,
        )
        opts.update(kwargs)
        return SearchAppConfig.generate(opts, **overrides)


class DashboardPageResource(TemplatePageUIResource):
    @login_required
    def render_DashboardRecordsPage(self, **kwargs):
        search_app_config = self.config.records_search_app_config(
            # TODO: patch for search app config issue in invenio https://github.com/inveniosoftware/invenio-search-ui/issues/196
            overrides={
                "defaultSortingOnEmptyQueryString": {"sortBy": "newest"},
                "overridableIdPrefix": f"{self.config.records_app_id}.Search",
                "ui_endpoint": "/docs",
            }
        )
        return self.render(
            "DashboardRecordsPage", search_app_config=search_app_config, **kwargs
        )

    @login_required
    def render_DashboardCommunitiesPage(self, **kwargs):
        search_app_config = self.config.communities_search_app_config(
            overrides={
                "defaultSortingOnEmptyQueryString": {"sortBy": "newest"},
                "overridableIdPrefix": f"{self.config.communities_app_id}.Search",
            }
        )
        return self.render(
            "DashboardCommunitiesPage", search_app_config=search_app_config, **kwargs
        )

    @login_required
    def render_DashboardRequestsPage(self, **kwargs):
        search_app_config = self.config.requests_search_app_config(
            overrides={
                "defaultSortingOnEmptyQueryString": {"sortBy": "newest"},
                "overridableIdPrefix": f"{self.config.requests_app_id}.Search",
            }
        )
        return self.render(
            "DashboardRequestsPage", search_app_config=search_app_config, **kwargs
        )


def create_blueprint(app):
    """Register blueprint for this resource."""
    app_blueprint = DashboardPageResource(DashboardPageResourceConfig()).as_blueprint()

    @app_blueprint.before_app_first_request
    def init_menu():
        user_dashboard = current_menu.submenu("user_dashboard")
        user_dashboard.submenu("records").register(
            "dashboard.render_DashboardRecordsPage",
            text=_("Records"),
            order=1,
        )

        user_dashboard.submenu("communities").register(
            "dashboard.render_DashboardCommunitiesPage",
            text=_("Communities"),
            order=2,
        )

        user_dashboard.submenu("requests").register(
            "dashboard.render_DashboardRequestsPage",
            text=_("Requests"),
            order=3,
        )
        # if you add dashboard to your project, the library adds itself to the main menu
        main_menu_dashboard = current_menu.submenu("main.dashboard")
        main_menu_dashboard.register(
            "dashboard.render_DashboardRecordsPage",
            _("Dashboard"),
            order=1,
        )

    return app_blueprint
