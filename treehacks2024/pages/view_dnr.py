import reflex as rx
from reflex.data import FormData
from .login import require_login

@rx.page(route="/view_dnr", title="View DNR + EOL Answers", image="/github.svg")
@require_login
def view_dnr() -> rx.Component:
    def on_submit(form_data: FormData) -> rx.event.EventSpec:
        #add way to save data to database later
        print(form_data)
        return rx.redirect("/submission_successful")

    def question_input(label: str, id: str) -> rx.Component:
        return rx.fragment(
            rx.text(label, margin_top="4px", margin_bottom="2px"),
            rx.input(id=id, placeholder="Type your answer here")
        )

    questions = [
        "Can you describe your understanding of your current health condition and how it might change in the future?",
        "How do you view the progression of your illness or condition?",
        # ... (add all other questions)
        "Are there specific concerns or fears about end-of-life that you would like to discuss or address?",
    ]

    form = rx.form(
        rx.vstack(
            *(question_input(question, f"question{i}") for i, question in enumerate(questions)),
            spacing="6"
        ),
        rx.button("Submit", type="submit", margin_top="20px"),
        on_submit=on_submit
    )

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
