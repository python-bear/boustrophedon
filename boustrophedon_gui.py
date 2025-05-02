import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageDraw, ImageFont
from textwrap import wrap


def justify_line(text: str, font, target_width: int, full_justify: bool = True):
    words = text.split()
    if len(words) == 1 or not full_justify:
        return [(word, font.getlength(" ")) for word in words[:-1]] + [(words[-1], 0)]

    dummy_img = Image.new("RGB", (1, 1))
    draw = ImageDraw.Draw(dummy_img)
    word_widths = [draw.textlength(word, font=font) for word in words]
    total_words_width = sum(word_widths)
    total_spacing = target_width - total_words_width
    spacing_between = total_spacing / (len(words) - 1)

    return [(word, spacing_between) for word in words[:-1]] + [(words[-1], 0)]


def render_boustrophedon_image(paragraphs: list, line_char_limit: int = 90, font_size: int = 19, scale: int = 4,
                               output_path: str = "boustrophedon.png", font_path: str = "times.ttf"):
    font = ImageFont.truetype(font_path, font_size * scale)
    img_width = int(700 * (line_char_limit / 90) * scale)
    line_height = (font_size + 10) * scale

    all_lines = []
    line_directions = []
    for para in paragraphs:
        lines = wrap(para, width=line_char_limit)
        for line in lines:
            all_lines.append(line)
            line_directions.append(len(line_directions) % 2 == 0)

    img_height = line_height * len(all_lines) + 10 * scale
    image = Image.new("RGB", (img_width, img_height), color="white")
    draw = ImageDraw.Draw(image)

    line_index = 0
    for para in paragraphs:
        lines = wrap(para, width=line_char_limit)
        for l_idx, line in enumerate(lines):
            y = line_index * line_height + 5 * scale
            is_last_line = (l_idx == len(lines) - 1)
            left_to_right = (line_index % 2 == 0)
            justified = justify_line(line, font, img_width - 20 * scale, full_justify=not is_last_line)

            if left_to_right:
                x = 10 * scale
                for word, spacing in justified:
                    draw.text((x, y), word, font=font, fill="black")
                    x += draw.textlength(word, font=font) + spacing
            else:
                temp = Image.new("RGB", (img_width, line_height), "white")
                temp_draw = ImageDraw.Draw(temp)
                x_temp = 10 * scale
                for word, spacing in justified:
                    temp_draw.text((x_temp, 0), word, font=font, fill="black")
                    x_temp += temp_draw.textlength(word, font=font) + spacing
                flipped = temp.transpose(Image.FLIP_LEFT_RIGHT)
                image.paste(flipped, (0, y))

            line_index += 1

    image.save(output_path)
    image.show()


def generate_image():
    try:
        text = text_box.get("1.0", tk.END).strip().split("\n")
        char_limit = int(char_limit_entry.get())
        font_size = int(font_size_entry.get())
        scale = int(scale_entry.get())

        output_path = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("PNG files", "*.png")],
            title="Save Boustrophedon Image As"
        )

        if not output_path:
            messagebox.showerror("Error", f"User cancelled process.")
            return

        render_boustrophedon_image(
            paragraphs=text,
            line_char_limit=char_limit,
            font_size=font_size,
            scale=scale,
            output_path=output_path
        )
        messagebox.showinfo("Success", f"Image saved to:\n{output_path}")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to generate image:\n{e}")


root = tk.Tk()
root.title("Boustrophedon Renderer")

tk.Label(root, text="Text To Render:").pack()
text_box = tk.Text(root, height=15, width=70, wrap="word")
text_box.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

form_frame = tk.Frame(root)
form_frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

tk.Label(form_frame, text="Line Char Limit: (default=90)").grid(row=0, column=0, sticky="e")
char_limit_entry = tk.Entry(form_frame)
char_limit_entry.insert(0, "90")
char_limit_entry.grid(row=0, column=1, padx=5, pady=5, sticky="NESW")

tk.Label(form_frame, text="Font Size: (default=19)").grid(row=1, column=0, sticky="e")
font_size_entry = tk.Entry(form_frame)
font_size_entry.insert(0, "19")
font_size_entry.grid(row=1, column=1, padx=5, pady=5, sticky="NESW")

tk.Label(form_frame, text="Scale: (default=4)").grid(row=2, column=0, sticky="e")
scale_entry = tk.Entry(form_frame)
scale_entry.insert(0, "4")
scale_entry.grid(row=2, column=1, padx=5, pady=5, sticky="NESW")

tk.Button(root, text="Generate Rendered Image", command=generate_image).pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

root.mainloop()
