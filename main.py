from tkinter import *
from tkinter import ttk
from tkinter import filedialog
 
root = Tk()
root.title("Question generator")
root.geometry("1300x500")
 
root.grid_rowconfigure(index=0, weight=1)
root.grid_columnconfigure(index=0, weight=1)
root.grid_columnconfigure(index=1, weight=1)
root.grid_columnconfigure(index=2, weight=1)
root.grid_columnconfigure(index=3, weight=1)

text_editor = Text()
text_editor.grid(column=0, columnspan=2, row=0)

questions_text_editor = Text()
questions_text_editor.grid(column=2, columnspan=2, row=0)
 
# открываем файл в текстовое поле
def open_file():
    filepath = filedialog.askopenfilename()
    if filepath != "":
        with open(filepath, "r") as file:
            text =file.read()
            text_editor.delete("1.0", END)
            text_editor.insert("1.0", text)
 
# сохраняем текст из текстового поля в файл
def generate_questions():
    questions = "Самый главный вопрос? \n Ответ: 42"
    questions_text_editor.delete("1.0", END)
    questions_text_editor.insert("1.0", questions)
 
open_button = ttk.Button(text="Открыть файл", command=open_file)
open_button.grid(column=0, row=1, sticky=NSEW, padx=10)
 
save_button = ttk.Button(text="Сгенерировать вопросы", command=generate_questions)
save_button.grid(column=2, row=1, sticky=NSEW, padx=10)
 
root.mainloop()
