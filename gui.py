import tkinter as tk
from tkinter import filedialog, messagebox, Toplevel
from PIL import ImageTk
from image_processing import recognize_text, process_image
from database import save_text_to_database


file_path = ""
original_image = None


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

        text, image_with_text = process_image(image)

        save_text_to_database(text)

        image_tk = ImageTk.PhotoImage(image_with_text)

        image_label.config(image=image_tk)
        image_label.image = image_tk

        button_read_text.config(state=tk.NORMAL)


def read_text_button_pressed():
    global original_image

    if original_image is not None:
        image = original_image.copy()

        text, _ = process_image(image)

        text_window = Toplevel(window)
        text_window.title("Текст")
        text_window.geometry("640x780")

        text_label = tk.Label(text_window, text=text, wraplength=600, justify=tk.LEFT)
        text_label.pack()


def main():
    window = tk.Tk()
    window.title("Распознавание текста")
    window.geometry("1280x780")

    image_label = tk.Label(window)
    image_label.pack()

    button_frame = tk.Frame(window)
    button_frame.pack(side=tk.BOTTOM)

    button_open = tk.Button(button_frame, text="Открыть изображение", command=open_image)
    button_open.pack(side=tk.LEFT)

    button_read_text = tk.Button(button_frame, text="Чтение текста", state=tk.DISABLED, command=read_text_button_pressed)
    button_read_text.pack(side=tk.LEFT)

    button_recognize = tk.Button(button_frame, text="Распознать текст", state=tk.DISABLED, command=recognize_button_pressed)
    button_recognize.pack(side=tk.LEFT)

    window.mainloop()
