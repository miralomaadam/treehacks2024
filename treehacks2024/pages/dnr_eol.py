import reflex as rx

from .login import require_login


@rx.page(route="/dnr_eol", title="Sign DNR + Answer EOL Questions", image="/github.svg")
@require_login
def dnr_eol() -> rx.Component:
    return rx.fragment(
        rx.chakra.color_mode_button(rx.chakra.color_mode_icon(), float="right"),
        rx.vstack(
            rx.heading("Sign DNR + Answer EOL Questions", font_size="2em"),
            rx.spacer(),
            spacing="4",
            padding_top="10%",
            align="center",
        ),
    )