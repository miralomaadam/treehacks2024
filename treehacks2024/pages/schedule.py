from datetime import datetime

import reflex as rx

from .login import require_login
from ..state import State
from ..components import navbar


@rx.page(title="Schedule Appointment", image="/github.svg")
@require_login
def schedule() -> rx.Component:
    return rx.fragment(
        rx.vstack(
            navbar("Schedule Appointment"),
            rx.container(style={"height": "1em"}),
            rx.select(items=[
                "Katelynn Upham (0.6 miles)", "Anhthu Lewis (1.0 miles)", "Jaclyn Bilello (1.1 miles)", "Rekha Avirah (2.0 miles)",
                # "Timothy Heja Tsung (0.1 miles)", "Leigh Ann Fraley (0.6 miles)", "Char Armitage (0.6 miles)", "Yesenia Perez (0.6 miles)", "Marissa G. Hall (0.6 miles)", "Drina Adams (1.2 miles)", "Katrina Sarkissian (5.6 miles)"
            ]),
            rx.spacer(),
            rx.form(
                rx.hstack(
                    rx.text(
                        "Date & Time",
                        color="hsl(240, 5%, 64.9%)",
                        margin_top="2px",
                        margin_bottom="4px",
                    ),
                    rx.input(
                        placeholder="date",
                        id="date",
                        border_color="hsl(240,3.7%,15.9%)",
                        justify_content="center",
                        type="date",
                        #value=datetime.now().strftime("%Y-%m-%d"),
                        style={"font-size": "3rem", "height": "100px"},
                    ),
                    rx.spacer(),
                    rx.input(
                        placeholder="time",
                        id="time",
                        border_color="hsl(240,3.7%,15.9%)",
                        justify_content="center",
                        type="time",
                        #value=datetime.now().strftime("%H:%M"),
                        style={"font-size": "3rem", "height": "100px"},
                    ),
                    padding_top="14px",
                ),
                rx.spacer(),
                rx.button(
                    "Schedule",
                    type="submit",
                    width="100%",
                ),
                on_submit=State.schedule_appointment,
            ),
            spacing="4",
            padding_top="10%",
            align="center",
        ),
    )