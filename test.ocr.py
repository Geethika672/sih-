import pytesseract
from PIL import Image, ImageDraw
from pytesseract import Output
import re

pytesseract.pytesseract.tesseract_cmd = (
    r"C:\Program Files\Tesseract-OCR\tesseract.exe"
)

image = Image.open(
    r"C:\Desktop\PRIVI-BROWSER\extension\backend\test.png"
)

data = pytesseract.image_to_data(
    image,
    output_type=Output.DICT
)

draw = ImageDraw.Draw(image)

for i, word in enumerate(data["text"]):

    word = word.strip()

    if not word:
        continue

    x = data["left"][i]
    y = data["top"][i]
    w = data["width"][i]
    h = data["height"][i]

    # Phone number → hide only the number
    if re.fullmatch(r"\d{10}", word):
        draw.rectangle(
            [x, y, x + w, y + h],
            fill="black"
        )
        print("📱 Phone number redacted")

    # Password → hide only the value, NOT the label
    if re.search(r"password", word, re.IGNORECASE):

        # Cover area to the right of "password:"
        draw.rectangle(
            [x + w, y, x + w + 150, y + h],
            fill="black"
        )

        print("🔐 Password value redacted")

output_path = (
    r"C:\Desktop\PRIVI-BROWSER\extension\backend\protected.png"
)

image.save(output_path)

print("\n✅ Protected screenshot saved!")
print(output_path)