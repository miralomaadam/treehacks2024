import reflex as rx


def navbar(heading: str, hide_home: bool = False) -> rx.Component:
    components = [
        rx.heading(heading, font_size="1em", ),
        rx.spacer(),
        rx.chakra.color_mode_button(rx.chakra.color_mode_icon(), float="right")
    ]
    if not hide_home:
        components.insert(2,
        rx.chakra.button("Home", on_click=rx.redirect("/")))
    return rx.hstack(
        *components,
        position="fixed",
        top="0px",
        background_color="lightgray",
        padding="1em",
        height="3em",
        width="100%",
        z_index="5",
    )

