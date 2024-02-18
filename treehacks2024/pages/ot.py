import reflex as rx

from .login import require_login
from ..components import chat, action_bar, navbar


@rx.page(title="Find OT Interventions", image="/github.svg")
@require_login
def ot() -> rx.Component:
    return rx.fragment(
        rx.vstack(
            navbar("Find OT Interventions"),
            rx.container(style={"height": "1em"}),
            chat(),
            action_bar(),
            spacing="4",
            padding_top="10%",
            align="center",
        ),
    )