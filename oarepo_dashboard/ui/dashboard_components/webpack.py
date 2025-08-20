from invenio_assets.webpack import WebpackThemeBundle

theme = WebpackThemeBundle(
    __name__,
    ".",
    default="semantic-ui",
    themes={
        "semantic-ui": {
            "entry": {
                "dashboard_components": "./js/dashboard_components/custom-components.js"
            },
            "dependencies": {},
            "devDependencies": {},
            "aliases": {"@js/dashboard_components": "./js/dashboard_components/search"},
        }
    },
)
