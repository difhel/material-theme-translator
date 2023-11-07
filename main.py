import zipfile
import locals
import os


while (result_1 := input(locals.locale_1)) not in ["n", "y"]:
    ...
if result_1 == "n":
    import webbrowser
    webbrowser.open("https://m3.material.io/theme-builder")

result_2 = input(locals.locale_2)
result_3 = result_2
if result_2.endswith(".zip"):
    print("Trying to unzip the file...")
    if not os.path.isfile(result_2):
        print("Error: file not found.")
        exit(0)
    with zipfile.ZipFile(result_2, 'r') as zip_ref:
        zip_ref.extractall(os.getcwd() + "/material_theme")
        result_3 = os.getcwd() + "/material_theme"

if not os.path.isfile(result_3 + "/css/tokens.css"):
    print(f"Error: file ${result_3}/css/tokens.css not found. You may have specified the wrong folder path or the archive has the wrong format.")
    exit(0)

colors = []
themes = []

blocks_colors = {
    "primary": False,
    "secondary": False,
    "tertiary": False,
    "neutral": False,
    "neutral-variant": False,
    "error": False
}

blocks_themes = {
    "light": False,
    "dark": False
}

is_block_colors_open = False
is_block_themes_open = False

def get_color_name(text):
    index = next(i for i, c in enumerate(text) if c.isdigit())
    return text[:index]

with open(result_3 + "/css/tokens.css") as file:
    tokens = file.read()
    print("Writing colors...")
    for line in tokens.split("\n"):
        if line.strip().startswith("--md-ref-palette"):
            # working with colors
            color_line = line.strip().split("--md-ref-palette-")[-1]
            color_name = get_color_name(color_line)
            if not blocks_colors[color_name]:
                if is_block_colors_open:
                    colors.append("}\n\n")
                colors.append(f"/* {color_name.capitalize()} colors */\n")
                colors.append("html {\n")
                is_block_colors_open = True
                blocks_colors[color_name] = True
            if color_name in blocks_colors:
                colors.append(f"    --{color_name}-{color_line.split(color_name)[-1]}\n")
        if line.strip().startswith("--md-sys-color"):
            if is_block_colors_open:
                colors.append("}\n")
                is_block_colors_open = False

            color_line = line.strip().split("--md-sys-color-")[-1]
            color_name = color_line[::-1].split("-", maxsplit=1)[-1][::-1]
            color_theme = color_line.split("-")[-1].split(":")[0]
            color_value = color_line.split(": ")[-1].split(";")[0]
            
            if not blocks_themes[color_theme]:
                if is_block_themes_open:
                    themes.append("}\n\n")
                themes.append(f"/* {color_theme.capitalize()} theme */\n")
                themes.append(f"html:has(* > .{color_theme}) {'{'}\n")
                is_block_themes_open = True
                blocks_themes[color_theme] = True
            themes.append(f"    --{color_name}: {color_value};\n")
    if is_block_themes_open:
        themes.append("}")
        is_block_themes_open = False

with open("output.css", "w") as f:
    f.write(locals.copyright)
    for c in colors:
        f.write(c)
    for c in themes:
        f.write(c)

print(f"Done. Colors has been written to {os.getcwd()}/output.css")