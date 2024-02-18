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
    top_image = rx.chakra.image(
        src="/Banner SVG.svg",  # Replace with the path to your image
        width="100%",
        object_fit="cover"  # Optional, for how the image should fit into the container
    )

    # with rx.chakra.theme_provider():  # Commented out for now
    sidebar = rx.chakra.box(
        rx.chakra.vstack(
            #rx.chakra.image(src="/LogoSVG.svg", width="200px", height="200px", align="center"),
            rx.chakra.divider(orientation="horizontal"),
            rx.chakra.box(rx.chakra.link("Make DNR Appointment", href="/schedule", display="block", text_align="center", padding="0.5em", border_radius="full", background="#097a87", color="white", font_size="0.5em", width="100%"), width="96%", height="80px", display="flex", justify_content="center", align_items="center"),
            rx.chakra.box(rx.chakra.link("Medical Resources", href="/medical", display="block", text_align="center", padding="0.5em", border_radius="full", background="#097a87", color="white", font_size="0.5em", width="100%"), width="96%", height="80px", display="flex", justify_content="center", align_items="center"),
            rx.chakra.box(rx.chakra.link("Preferred Medical Care", href="/dnr_eol", display="block", text_align="center", padding="0.5em", border_radius="full", background="#097a87", color="white", font_size="0.5em", width="100%"), width="96%", height="80px", display="flex", justify_content="center", align_items="center"),
            #rx.chakra.box(rx.chakra.link("View DNR", href="/view_dnr", display="block", text_align="center", padding="0.5em", border_radius="full", background="#097a87", color="white", font_size="0.5em", width="100%"), width="280px", height="80px", display="flex", justify_content="center", align_items="center"),
            rx.chakra.box(rx.chakra.link("Find OT Interventions", href="/ot", display="block", text_align="center", padding="0.5em", border_radius="full", background="#097a87", color="white", font_size="0.5em", width="100%"), width="96%", height="80px", display="flex", justify_content="center", align_items="center"),
            rx.chakra.box(rx.chakra.link("Write Your Will", href="/will", display="block", text_align="center", padding="0.5em", border_radius="full", background="#097a87", color="white", font_size="0.5em", width="100%"), width="96%", height="80px", display="flex", justify_content="center", align_items="center"),
            rx.chakra.box(rx.chakra.link("Logout", on_click=State.do_logout, display="block", text_align="center", padding="0.5em", border_radius="full", background="#097a87", color="white", font_size="0.5em", width="100%"), width="96%", height="80px", display="flex", justify_content="center", align_items="center"),
        ),
        width="18%",
        padding="2.5%",
        background_color="#FFFFFF",
    )

    main_content = rx.chakra.box(
        #rx.chakra.heading("Welcome to AutonomyAid!", font_size="2em", color="#01353b"),
        rx.chakra.text("In the journey of life, everyone deserves dignity, understanding, and autonomy, especially during the golden years. At AutonomyAid, we believe in empowering our elderly community with seamless, accessible healthcare solutions tailored for end-of-life care. Our web-based application is crafted with simplicity and ease of use in mind, making it perfect for those who may not have a smartphone but can access public computers. With AutonomyAid, you can confidently manage your healthcare decisions directly from your fingertips.",
            font_size="0.7em",
            #margin_top="0.5em",
            padding="1em",
            ),
        rx.text.strong("Key Features: ",            
            font_size="0.7em",
            #margin_top="0.5em",
            padding="1em",
            ),
        rx.unordered_list(
            rx.list_item("Direct DNR Management: Securely set up appointments with healthcare providers to sign a Do Not Resuscitate (DNR) order. Your DNR will be automatically uploaded to your electronic health record, ensuring your wishes are respected without relying on intermediaries.", font_size="0.7em", left_padding="1em"),
            rx.list_item("Intuitive Health Chatbot: Our friendly chatbot is here to listen to your health concerns. It gently guides you through questions about your ailments and suggests occupational therapy interventions to alleviate symptoms and improve your quality of life.", font_size="0.7em", left="1em"),
            rx.list_item("Ethical Guidance for Tough Decisions: Life's hardest choices shouldn't be faced alone. Our platform provides clear, compassionate answers to complex medical ethics questions beyond DNR directives, like considerations for surgeries that could impact motor function or sensory abilities.", font_size="0.7em", left="1em"),
        ),
        
        #padding_top="0%",
        width="80%",
    )

    layout = rx.chakra.vstack(top_image, rx.chakra.hstack(sidebar, main_content, direction="row", height="100vh", background_color="#dad6d2"))

    return rx.fragment(
        layout,
        rx.chakra.color_mode_button(rx.chakra.color_mode_icon(), float="right"),
    )
