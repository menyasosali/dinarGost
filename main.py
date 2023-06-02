import cv2
import numpy as np
import pytesseract
from PIL import Image, ImageDraw
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import ImageTk

file_path = ""
original_image = None

def recognize_text(image_path):
    global original_image

    image = cv2.imread(image_path)
    original_image = image.copy()

    image_without_text = image.copy()
    image_without_text = cv2.resize(image_without_text, (1280, 720))

    image_tk = ImageTk.PhotoImage(Image.fromarray(image_without_text))

    image_label.config(image=image_tk)
    image_label.image = image_tk


def open_image():
    global file_path

    file_path = filedialog.askopenfilename()

    if file_path:
        try:
            recognize_text(file_path)
            button_recognize.config(state=tk.NORMAL)
        except Exception as e:
            messagebox.showerror("Ошибка", str(e))


def recognize_button_pressed():
    global original_image

    if original_image is not None:
        image = original_image.copy()

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

        image_tk = ImageTk.PhotoImage(image_with_text)

        image_label.config(image=image_tk)
        image_label.image = image_tk


window = tk.Tk()
window.title("Распознавание текста")
window.geometry("1280x750")

image_label = tk.Label(window)
image_label.pack()

button_open = tk.Button(window, text="Открыть изображение", command=open_image)
button_open.pack()

button_recognize = tk.Button(window, text="Распознать текст", state=tk.DISABLED, command=recognize_button_pressed)
button_recognize.pack()

window.mainloop()
