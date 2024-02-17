import reflex as rx

from .pages import index
from .styles import base_style

app = rx.App(style=base_style)
app.add_page(index)