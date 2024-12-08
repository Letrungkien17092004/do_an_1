from django.shortcuts import render
from .chatBot import ChatBot
# Create your views here.
chatBot = ChatBot()
def chat(messageInput):
    chatResponse = chatBot.chat(messageInput)
    return chatResponse