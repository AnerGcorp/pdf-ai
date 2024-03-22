from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.chains import LLMChain
from dotenv import load_dotenv

load_dotenv()

chat = ChatOpenAI(streaming=True)

prompt = ChatPromptTemplate.from_messages([
    ("human", "{content}")
])

chain = LLMChain(llm=chat, prompt=prompt)
for message in chain.stream(input={'content': "Tell me a joke"}):
    print(message)
# messages = prompt.format_messages(content="Tell me a joke")
# for message in chat.stream(messages):
#     print(message.content)