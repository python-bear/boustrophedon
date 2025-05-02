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

    # Process lines from all paragraphs
    all_lines = []
    line_directions = []  # Track LTR/RTL for each line
    for p_idx, para in enumerate(paragraphs):
        lines = wrap(para, width=line_char_limit)
        for l_idx, line in enumerate(lines):
            all_lines.append(line)
            direction = (len(line_directions) % 2 == 0)
            line_directions.append(direction)

    img_height = line_height * len(all_lines) + 10 * scale
    image = Image.new("RGB", (img_width, img_height), color="white")
    draw = ImageDraw.Draw(image)

    line_index = 0
    for para in paragraphs:
        lines = wrap(para, width=line_char_limit)
        for l_idx, line in enumerate(lines):
            y = line_index * line_height + 5  * scale
            is_last_line = (l_idx == len(lines) - 1)
            left_to_right = (line_index % 2 == 0)
            justified = justify_line(line, font, img_width - 20 * scale, full_justify=not is_last_line)

            if left_to_right:
                x = 10 * scale
                for word, spacing in justified:
                    draw.text((x, y), word, font=font, fill="black")
                    x += draw.textlength(word, font=font) + spacing
            else:
                # Draw to temp image and flip
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


text = """Grendel comes, the great march-stepper, bearing God’s anger. He seizes and kills one of the sleeping warriors. Then he advances towards Beowulf. A fierce and desperate hand-to-hand struggle ensues. No arms are used, both combatants trusting to strength and hand-grip. Beowulf tears Grendel’s shoulder from its socket, and the monster retreats to his den, howling and yelling with agony and fury. The wound is fatal.

The next morning, at early dawn, warriors in numbers flock to the hall Heorot, to hear the news. Joy is boundless. Glee runs high. Hrothgar and his retainers are lavish of gratitude and of gifts.

Grendel’s mother, however, comes the next night to avenge his death. She is furious and raging. While Beowulf is sleeping in a room somewhat apart [x]from the quarters of the other warriors, she seizes one of Hrothgar’s favorite counsellors, and carries him off and devours him. Beowulf is called. Determined to leave Heorot entirely purified, he arms himself, and goes down to look for the female monster. After traveling through the waters many hours, he meets her near the sea-bottom. She drags him to her den. There he sees Grendel lying dead. After a desperate and almost fatal struggle with the woman, he slays her, and swims upward in triumph, taking with him Grendel’s head.

Joy is renewed at Heorot. Congratulations crowd upon the victor. Hrothgar literally pours treasures into the lap of Beowulf; and it is agreed among the vassals of the king that Beowulf will be their next liegelord.

Beowulf leaves Dane-land. Hrothgar weeps and laments at his departure.

When the hero arrives in his own land, Higelac treats him as a distinguished guest. He is the hero of the hour.

Beowulf subsequently becomes king of his own people, the Geats. After he has been ruling for fifty years, his own neighborhood is wofully harried by a fire-spewing dragon. Beowulf determines to kill him. In the ensuing struggle both Beowulf and the dragon are slain. The grief of the Geats is inexpressible. They determine, however, to leave nothing undone to honor the memory of their lord. A great funeral-pyre is built, and his body is burnt. Then a memorial-barrow is made, visible from a great distance, that sailors afar may be constantly reminded of the prowess of the national hero of Geatland.

The poem closes with a glowing tribute to his bravery, his gentleness, his goodness of heart, and his generosity.""".split("\n")

render_boustrophedon_image(text, line_char_limit=50, font_size=19, scale=4)
