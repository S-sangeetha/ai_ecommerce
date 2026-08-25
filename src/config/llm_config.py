import os
from langchain_google_genai import ChatGoogleGenerativeAI ,GoogleGenerativeAIEmbeddings
from dotenv import load_dotenv
from google import genai
load_dotenv()


class LlmEmbedding:
        def __init__(self):
            self.client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

            self.llm = ChatGoogleGenerativeAI(
                model="gemini-3.6-flash",
                temperature=0
            )

            

            self.embeddings_model = GoogleGenerativeAIEmbeddings(
                model="gemini-embedding-001",
                google_api_key=os.getenv("GOOGLE_API_KEY"),
                output_dimensionality=768
            )

        async def create_embeddings(self,text:str) -> list[float]:
                  embeddings = await self.embeddings_model.aembed_query(text)
                  return embeddings


llm_embedding  = LlmEmbedding()