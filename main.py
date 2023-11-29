from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from langchain.schema import HumanMessage, SystemMessage
from langchain.chat_models.gigachat import GigaChat
from langchain.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import Pinecone
from langchain.embeddings.openai import OpenAIEmbeddings
import pinecone
import os
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain

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
            text = file.read()
            text_editor.delete("1.0", END)
            text_editor.insert("1.0", text)
            return text

def chat_questions(user_input, chat):
    messages = [SystemMessage(
        content='Ты преподаватель, твоя цель сгенерировать вопросы по тексту, который ведёт пользователь, так чтобы проверить его знания по этому тексту, например: текст:{Меня зовут Алёна , мне 32 года}, твой вопрос:{Как тебя зовут?}')
        , HumanMessage(content=user_input)]
    res = chat(messages)
    messages.append(res)
    return res.content


# сохраняем текст из текстового поля в файл
def generate_questions():
    questions = start_place()
    questions_text_editor.delete("1.0", END)
    questions_text_editor.insert("1.0", questions)


def start_place():
    # Авторизация в сервисе GigaChat
    chat = GigaChat(
        credentials="MDQ0MzhkMTYtZTQ0NS00M2M0LWI5OGItNmRmZDdkYTNkZmFmOjA0MDliNzIzLTU0YjYtNDY3OC1iMjVjLTY4MjczYjExOWU3Yg==",
        verify_ssl_certs=False)
    user_input = open_file()
    #user_input = input("User: ")
    questions = chat_questions(user_input, chat=chat)
    return f"Вопросы: \n {questions}"


open_button = ttk.Button(text="Открыть файл", command=open_file)
open_button.grid(column=0, row=1, sticky=NSEW, padx=10)

save_button = ttk.Button(text="Сгенерировать вопросы", command=generate_questions)
save_button.grid(column=2, row=1, sticky=NSEW, padx=10)

root.mainloop()