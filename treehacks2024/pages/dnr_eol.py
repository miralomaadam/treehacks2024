import reflex as rx

from .login import require_login
from ..components import navbar

question_style = {
    "bg": "white",
    "padding": "2em",
    "border_radius": "100px",
    "width": "90%",
    "align_items": "start",
}

@rx.page(route="/dnr_eol", title="Questions & Answers About Preferred Medical Care ", image="/github.svg")
@require_login
def dnr_eol() -> rx.Component:

    top_image = rx.chakra.image(
        src="/Banner SVG.svg",  # Replace with the path to your image
        width="100%",
        object_fit="cover"  # Optional, for how the image should fit into the container
    )
    
    def go_home() -> rx.event.EventSpec:
        return rx.redirect('/')

    def on_submit() -> rx.event.EventSpec:
        # save data to a database later
        return rx.redirect('/dnr_eol')
    
    def question_input(label: str, id: str) -> rx.Component:
        return rx.fragment(
            rx.text(label, margin_top="2px", margin_bottom="2px"),
            rx.input(id=id, placeholder="Type your answer here"),
            style=question_style
        )

    sidebar = rx.chakra.box(
    rx.chakra.vstack(
        rx.chakra.box(
            #rx.chakra.link("Return to Home", href="/", display="block", text_align="center", padding="0.5em", border_radius="full", background="#097a87", color="white", font_size="0.5em", width="100%"),
            padding_bottom="1em",  # Add padding below the button if needed
        ),
        rx.chakra.divider(orientation="horizontal"),
        # You can add more components here if needed
    ),
    width="10%",
    padding="2.5%",
    background_color="#FFFFFF",
    display="flex",
    flex_direction="column",
    justify_content="flex-start",  # This aligns children to the start of the flex container
)
    
    questions = [
        "Can you describe your understanding of your current health condition and how it might change in the future?",
        "How do you view the progression of your illness or condition?",
        "In situations where treatment might extend your life but not cure your illness, how would you like us to proceed?",
        "If you had to choose, would you prefer a longer life with potential discomfort or a shorter life with less discomfort?",
        "What are your most important considerations for comfort and quality of life?",
        "How do you feel about receiving care that focuses solely on managing symptoms, such as pain or nausea, rather than treating the underlying illness?",
        "How do you feel about receiving medical treatments that doctors may consider unlikely to improve your condition?",
        "In what circumstances, if any, would you find a medical treatment to be futile or not worth undergoing?",
        "Who would you trust to make medical decisions on your behalf if you're unable to do so yourself? Please provide the contact information for at least one individual.",
        "Would you prefer this person to make decisions based strictly on your stated preferences, or also consider their own judgment and feelings?",
        "What does a good quality of life mean to you in the context of your illness?",
        "Are there specific conditions or outcomes that you would find unacceptable for your quality of life?",
        "How do you feel about the impact of the cost of your care on your family or society?",
        "Would your preferences change if a treatment is particularly costly or resource-intensive?",
        "Do you have any specific wishes or instructions you want to be followed regarding end-of-life care?",
        "Have you completed an advanced directive or living will, and if so, can you share the details?",
        "Are there any personal, cultural, or religious beliefs that should be considered in your end-of-life care?",
        "How do you view the practice of organ transplantation?",
        "How do you view the use of stem cells in regenerative medicine?",
        "How do these beliefs affect your views on medical interventions and quality of life?",
        "What kind of emotional or psychological support would be most helpful for you during end-of-life care?",
        "Are there specific concerns or fears about end-of-life that you would like to discuss or address?",
    ]

    form = rx.form(
        rx.vstack(
            *(question_input(question, f"question{i}") for i, question in enumerate(questions)),
            spacing="6"
        ),
        rx.button("Submit", type="submit", margin_top="20px", on_click=on_submit, 
                color="white", width="6em", padding="1em"),
        style=question_style
    )

    return rx.fragment(
    rx.vstack(
        navbar('Preferred Medical Care'),  # This will place the image at the top of the page
        rx.spacer(padding="3em"),
        form,
        spacing="4",
        align="center",
    )
)


