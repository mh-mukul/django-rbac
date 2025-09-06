import os
from dotenv import load_dotenv
from django.urls import reverse_lazy
from django.templatetags.static import static
from django.utils.translation import gettext_lazy as _

load_dotenv()
DJANGO_ENV = os.getenv("DJANGO_ENV", "dev")


def environment_callback() -> list[str]:
    """
    Callback has to return a list of two values represeting text value and the color
    type of the label displayed in top right corner.
    """
    # return ["Production", "danger"]  # info, danger, warning, success
    return {
        "dev": ["Development", "info"],
        "staging": ["Staging", "warning"],
        "prod": ["Production", "danger"],
    }.get(DJANGO_ENV.lower(), ["Development", "info"])


UNFOLD_CONFIG = {
    "SITE_TITLE": "Django RBAC",
    "SITE_URL": "/",
    "SITE_ICON": {
        "light": lambda request: static("icon-light.svg"),  # light mode
        "dark": lambda request: static("icon-dark.svg"),  # dark mode
    },
    "SITE_LOGO": {
        "light": lambda request: static("logo-light.svg"),  # light mode
        "dark": lambda request: static("logo-dark.svg"),  # dark mode
    },
    "SHOW_HISTORY": True,  # show/hide "History" button, default: True
    "ENVIRONMENT": environment_callback(),  # environment name in header
    "LOGIN": {
        "image": lambda request: static("sample/login-bg.jpg"),
        "redirect_after": lambda request: reverse_lazy("admin:APP_MODEL_changelist"),
    },
    "COMMAND": {
        "search_models": True,  # Default: False
        "show_history": True,  # Enable history
    },
    "SIDEBAR": {
        "show_search": True,
        "command_search": True,
        "show_all_applications": True,
        "navigation": [
            {
                "title": _("Authorization"),
                "icon": "lock",
                "collapsible": True,
                "items": [
                    {
                        "title": _("Modules"),
                        "link": reverse_lazy("admin:authorization_module_changelist"),
                        "icon": "list",
                    },
                    {
                        "title": _("Permissions"),
                        "link": reverse_lazy("admin:authorization_permission_changelist"),
                        "icon": "verified_user",
                    },
                    {
                        "title": _("Roles"),
                        "link": reverse_lazy("admin:authorization_role_changelist"),
                        "icon": "assignment_ind",
                    },
                    {
                        "title": _("Role Permissions"),
                        "link": reverse_lazy("admin:authorization_rolepermission_changelist"),
                        "icon": "security",
                    },
                ],
            },
            {
                "items": [
                    {
                        "title": _("Organizations"),
                        "link": reverse_lazy("admin:organization_organization_changelist"),
                        "icon": "business_center",
                    },
                ],
            },
            {
                "items": [
                    {
                        "title": _("Users"),
                        "link": reverse_lazy("admin:user_user_changelist"),
                        "icon": "people",
                    },
                ],
            },
        ],
    },
}
