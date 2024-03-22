from typing import Any
from uuid import UUID
from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.chains import LLMChain
from langchain.callbacks.base import BaseCallbackHandler
from dotenv import load_dotenv

load_dotenv()

class StreamingHandler(BaseCallbackHandler):
    def on_llm_new_token(self, token: str, **kwargs: Any) -> Any:
        print(token)

chat = ChatOpenAI(
    streaming=True,
    callbacks=[StreamingHandler()]
)

prompt = ChatPromptTemplate.from_messages([
    ("human", "{content}")
])

chain = LLMChain(llm=chat, prompt=prompt)
for message in chain.stream(input={'content': "Tell me a joke"}):
    print(message)
# messages = prompt.format_messages(content="Tell me a joke")
# for message in chat.stream(messages):
#     print(message.content)