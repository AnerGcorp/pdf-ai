from typing import Any
from uuid import UUID
from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.chains import LLMChain
from langchain.callbacks.base import BaseCallbackHandler
from queue import Queue
from threading import Thread
from dotenv import load_dotenv
from langchain.schema.output import LLMResult

load_dotenv()

class StreamingHandler(BaseCallbackHandler):
    def __init__(self, queue):
        self.queue = queue

    def on_llm_new_token(self, token: str, **kwargs: Any) -> Any:
        self.queue.put(token)
    
    def on_llm_end(self, response: LLMResult, **kwargs: Any) -> Any:
        self.queue.put(None)
    
    def on_llm_error(self, error, **kwargs: Any) -> Any:
        self.queue.put(None)

chat = ChatOpenAI(streaming=True)

prompt = ChatPromptTemplate.from_messages([
    ("human", "{content}")
])

class StreamingChain(LLMChain):

    def stream(self, input):
        queue = Queue()
        handler = StreamingHandler(queue)

        def task():
            self(input, callbacks=[handler])

        Thread(target=task).start()

        while True:
            token = queue.get()
            if token is None:
                break
            yield token

chain = StreamingChain(llm=chat, prompt=prompt)

for output in chain.stream(input={'content': "Tell me a joke"}):
    print(output)