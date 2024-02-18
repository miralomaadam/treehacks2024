from treehacks2024 import styles
import reflex as rx
from .login import require_login
from ..state import State


@rx.page(route="/", title="Home", image="/github.svg")
@require_login
def index() -> rx.Component:
    """Render the index page.

    Returns:
        A reflex component.
    """
    # with rx.chakra.theme_provider():  # Commented out for now
    sidebar = rx.chakra.box(
        rx.chakra.vstack(
            rx.chakra.divider(orientation="horizontal"),
            rx.chakra.link("Schedule DNR Appointment", href="/schedule"),
            rx.chakra.link("Answer Questions About Preferred Medical Care", href="/dnr_eol"),
            rx.chakra.link("View DNR", href="/view_dnr"),
            rx.chakra.link("Find OT Interventions", href="/ot"),
            rx.chakra.link("Will", href="/will"),
        ),
        width="20%",
        padding="5%",
        background_color="#FFFFFF" ,
    )

    main_content = rx.chakra.box(
        rx.chakra.heading("Welcome!", font_size="2em"),
        padding_top="10%",
        width="80%",
    )

    layout = rx.chakra.hstack(sidebar, main_content, direction="row", height="100vh")

    return rx.fragment(
        layout,
        rx.chakra.color_mode_button(rx.chakra.color_mode_icon(), float="right"),
    )
