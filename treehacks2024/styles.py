"""Styles for the app."""

import reflex as rx

border_radius = "0.375rem"
box_shadow = "0px 0px 0px 1px rgba(84, 82, 95, 0.14)"
border = "1px solid #F4F3F6"
text_color = "black"
accent_text_color = "#1A1060"
accent_color = "#F5EFFE"
hover_accent_color = {"_hover": {"color": accent_color}}
hover_accent_bg = {"_hover": {"bg": accent_color}}
content_width_vw = "90vw"
sidebar_width = "20em"

bg_dark_color = "#111"
bg_medium_color = "#222"

border_color = "#fff3"

accennt_light = "#6649D8"
accent_color = "#5535d4"
accent_dark = "#4c2db3"

icon_color = "#fff8"

text_light_color = "#fff"
shadow_light = "rgba(17, 12, 46, 0.15) 0px 48px 100px 0px;"
shadow = "rgba(50, 50, 93, 0.25) 0px 50px 100px -20px, rgba(0, 0, 0, 0.3) 0px 30px 60px -30px, rgba(10, 37, 64, 0.35) 0px -2px 6px 0px inset;"

message_style = dict(display="inline-block", p="4", border_radius="xl", max_w="30em")

input_style = dict(
    bg=bg_medium_color,
    border_color=border_color,
    border_width="1px",
    p="4",
)

icon_style = dict(
    font_size="md",
    color=icon_color,
    _hover=dict(color=text_light_color),
    cursor="pointer",
    w="8",
)

sidebar_style = dict(
    border="double 1px transparent;",
    border_radius="10px;",
    background_image=f"linear-gradient({bg_dark_color}, {bg_dark_color}), radial-gradient(circle at top left, {accent_color},{accent_dark});",
    background_origin="border-box;",
    background_clip="padding-box, border-box;",
    p="2",
    _hover=dict(
        background_image=f"linear-gradient({bg_dark_color}, {bg_dark_color}), radial-gradient(circle at top left, {accent_color},{accennt_light});",
    ),
)


template_page_style = {"padding_top": "5em", "padding_x": ["auto", "2em"], "flex": "1"}

template_content_style = {
    "align_items": "flex-start",
    "box_shadow": box_shadow,
    "border_radius": border_radius,
    "padding": "1em",
    "margin_bottom": "2em",
}

link_style = {
    "color": text_color,
    "text_decoration": "none",
    **hover_accent_color,
}

button_style = {
    "color": text_color,
    "text_decoration": "none",
    "font-size": "25px",
    **hover_accent_color,
}

overlapping_button_style = {
    "background_color": "white",
    "border": border,
    "border_radius": border_radius,
}

base_style = {
    "font_size": "40px",
    rx.button: {"font_size": "40px", "padding": "50px 50px"},
    rx.chakra.Avatar: {
        "shadow": shadow,
        "color": text_light_color,
        "bg": border_color,
    },
    rx.chakra.Button: {
        "shadow": shadow,
        "color": text_light_color,
        "_hover": {
            "bg": accent_dark,
        },
    },
    rx.chakra.Menu: {
        "bg": bg_dark_color,
        "border": f"red",
    },
    rx.chakra.MenuList: {
        "bg": bg_dark_color,
        "border": f"1.5px solid {bg_medium_color}",
    },
    rx.chakra.MenuDivider: {
        "border": f"1px solid {bg_medium_color}",
    },
    rx.chakra.MenuButton: {
        "width": "3em",
        "height": "3em",
        **overlapping_button_style,
    },
    rx.chakra.MenuItem: {
        "bg": bg_dark_color,
        "color": text_light_color,
        **hover_accent_bg},
    rx.chakra.DrawerContent: {
        "bg": bg_dark_color,
        "color": text_light_color,
        "opacity": "0.9",
    },
    rx.chakra.Hstack: {
        "align_items": "center",
        "justify_content": "space-between",
    },
    rx.chakra.Vstack: {
        "align_items": "stretch",
        "justify_content": "space-between",
    },
}

markdown_style = {
    "code": lambda text: rx.chakra.code(text, color="#1F1944", bg="#EAE4FD"),
    "a": lambda text, **props: rx.chakra.link(
        text,
        **props,
        font_weight="bold",
        color="#03030B",
        text_decoration="underline",
        text_decoration_color="#AD9BF8",
        _hover={
            "color": "#AD9BF8",
            "text_decoration": "underline",
            "text_decoration_color": "#03030B",
        },
    ),
}
