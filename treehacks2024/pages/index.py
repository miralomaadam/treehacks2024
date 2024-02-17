"""The home page of the app."""

from treehacks2024 import styles

import reflex as rx

from .login import require_login


@rx.page(route="/", title="Home", image="/github.svg")
@require_login
def index() -> rx.Component:
    """Render the index page.

    Returns:
        A reflex component.
    """
    return rx.fragment(
        rx.chakra.color_mode_button(rx.chakra.color_mode_icon(), float="right"),
        rx.vstack(
            rx.heading("Welcome!", font_size="2em"),
            rx.spacer(),
            rx.link(rx.button("Schedule DNR appointment"), href="/schedule", high_contrast=True),
            rx.link(rx.button("Sign DNR + Answer EOL Questions"), href="/dnr_eol", high_contrast=True),
            rx.link(rx.button("View DNR"), href="/view_dnr", high_contrast=True),
            rx.link(rx.button("Find OT interventions"), href="/ot", high_contrast=True),
            rx.link(rx.button("Will"), href="/will", high_contrast=True),
            rx.button("Logout", on_click=rx.redirect("/logout"), float="right", size="4", high_contrast=True),
            spacing="4",
            padding_top="10%",
            align="center",
        ),
    )