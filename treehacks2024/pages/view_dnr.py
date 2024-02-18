import reflex as rx

from .login import require_login
from ..components import navbar


@rx.page(route="/view_dnr", title="View DNR + EOL Answers", image="/github.svg")
@require_login
def view_dnr() -> rx.Component:
    return rx.fragment(
        rx.vstack(
            navbar("View DNR + EOL Answers"),
            rx.container(style={"height": "1em"}),
            spacing="4",
            padding_top="10%",
            align="center",
        ),
    )