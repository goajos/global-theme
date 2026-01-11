import pywal
from PIL import Image, ImageColor
import re
from pathlib import Path

BACKGROUNDS = "/home/jappe/Pictures/Backgrounds"
MODULES = "/home/jappe/.config/arch-config/modules"
theme_modules: dict[str, dict[str, str | list[str | tuple[str, str, str | list[str]]]]] = {
    "alacritty": {
        "config": f"{MODULES}/alacritty/dotfiles/alacritty/themes/theme.toml",
        "patterns": [
                (r'background = \"#[0-9a-fA-F]{6}\"', 'background = "{color}"', "background"),
                (r'foreground = \"#[0-9a-fA-F]{6}\"', 'foreground = "{color}"', "foreground"),
                (r'text = \"#[0-9a-fA-F]{6}\"', 'text = "{color}"', "foreground"),
                (r'cursor = \"#[0-9a-fA-F]{6}\"', 'cursor = "{color}"', "cursor"),
                (r'normal.black = \"#[0-9a-fA-F]{6}\"', 'normal.black = "{color}"', "color0"),
                (r'normal.red = \"#[0-9a-fA-F]{6}\"', 'normal.red = "{color}"', "color1"),
                (r'normal.green = \"#[0-9a-fA-F]{6}\"', 'normal.green = "{color}"', "color2"),
                (r'normal.yellow = \"#[0-9a-fA-F]{6}\"', 'normal.yellow = "{color}"', "color3"),
                (r'normal.blue = \"#[0-9a-fA-F]{6}\"', 'normal.blue = "{color}"', "color4"),
                (r'normal.magenta = \"#[0-9a-fA-F]{6}\"', 'normal.magenta = "{color}"',"color5"),
                (r'normal.cyan = \"#[0-9a-fA-F]{6}\"', 'normal.cyan = "{color}"',"color6"),
                (r'normal.white = \"#[0-9a-fA-F]{6}\"', 'normal.white = "{color}"', "color7"),
                (r'bright.black = \"#[0-9a-fA-F]{6}\"', 'bright.black = "{color}"', "color8"),
                (r'bright.red = \"#[0-9a-fA-F]{6}\"', 'bright.red = "{color}"', "color9"),
                (r'bright.green = \"#[0-9a-fA-F]{6}\"', 'bright.green = "{color}"', "color10"),
                (r'bright.yellow = \"#[0-9a-fA-F]{6}\"', 'bright.yellow = "{color}"', "color11"),
                (r'bright.blue = \"#[0-9a-fA-F]{6}\"', 'bright.blue = "{color}"', "color12"),
                (r'bright.magenta = \"#[0-9a-fA-F]{6}\"', 'bright.magenta = "{color}"', "color13"),
                (r'bright.cyan = \"#[0-9a-fA-F]{6}\"', 'bright.cyan = "{color}"', "color14"),
                (r'bright.white = \"#[0-9a-fA-F]{6}\"', 'bright.white = "{color}"', "color15"),
            ],
        },
    "fuzzel": {
        "config": f"{MODULES}/fuzzel/dotfiles/fuzzel/fuzzel.ini",
        "patterns": [
                (r"background=[0-9a-fA-F]{6}80", "background={color}80", "background"),
                (r"text=[0-9a-fA-F]{8}", "text={color}ff", "foreground"),
                (r"prompt=[0-9a-fA-F]{8}", "prompt={color}ff", "foreground"), # >
                (r"input=[0-9a-fA-F]{8}", "input={color}ff", "foreground"), # input text
                (r"match=[0-9a-fA-F]{8}", "match={color}ff", "color6"), # non selection bar match
                (r"selection=[0-9a-fA-F]{6}80", "selection={color}80", "color14"), # selection bar
                (r"selection-match=[0-9a-fA-F]{8}", "selection-match={color}ff", "color6"), # selection bar match
                (r"selection-text=[0-9a-fA-F]{8}", "selection-text={color}ff", "background"), # selection bar text
                (r"border=[0-9a-fA-F]{8}", "border={color}ff", "color6"),
            ],
        },
    "gtklock": {
        "config": f"{MODULES}/niri/idle/dotfiles/gtklock/style.css",
        "patterns": [
                r'background-image: url\("[^"]+"\)',
            ],
        },
    "mako": {
        "config": f"{MODULES}/mako/dotfiles/mako/config",
        "patterns": [
               (r"background-color=#[0-9a-fA-F]{6}80", "background-color={color}80", "background"),
               (r"text-color=#[0-9a-fA-F]{8}", "text-color={color}ff", "foreground"),
               (r"border-color=#[0-9a-fA-F]{8}", "border-color={color}ff", "color6"),
               (r"progress-color=over #[0-9a-fA-F]{6}80", "progress-color=over {color}80", "color14"),
            ],
        },
    "niri-colors": {
        "config": f"{MODULES}/niri/dotfiles/niri/config.kdl",
        "patterns": [
                (r'active-gradient from="#[0-9a-fA-F]{6}ff" to="#[0-9a-fA-F]{6}ff" angle-0', 'active-gradient from="{color0}ff" to="{color1}ff" angle=0', ["color6", "color2"])
                # (r'active-color "#[0-9a-fA-F]{6}ff"', 'active-color "{color}ff"', "color14"),
                # (r'urgent-color "#[0-9a-fA-F]{6}ff"', 'urgent-color "{color}ff"', "foreground")
            ],
            
        },
    "niri-image": {
        "config": f"{MODULES}/niri/dotfiles/niri/config.kdl",
        "patterns": [
                r'spawn-sh-at-startup "swww img -n niri-background [^"]+"+',
                r'spawn-sh-at-startup "swww img -n niri-overview [^"]+"+',
            ],
        },
    "nvim": {
        "config": f"{MODULES}/nvim/dotfiles/nvim/lua/config/theme.lua",
        "patterns": [
                (r'background = \"#[0-9a-fA-F]{6}\"', 'background = "{color}"', "background"),
                (r'foreground = \"#[0-9a-fA-F]{6}\"', 'foreground = "{color}"', "foreground"),
                (r'text = \"#[0-9a-fA-F]{6}\"', 'text = "{color}"', "foreground"),
                (r'cursor = \"#[0-9a-fA-F]{6}\"', 'cursor = "{color}"', "cursor"),
                (r'black = \"#[0-9a-fA-F]{6}\"', 'black = "{color}"', "color0"),
                (r'red = \"#[0-9a-fA-F]{6}\"', 'red = "{color}"', "color1"),
                (r'green = \"#[0-9a-fA-F]{6}\"', 'green = "{color}"', "color2"),
                (r'yellow = \"#[0-9a-fA-F]{6}\"', 'yellow = "{color}"', "color3"),
                (r'blue = \"#[0-9a-fA-F]{6}\"', 'blue = "{color}"', "color4"),
                (r'magenta = \"#[0-9a-fA-F]{6}\"', 'magenta = "{color}"',"color5"),
                (r'cyan = \"#[0-9a-fA-F]{6}\"', 'cyan = "{color}"',"color6"),
                (r'white = \"#[0-9a-fA-F]{6}\"', 'white = "{color}"', "color7"),
                (r'bright_black = \"#[0-9a-fA-F]{6}\"', 'bright_black = "{color}"', "color8"),
                (r'bright_red = \"#[0-9a-fA-F]{6}\"', 'bright_red = "{color}"', "color9"),
                (r'bright_green = \"#[0-9a-fA-F]{6}\"', 'bright_green = "{color}"', "color10"),
                (r'bright_yellow = \"#[0-9a-fA-F]{6}\"', 'bright_yellow = "{color}"', "color11"),
                (r'bright_blue = \"#[0-9a-fA-F]{6}\"', 'bright_blue = "{color}"', "color12"),
                (r'bright_magenta = \"#[0-9a-fA-F]{6}\"', 'bright_magenta = "{color}"', "color13"),
                (r'bright_cyan = \"#[0-9a-fA-F]{6}\"', 'bright_cyan = "{color}"', "color14"),
                (r'bright_white = \"#[0-9a-fA-F]{6}\"', 'bright_white = "{color}"', "color15"),
            ],
        },
    }


def replace_colors_in_config(module_key, colors):
    module = theme_modules[module_key]
    config_path = Path(module["config"])

    with open(config_path, "r") as fid:
        config = fid.read()

    for pattern_idx, (pattern, replacement, color_key) in enumerate(module["patterns"]):
        if module_key == "fuzzel":
            config = re.sub(
                pattern,
                replacement.format(color=colors[color_key][1:]),
                config
            )
        elif module_key == "niri-colors":
            config = re.sub(
                pattern,
                replacement.format(color0=colors[color_key[0]], color1=colors[color_key[1]]),
                config
            )
        else:
            config = re.sub(
                pattern,
                replacement.format(color=colors[color_key]),
                config
            )

    with open(config_path, "w") as fid:
        fid.write(config)

def replace_image_in_config(module, replacements):
    config_path = Path(module["config"])
    with open(config_path, "r") as fid:
        config = fid.read()

    for pattern_idx, pattern in enumerate(module["patterns"]):
        config = re.sub(
            pattern,
            replacements[pattern_idx],
            config
        )

    with open(config_path, "w") as fid:
        fid.write(config)

def show_color_reference(flat_colors):
    print("\n" + "="*60)
    print("COLOR REFERENCE")
    print("="*60)
    for key, color in flat_colors.items():
        rgb = ImageColor.getrgb(color)
        ansi_bg = f"\033[38;2;{rgb[0]};{rgb[1]};{rgb[2]}m"
        reset = "\033[0m"
        print(f"{key:20} {color:10} {ansi_bg}█████{reset}")
    print("="*60 + "\n")

def main():
    image_path = Path(f"{BACKGROUNDS}/lofi-boy.jpg")
    # image_path = Path(f"{BACKGROUNDS}/adventure-time.jpg")
    image = pywal.image.get(image_path)
    colors = pywal.colors.get(image)
    flat_colors = {
        **colors["special"], **colors["colors"]
    }

    show_color_reference(flat_colors)

    color_hex = flat_colors["color14"]
    color_rgb = ImageColor.getrgb(color_hex)
    overview_image = Image.new("RGB", (1920,1080), color_rgb)
    overview_path = Path(f"{BACKGROUNDS}/solid_{color_hex}.jpg")
    overview_image.save(overview_path) 

    niri_replacements = [
        f'spawn-sh-at-startup "swww img -n niri-background {image_path}"',
        f'spawn-sh-at-startup "swww img -n niri-overview {overview_path}"',
    ]
    replace_image_in_config(theme_modules["niri-image"], niri_replacements)

    gtklock_replacements = [
        f'background-image: url("{image_path}")'
    ]
    replace_image_in_config(theme_modules["gtklock"], gtklock_replacements)

    replace_colors_in_config("alacritty", flat_colors)
    replace_colors_in_config("fuzzel", flat_colors)
    replace_colors_in_config("mako", flat_colors)
    replace_colors_in_config("niri-colors", flat_colors)
    replace_colors_in_config("nvim", flat_colors)

main()
