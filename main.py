from tkinter import *
from tkinter import ttk
from tkinter import filedialog
import requests
from bs4 import BeautifulSoup
from langchain.schema import HumanMessage, SystemMessage
from langchain.chat_models.gigachat import GigaChat
from langchain.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import Pinecone
from langchain.embeddings.openai import OpenAIEmbeddings
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
root.grid_columnconfigure(index=4, weight=1)
root.grid_columnconfigure(index=5, weight=1)

text_editor_label = Label(text="Текст")
text_editor_label.grid(column=0, columnspan=2, row=0)
text_editor = Text()
text_editor.grid(column=0, columnspan=2, row=1)

questions_text_editor_label = Label(text="Вопросы")
questions_text_editor_label.grid(column=2, columnspan=2, row=0)
questions_text_editor = Text()
questions_text_editor.grid(column=2, columnspan=2, row=1)

answers_text_editor_label = Label(text="Ответы")
answers_text_editor_label.grid(column=4, columnspan=2, row=0)
answers_text_editor = Text()
answers_text_editor.grid(column=4, columnspan=2, row=1)


def open_file():
    filepath = filedialog.askopenfilename()
    if filepath != "":
        with open(filepath, "r", encoding = "utf-8") as file:
            text = file.read()
            text_editor.delete("1.0", END)
            text_editor.insert("1.0", text)
            print("Проверка1")
            return text


def chat_questions(user_input, chat):
    messages = [SystemMessage(
        content='Ты преподаватель, твоя цель сгенерировать 5 - 6 вопросов по тексту, который ведёт пользователь, так чтобы проверить его знания по этому тексту, например: текст:{Меня зовут Алёна , мне 32 года}, твой вопрос:{Как тебя зовут?}')
        , HumanMessage(content=user_input)]
    res = chat(messages)
    messages.append(res)
    print("Проверка2")

    return res.content


def chat_answer(questions, chat):
    messages = [SystemMessage(
        content='Тебе надо сгенерировать ответы на вопросы по тексту, который тебе пришлёт пользователь'),
        HumanMessage(content=questions)]
    res = chat(messages)
    messages.append(res)
    return res.content

class ChatBot:
    chat = GigaChat(
        credentials="MDQ0MzhkMTYtZTQ0NS00M2M0LWI5OGItNmRmZDdkYTNkZmFmOjA0MDliNzIzLTU0YjYtNDY3OC1iMjVjLTY4MjczYjExOWU3Yg==",
        verify_ssl_certs=False)
    

def generate_questions():
    user_input = text_editor.get("1.0", "end")
    questions = chat_questions(user_input, chat=ChatBot.chat)
    #questions = start_place(user_input, chat_questions)
    questions_text_editor.delete("1.0", END)
    questions_text_editor.insert("1.0", questions)
    print(questions)

def generate_answer():
    text = text_editor.get("1.0", "end") + questions_text_editor.get("1.0", "end")
    answers = chat_answer(text, chat=ChatBot.chat)
    answers_text_editor.delete("1.0", END)
    answers_text_editor.insert("1.0", answers)
    print(answers)


def get_text_by_url():
    url = url_entry.get()
    rs = requests.get(url)
    root = BeautifulSoup(rs.content, 'html.parser')
    print(root)
    paragraphs = root.find_all('p')
    text_for_viewing = ""
    for p in paragraphs:
        text_for_viewing+=p.text
    text_editor.delete("1.0", END)
    text_editor.insert("1.0", text_for_viewing)


open_button = ttk.Button(text="Открыть файл", command=open_file)
open_button.grid(column=0, row=2, sticky=NSEW, padx=10)

url_entry = ttk.Entry(text="Открыть статью по ссылке")
url_entry.grid(column=0, row=3, sticky=NSEW, padx=10)
open_url_button = ttk.Button(text="Открыть статью по ссылке", command=get_text_by_url)
open_url_button.grid(column=1, row=3, sticky=NSEW, padx=10)

generate_questions_button = ttk.Button(text="Сгенерировать вопросы", command=generate_questions)
generate_questions_button.grid(column=2, row=2, sticky=NSEW, padx=10)

get_answers_button = ttk.Button(text="Ответить на вопросы", command=generate_answer)
get_answers_button.grid(column=4, row=2, sticky=NSEW, padx=10)

root.mainloop()
