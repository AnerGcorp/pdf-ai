from langchain.chat_models import ChatOpenAI

def build_llm(char_args):
    return ChatOpenAI()