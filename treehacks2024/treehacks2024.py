import reflex as rx

from .pages import index

app = rx.App(style={"font_size": "40px", rx.button: {"font_size": "40px", "padding": "50px 50px"}})
app.add_page(index)