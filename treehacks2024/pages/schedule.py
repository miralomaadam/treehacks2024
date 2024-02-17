import reflex as rx

from .login import require_login


@rx.page(title="Schedule Appointment", image="/github.svg")
@require_login
def schedule() -> rx.Component:
    return rx.fragment(
        rx.chakra.color_mode_button(rx.chakra.color_mode_icon(), float="right"),
        rx.vstack(
            rx.heading("Schedule Appointment", font_size="2em"),
            rx.spacer(),
            spacing="4",
            padding_top="10%",
            align="center",
        ),
    )