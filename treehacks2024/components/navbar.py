import reflex as rx


def navbar(heading: str, hide_home: bool = False) -> rx.Component:
    components = [
        rx.spacer(),
        rx.heading(heading, font_size="1em", padding="0.35em 2.5vw 0 0", color="black", justify="center"),
        #rx.chakra.color_mode_button(rx.chakra.color_mode_icon(), float="right",
        #                    style={"font-size": "30px", "height": "80px", "line-height": "80px"},)
        rx.chakra.button("Home", on_click=rx.redirect("/"),
                         style={"font-size": "20px", "height": "60px", "line-height": "60px"}, justify="center")
    ]
    #if not hide_home:
    #    components.insert(2,
    #    rx.chakra.button("Home", on_click=rx.redirect("/"), style={"font-size": "30px", "height": "80px", "line-height": "80px"},))
    return rx.vstack(
        rx.chakra.image(
            src="/Banner SVG.svg",  # Replace with the path to your image
            object_fit="cover",  # Optional, for how the image should fit into the container
            position="fixed",
            top="0px",
            width="100%",
            z_index="4",
        ),
        rx.hstack(
            *components,
            position="fixed",
            top="0px",
            padding="3vw 2.5vw 2.5vw 2.5vw",
            height="3em",
            width="100%",
            z_index="5",
            justify="center",
        ),
        width="100%",
        #height="200px",
        padding="0px",
        margin="0px",

    )

