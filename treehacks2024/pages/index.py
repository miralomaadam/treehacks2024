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
<<<<<<< HEAD
    top_image = rx.chakra.image(
        src="/Logo 0 - Teal.png", 
        height="30px", 
        width="100%",
        object_fit="cover"  
    )

=======
>>>>>>> parent of 3eada6a (Update index.py)
    sidebar = rx.chakra.box(
        rx.chakra.vstack(
            rx.chakra.image(src="/Logo 0 - Teal.png", width="200px", height="200px", align="center"),
            rx.chakra.divider(orientation="horizontal"),
            rx.chakra.box(rx.chakra.link("Schedule DNR Appointment", href="/schedule", display="block", text_align="center", padding="0.5em", border_radius="full", background="#097a87", color="white", font_size="0.4em", width="100%"), width="240px", height="80px", display="flex", justify_content="center", align_items="center"),
            rx.chakra.box(rx.chakra.link("Identify Preferred Medical Care", href="/dnr_eol", display="block", text_align="center", padding="0.5em", border_radius="full", background="#097a87", color="white", font_size="0.4em", width="100%"), width="240px", height="80px", display="flex", justify_content="center", align_items="center"),
            rx.chakra.box(rx.chakra.link("View DNR", href="/view_dnr", display="block", text_align="center", padding="0.5em", border_radius="full", background="#097a87", color="white", font_size="0.4em", width="100%"), width="240px", height="80px", display="flex", justify_content="center", align_items="center"),
            rx.chakra.box(rx.chakra.link("Find OT Interventions", href="/ot", display="block", text_align="center", padding="0.5em", border_radius="full", background="#097a87", color="white", font_size="0.4em", width="100%"), width="240px", height="80px", display="flex", justify_content="center", align_items="center"),
            rx.chakra.box(rx.chakra.link("Will", href="/will", display="block", text_align="center", padding="0.5em", border_radius="full", background="#097a87", color="white", font_size="0.4em", width="100%"), width="240px", height="80px", display="flex", justify_content="center", align_items="center"),
        ),
        width="30%",
        padding="5%",
        background_color="#FFFFFF" ,
    )

    main_content = rx.chakra.box(
        rx.chakra.heading("Welcome to AutonomyAid!", font_size="2em", color="#01353b"),
        rx.chakra.text("This a site that helps senior citizens get the medical care they want and need. "
            "Our company nameis AutonomyAid -- a union of two words at the center of our stated goal: "
            "we want to aid seniors with maintaining and regaining their autonomy to live out the last stage "
            "of their lives in the manner they best see fit. That autonomy encompasses making and communicating "
            "decisions about health care decisions, about representation of their interest should they become "
            "incapacitated, and about outlining the distribution of their assets. We are creating a Web-app "
            "(as opposed to a mobile app) to increase accessibility for elderly people who have access to public "
            "computers but may not have smart phones, or seniors who find smart phones incompatible with "
            "degenerative vision problems or decline in dexterity due to arthritis in their hands.",
            font_size="0.5em",
            margin_top="2em",
            padding="1em",),
        padding_top="10%",
        width="80%",
    )

    layout = rx.chakra.hstack(sidebar, main_content, direction="row", height="100vh", background_color="#dad6d2")

    return rx.fragment(
        layout,
        rx.chakra.color_mode_button(rx.chakra.color_mode_icon(), float="right"),
    )
