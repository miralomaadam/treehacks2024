import reflex as rx

from .login import require_login


@rx.page(route="/view_dnr", title="View DNR + EOL Answers", image="/github.svg")
@require_login
def view_dnr() -> rx.Component:
    return rx.fragment(
        rx.chakra.color_mode_button(rx.chakra.color_mode_icon(), float="right"),
        rx.vstack(
            rx.heading("View DNR + EOL Answers", font_size="2em"),
            rx.spacer(),
            spacing="4",
            padding_top="10%",
            align="center",
        ),
    )