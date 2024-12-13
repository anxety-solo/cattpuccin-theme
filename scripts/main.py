from modules.script_callbacks import on_ui_settings
from modules.shared import OptionInfo, opts

import gradio as gr
import shutil
import re
import os

section = ("ctp", "Catppuccin Theme")

flavors: tuple[str] = ("anxety", "latte", "frappe", "macchiato", "mocha")
accents: tuple[str] = (
    "anxety",
    "rosewater",
    "flamingo",
    "pink",
    "mauve",
    "red",
    "maroon",
    "peach",
    "yellow",
    "green",
    "teal",
    "sky",
    "blue",
    "sapphire",
    "lavender",
)

script_path = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))

def on_accent_change():
    # replace the color
    with open(os.path.join(script_path, "style.css"), "r+") as file:
        pattern = re.compile(r"--ctp-accent:\s*(.*)")
        text = re.sub(
            pattern,
            f"--ctp-accent: var(--ctp-{opts.accent_color});",
            file.read(),
            count=1,
        )

        file.seek(0)
        file.write(text)
        file.truncate()

def on_flavor_change():
    # Move css over
    if gr.__version__ >= '4.40.0':
        source_css = os.path.join(script_path, f'flavors/gradio4/{opts.ctp_flavor}.css')
    else: 
        source_css = os.path.join(script_path, f'flavors/{opts.ctp_flavor}.css')

    # Copy the contents of the selected flavor CSS to style.css
    shutil.copy(source_css, os.path.join(script_path, 'style.css'))

    # re-appply accent color
    on_accent_change()

def on_settings():
    opts.add_option(
        "ctp_flavor",
        OptionInfo(
            default="anxety",
            label="Catppuccin Flavor",
            component=gr.Radio,
            component_args={"choices": flavors},
            onchange=on_flavor_change,
            section=section,
            category_id="ui",
        ),
    )

    opts.add_option(
        "accent_color",
        OptionInfo(
            default="anxety",
            label="Accent",
            component=gr.Radio,
            component_args={"choices": accents},
            onchange=on_accent_change,
            section=section,
            category_id="ui",
        ),
    )
    
    on_flavor_change()  # First Setup

on_ui_settings(on_settings)