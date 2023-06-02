import cv2
import numpy as np
import pytesseract
from PIL import Image, ImageDraw
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import ImageTk

file_path = ""  # Объявление глобальной переменной
original_image = None  # Глобальная переменная для хранения оригинального изображения

def recognize_text(image_path):
    global original_image

    # Загрузка изображения
    image = cv2.imread(image_path)
    original_image = image.copy()  # Сохранение оригинального изображения

    # Создание нового изображения без выделенного текста
    image_without_text = image.copy()

    # Изменение размера изображения
    image_without_text = cv2.resize(image_without_text, (1280, 720))

    # Преобразование изображения в формат, поддерживаемый Tkinter
    image_tk = ImageTk.PhotoImage(Image.fromarray(image_without_text))

    # Отображение изображения без выделенного текста в окне программы
    image_label.config(image=image_tk)
    image_label.image = image_tk


def open_image():
    global file_path  # Объявление переменной file_path как глобальной

    # Открытие диалогового окна для выбора изображения
    file_path = filedialog.askopenfilename()

    if file_path:
        try:
            # Отображение изображения без выделенного текста
            recognize_text(file_path)
            button_recognize.config(state=tk.NORMAL)  # Разблокировка кнопки "Распознать текст"
        except Exception as e:
            messagebox.showerror("Ошибка", str(e))


def recognize_button_pressed():
    global original_image

    if original_image is not None:
        # Создание копии оригинального изображения
        image = original_image.copy()

        # Предобработка изображения
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        gray = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]

        # Применение Tesseract OCR для распознавания текста
        text = pytesseract.image_to_string(gray, lang='gost')

        # Распознавание границ текста
        data = pytesseract.image_to_data(gray, lang='gost', output_type=pytesseract.Output.DICT)

        # Создание нового изображения с выделенным текстом
        image_with_text = Image.fromarray(image)
        draw = ImageDraw.Draw(image_with_text)

        for i in range(len(data['text'])):
            if int(data['conf'][i]) > 20:
                x, y, w, h = data['left'][i], data['top'][i], data['width'][i], data['height'][i]
                draw.rectangle([x, y, x + w, y + h], outline='red')

        # Изменение размера изображения
        image_with_text = image_with_text.resize((1280, 720))

        # Преобразование изображения в формат, поддерживаемый Tkinter
        image_tk = ImageTk.PhotoImage(image_with_text)

        # Отображение изображения с распознанным текстом в окне программы
        image_label.config(image=image_tk)
        image_label.image = image_tk


# Создание графического интерфейса
window = tk.Tk()
window.title("Распознавание текста")
window.geometry("1280x760")

# Создание контейнера для изображения
image_frame = tk.Frame(window)
image_frame.grid(row=0, column=0, columnspan=2)

# Создание метки для изображения
image_label = tk.Label(image_frame)
image_label.grid(row=0, column=0)

# Создание кнопки "Открыть изображение"
button_open = tk.Button(window, text="Открыть изображение", command=open_image)
button_open.grid(row=1, column=0)

# Создание кнопки "Распознать текст"
button_recognize = tk.Button(window, text="Распознать текст", state=tk.DISABLED, command=recognize_button_pressed)
button_recognize.grid(row=1, column=1)

window.mainloop()
