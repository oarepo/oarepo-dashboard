from oarepo_ui.resources.template_pages import TemplatePageUIResourceConfig, TemplatePageUIResource


class ComponentsResourceConfig(TemplatePageUIResourceConfig):
    url_prefix = "/me"
    blueprint_name = "dashboard_components"
    template_folder = "templates"


def create_blueprint(app):
    """Register blueprint for this resource."""
    return TemplatePageUIResource(ComponentsResourceConfig()).as_blueprint()
