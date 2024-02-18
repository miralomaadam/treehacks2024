import reflex as rx

from .login import require_login
from ..components import navbar


@rx.page(route="/medical", title="Medical Resources", image="/github.svg")
@require_login
def medical() -> rx.Component:
    top_image = rx.chakra.image(
        src="/Banner SVG.svg",  # Replace with the path to your image
        width="100%",
        object_fit="cover"  # Optional, for how the image should fit into the container
    )
    first_image = rx.chakra.image(
        src="/medical1.png",  # Replace with the path to your image
        width="100%",
        object_fit="cover"  # Optional, for how the image should fit into the container
    )

    second_image = rx.chakra.image(
        src="/medical2.png",  # Replace with the path to your image
        width="100%",
        object_fit="cover"  # Optional, for how the image should fit into the container
    )

    third_image = rx.chakra.image(
        src="/medical3.png",  # Replace with the path to your image
        width="100%",
        object_fit="cover"  # Optional, for how the image should fit into the container
    )

    fourth_image = rx.chakra.image(
        src="/medical4.png",  # Replace with the path to your image
        width="100%",
        object_fit="cover"  # Optional, for how the image should fit into the container
    )
    layout = rx.chakra.vstack(top_image, first_image, second_image, third_image, fourth_image, direction="column", height="100vh", background_color="#dad6d2")

    return rx.fragment(
        navbar('Medical Resources'),
        layout,
        rx.chakra.color_mode_button(rx.chakra.color_mode_icon(), float="right"),
    )