import reflex as rx

from .login import require_login
from ..components import chat, action_bar, navbar


@rx.page(title="Find OT Interventions", image="/github.svg")
@require_login
def ot() -> rx.Component:
    return rx.fragment(
        rx.vstack(
            navbar("Find OT Interventions"),
            rx.spacer(padding="2em"),
            rx.vstack(
            chat(),
            action_bar(),
            border_radius="10px",
            border="2px solid lightgrey",
            padding="0 10px 0 10px",
            ),
            spacing="4",
            padding_top="10%",
            align="center",
        ),
    )