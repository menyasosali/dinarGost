import cv2
import pytesseract
from PIL import Image, ImageDraw


def recognize_text(image_path):
    image = cv2.imread(image_path)
    original_image = image.copy()

    image_without_text = image.copy()
    image_without_text = cv2.resize(image_without_text, (1280, 720))

    return original_image, image_without_text


def process_image(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]

    text = pytesseract.image_to_string(gray, lang='gost')

    data = pytesseract.image_to_data(gray, lang='gost', output_type=pytesseract.Output.DICT)

    image_with_text = Image.fromarray(image)
    draw = ImageDraw.Draw(image_with_text)

    for i in range(len(data['text'])):
        if int(data['conf'][i]) > 60:
            x, y, w, h = data['left'][i], data['top'][i], data['width'][i], data['height'][i]
            draw.rectangle([x, y, x + w, y + h], outline='red')

    image_with_text = image_with_text.resize((1280, 720))

    return text, image_with_text
