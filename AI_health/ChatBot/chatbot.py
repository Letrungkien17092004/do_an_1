from nltk.chat.util import Chat, reflections
from .conversation import CONVERSATION_PAIR
# Khởi tạo chatbot với các câu hỏi và câu trả lời


class ChatBot:
    def __init__(self):
        self.model = Chat(CONVERSATION_PAIR)
    def chat(self, text_vi):
        text_vi = text_vi.lower()
        response = self.model.respond(text_vi)
        return response

