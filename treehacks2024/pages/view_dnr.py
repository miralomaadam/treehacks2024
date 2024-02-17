import reflex as rx
from .login import require_login

@rx.page(route="/view_dnr", title="View DNR + EOL Answers", image="/github.svg")
@require_login
def view_dnr() -> rx.Component:
    # Function to handle form submission
    def on_submit() -> rx.event.EventSpec:
        # Implement submission logic as per Reflex documentation
        # Example: Save form data, display a message, or redirect to another page
        # For now, we'll just redirect to the same page as a placeholder
        return rx.redirect('/view_dnr')

    # Create input fields for each question
    def question_input(label: str, id: str) -> rx.Component:
        return rx.fragment(
            rx.text(label, margin_top="4px", margin_bottom="2px"),
            rx.input(id=id, placeholder="Type your answer here")
        )

    # List of questions
    questions = [
        "Can you describe your understanding of your current health condition and how it might change in the future?",
        "How do you view the progression of your illness or condition?",
        # ... (add all other questions here)
        "Are there specific concerns or fears about end-of-life that you would like to discuss or address?",
    ]

    # Create a form with all the questions
    form = rx.form(
        rx.vstack(
            *(question_input(question, f"question{i}") for i, question in enumerate(questions)),
            spacing="6"
        ),
        rx.button("Submit", type="submit", margin_top="20px", on_click=on_submit)
    )

    # Layout the page
    return rx.fragment(
        rx.chakra.color_mode_button(rx.chakra.color_mode_icon(), float="right"),
        rx.vstack(
            rx.heading("View DNR + EOL Answers", font_size="2em"),
            form,
            spacing="4",
            padding_top="10%",
            align="center",
        )
    )
