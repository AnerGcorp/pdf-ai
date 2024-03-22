from typing import Any
from uuid import UUID
from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.chains import LLMChain
from langchain.callbacks.base import BaseCallbackHandler
from queue import Queue
from threading import Thread
from dotenv import load_dotenv

load_dotenv()

queue = Queue()

class StreamingHandler(BaseCallbackHandler):
    def on_llm_new_token(self, token: str, **kwargs: Any) -> Any:
        queue.put(token)

chat = ChatOpenAI(
    streaming=True,
    callbacks=[StreamingHandler()]
)

prompt = ChatPromptTemplate.from_messages([
    ("human", "{content}")
])

class StreamingChain(LLMChain):
    def stream(self, input):
        def task():
            self(input)

        Thread(target=task).start()

        while True:
            token = queue.get()
            yield token
chain = StreamingChain(llm=chat, prompt=prompt)

for output in chain.stream(input={'content': "Tell me a joke"}):
    print(output)