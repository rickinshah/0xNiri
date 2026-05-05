#!/usr/bin/env python3

import sys
import numpy as np
import json
from skimage import color
from skimage.color import deltaE_ciede2000

# --------------------------------------------------
# Palette
# --------------------------------------------------
PALETTE = {
    "adwaita": "#93c0ea",
    "black": "#4f4f4f",
    "blue": "#5294e2",
    "bluegrey": "#6c7a89",
    "breeze": "#3daee9",
    "brown": "#a0743c",
    "carmine": "#a30002",
    "cyan": "#00bcd4",
    "darkcyan": "#008b8b",
    "deeporange": "#ff5722",
    "green": "#4caf50",
    "grey": "#9e9e9e",
    "indigo": "#3f51b5",
    "magenta": "#e91e63",
    "nordic": "#5e81ac",
    "orange": "#ff9800",
    "palebrown": "#d7a86e",
    "paleorange": "#ffb74d",
    "pink": "#ff6fae",
    "red": "#e53935",
    "teal": "#009688",
    "violet": "#9c27b0",
    "white": "#ffffff",
    "yaru": "#e95420",
    "yellow": "#fbc02d",
    # Catppuccin Mocha
    "cat-mocha-rosewater": "#f5e0dc",
    "cat-mocha-flamingo": "#f2cdcd",
    "cat-mocha-pink": "#f5c2e7",
    "cat-mocha-mauve": "#cba6f7",
    "cat-mocha-red": "#f38ba8",
    "cat-mocha-maroon": "#eba0ac",
    "cat-mocha-peach": "#fab387",
    "cat-mocha-yellow": "#f9e2af",
    "cat-mocha-green": "#a6e3a1",
    "cat-mocha-teal": "#94e2d5",
    "cat-mocha-sky": "#89dceb",
    "cat-mocha-sapphire": "#74c7ec",
    "cat-mocha-blue": "#89b4fa",
    "cat-mocha-lavender": "#b4befe",
    # Catppuccin Macchiato
    "cat-macchiato-rosewater": "#f4dbd6",
    "cat-macchiato-flamingo": "#f0c6c6",
    "cat-macchiato-pink": "#f5bde6",
    "cat-macchiato-mauve": "#c6a0f6",
    "cat-macchiato-red": "#ed8796",
    "cat-macchiato-maroon": "#ee99a0",
    "cat-macchiato-peach": "#f5a97f",
    "cat-macchiato-yellow": "#eed49f",
    "cat-macchiato-green": "#a6da95",
    "cat-macchiato-teal": "#8bd5ca",
    "cat-macchiato-sky": "#91d7e3",
    "cat-macchiato-sapphire": "#7dc4e4",
    "cat-macchiato-blue": "#8aadf4",
    "cat-macchiato-lavender": "#b7bdf8",
    # Catppuccin Frappe
    "cat-frappe-rosewater": "#f2d5cf",
    "cat-frappe-flamingo": "#eebebe",
    "cat-frappe-pink": "#f4b8e4",
    "cat-frappe-mauve": "#ca9ee6",
    "cat-frappe-red": "#e78284",
    "cat-frappe-maroon": "#ea999c",
    "cat-frappe-peach": "#ef9f76",
    "cat-frappe-yellow": "#e5c890",
    "cat-frappe-green": "#a6d189",
    "cat-frappe-teal": "#81c8be",
    "cat-frappe-sky": "#99d1db",
    "cat-frappe-sapphire": "#85c1dc",
    "cat-frappe-blue": "#8caaee",
    "cat-frappe-lavender": "#babbf1",
    # Catppuccin Latte
    "cat-latte-rosewater": "#dc8a78",
    "cat-latte-flamingo": "#dd7878",
    "cat-latte-pink": "#ea76cb",
    "cat-latte-mauve": "#8839ef",
    "cat-latte-red": "#d20f39",
    "cat-latte-maroon": "#e64553",
    "cat-latte-peach": "#fe640b",
    "cat-latte-yellow": "#df8e1d",
    "cat-latte-green": "#40a02b",
    "cat-latte-teal": "#179299",
    "cat-latte-sky": "#04a5e5",
    "cat-latte-sapphire": "#209fb5",
    "cat-latte-blue": "#1e66f5",
    "cat-latte-lavender": "#7287fd",
}


# --------------------------------------------------
# Helpers
# --------------------------------------------------
def hex_to_rgb01(hex_color: str) -> np.ndarray:
    hex_color = hex_color.lstrip("#")
    return (
        np.array([int(hex_color[i : i + 2], 16) for i in (0, 2, 4)], dtype=float)
        / 255.0
    )


def hex_to_lab(hex_color: str) -> np.ndarray:
    rgb = hex_to_rgb01(hex_color)
    return color.rgb2lab(rgb.reshape(1, 1, 3))[0, 0]


def delta_e(lab1: np.ndarray, lab2: np.ndarray) -> float:
    return deltaE_ciede2000(lab1.reshape(1, 1, 3), lab2.reshape(1, 1, 3))[0, 0]


# Precompute Lab
PALETTE_LAB = {name: hex_to_lab(hex_val) for name, hex_val in PALETTE.items()}


# --------------------------------------------------
# ANSI color block
# --------------------------------------------------
def color_block(hex_color: str, width=2):
    hex_color = hex_color.lstrip("#")
    r, g, b = [int(hex_color[i : i + 2], 16) for i in (0, 2, 4)]
    return f"\033[48;2;{r};{g};{b}m{' ' * width}\033[0m"


# --------------------------------------------------
# Find top N
# --------------------------------------------------
def top_n_colors(target_hex: str, n=5):
    target_lab = hex_to_lab(target_hex)

    distances = []
    for name, lab in PALETTE_LAB.items():
        dist = delta_e(target_lab, lab)
        distances.append((name, dist))

    distances.sort(key=lambda x: x[1])
    return distances[:n]


# --------------------------------------------------
# CLI
# --------------------------------------------------
def main():
    if len(sys.argv) < 2:
        print("Usage: match_color.py <hex>")
        sys.exit(1)

    target = sys.argv[1]

    if not target.startswith("#") or len(target) != 7:
        print("Invalid hex color. Use format: #RRGGBB")
        sys.exit(1)

    print("\nInput color:", end=" ")
    print(color_block(target), target)

    top_colors = top_n_colors(target, 5)

    print("\nChoose color for icon theme:\n")

    for i, (name, dist) in enumerate(top_colors, 1):
        hex_val = PALETTE[name]
        print(f"{i}. {color_block(hex_val)} {hex_val}")

    # selection
    try:
        choice = int(input("\nChoose a color (1-5): "))
        if not (1 <= choice <= 5):
            raise ValueError
    except ValueError:
        choice = 1

    selected_name, selected_dist = top_colors[choice - 1]
    selected_hex = PALETTE[selected_name]

    print("\nSelected:", end=" ")
    print(color_block(selected_hex), selected_name, selected_hex)

    print(
        json.dumps(
            {
                "input": target,
                "selected": selected_name,
                "hex": selected_hex,
                "delta_e": selected_dist,
            }
        ),
        flush=True,
    )


if __name__ == "__main__":
    main()
