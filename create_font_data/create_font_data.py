from PIL import Image, ImageDraw, ImageFont
import os
import textwrap
import random
import csv
import uuid


def create_font_dataset():
    base_dir = "fonts_dataset"
    split_dirs = ["train", "val", "test"]
    for split in split_dirs:
        os.makedirs(os.path.join(base_dir, split), exist_ok=True)

    with open("font_phrases.txt", "r", encoding="utf-8") as font_phrases:
        phrases = [font_phrases.readline().strip() for _ in range(40)]

    fonts = {
        "BrushScriptMT": "brushscriptmtrusbyme_italic.otf",
        "ComicSansMS": "comic.ttf",
        "DINPro": "dinpro.otf",
        "FuturaPTBook": "FuturaPTBook.otf",
        "Garamond": "GARA.TTF",
        "Georgia": "georgia.ttf",
        "GothamPro": "gothampromedium.ttf",
        "HelveticaNeue": "helveticaneuecyr_roman.otf",
        "Lobster": "Lobster-Regular.ttf",
        "MontserratMedium": "Montserrat-Medium.ttf",
        "Pacifico": "Pacifico-Regular.ttf",
        "PlayfairDisplay": "PlayfairDisplay.ttf",
        "ProximaNova": "proximanova_regular.ttf",
        "Raleway": "Raleway-v4020-Regular.otf",
        "Roboto": "Roboto.ttf",
        "TimesNewRoman": "times.ttf"
    }

    background_colors = [
        (255, 255, 255),
        (230, 230, 250),
        (255, 228, 196),
        (176, 224, 230),
        (210, 180, 140)
    ]

    width, height = 640, 640
    text_color = (0, 0, 0)
    line_spacing = 1.2

    all_images = []

    for font_name, font_file in fonts.items():
        font_path = os.path.join("fonts", font_file)
        if not os.path.exists(font_path):
            print(f"Error with font: {font_path}")
            continue

        try:
            font = ImageFont.truetype(font_path, 50)
        except Exception as e:
            print(f"{e}: {font_name}")
            continue

        for phrase in phrases:
            wrapped_lines = textwrap.wrap(phrase, width=20)
            for bg_color in background_colors:
                img = Image.new('RGB', (width, height), bg_color)
                draw = ImageDraw.Draw(img)

                y = (height - len(wrapped_lines) * font.size * line_spacing) / 2
                for line in wrapped_lines:
                    text_width = draw.textlength(line, font=font)
                    x = (width - text_width) / 2
                    draw.text((x, y), line, font=font, fill=text_color)
                    y += font.size * line_spacing

                all_images.append((img, font_name))

    random.shuffle(all_images)

    total = len(all_images)
    train_end = int(total * 0.65)
    test_end = train_end + int(total * 0.25)

    split_bounds = {
        "train": all_images[:train_end],
        "test": all_images[train_end:test_end],
        "val": all_images[test_end:]
    }

    labels = []

    for split, data in split_bounds.items():
        for img, font_name in data:
            unique_id = uuid.uuid4().hex
            filename = f"{font_name}_{unique_id}.png"
            filepath = os.path.join(base_dir, split, filename)
            img.save(filepath)
            labels.append([filepath, font_name])

    with open(os.path.join(base_dir, "labels.csv"), "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["filepath", "label"])
        writer.writerows(labels)

    print("Dataset is ready")


if __name__ == "__main__":
    create_font_dataset()