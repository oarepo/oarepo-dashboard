from invenio_assets.webpack import WebpackThemeBundle

theme = WebpackThemeBundle(
    __name__,
    ".",
    default="semantic-ui",
    themes={
        "semantic-ui": {
            "entry": {
                "dashboard_records": "./js/dashboard/records/index.js",
                "dashboard_communities": "./js/dashboard/communities/index.js",
                "dashboard_requests": "./js/dashboard/requests/index.js",
                "dashboard_components": "./js/custom-components.js",
            },
            "dependencies": {},
            "devDependencies": {},
            "aliases": {
                "@translations/oarepo_dashboard": "translations/oarepo_dashboard/i18next.js"
            },
        }
    },
)
