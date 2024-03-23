import os
from langfuse.client import Langfuse

langfuse = Langfuse(
    os.environ["LANGFUSE_PUBLIC_KEY"],
    os.environ["LANGFUSE_SECRET_KEY"],
    host="https://prod-upload-langchain.fly.dev"
)