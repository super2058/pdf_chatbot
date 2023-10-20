from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import pinecone
from langchain.vectorstores import Pinecone
import os
import openai
from langchain.document_loaders import PyMuPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import SentenceTransformerEmbeddings
from dotenv import load_dotenv
import csv

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
load_dotenv()

pinecone_api_key = os.getenv("PINECONE_API_KEY")
openai_key = os.getenv("OPENAI_API_KEY")
openai.api_key = os.getenv("OPENAI_API_KEY")
pinecone_env = os.getenv("PINECONE_ENV")
index_name = os.getenv("PINECONE_INDEX_NAME")

loader = PyMuPDFLoader('dataset.pdf')
documents = loader.load()

# Open the CSV file for reading
# with open(csv_file_path, 'r', newline='') as csv_file:
#     csv_reader = csv.reader(csv_file)

#     # Initialize a list to store the rows from the CSV file
#     documents = []

#     for row in csv_reader:
#         documents.append(row)
# print(documents)
text_spliter = RecursiveCharacterTextSplitter(chunk_size=512, chunk_overlap=10)
texts = text_spliter.split_documents(documents)

embeddings = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")

pinecone.init(
    api_key=pinecone_api_key,  # find at app.pinecone.io
    environment=pinecone_env  # next to api key in console
)

index = Pinecone.from_documents(texts, embeddings, index_name=index_name)


@app.post("/chat/")
async def chat(reqeust: Request):
    body = await reqeust.json()
    query = body['query']
    try:
        llm_res = get_answer(query)
        return {"message": llm_res}
    except Exception as err:
        return ('Exception occurred. Please try again', str(err))


def get_similiar_docs(query, k=1, score=False):
    if score:
        similar_docs = index.similarity_search_with_score(query, k=k)
    else:
        similar_docs = index.similarity_search(query, k=k)
    return similar_docs


def generate_text(openAI_key, prompt, engine="text-davinci-003"):
    openai.api_key = openAI_key
    completions = openai.Completion.create(
        engine=engine,
        prompt=prompt,
        max_tokens=512,
        n=1,
        stop=None,
        temperature=0.1,
        seed=123,
        # stream=True,
    )
    return completions["choices"][0]["text"]


def get_answer(query):
    res = get_similiar_docs(query, k=1, score=False)
    page_content = res[0].page_content

    prompt = f"""
                You are a chatbot to assist users with your knowledge. You need to give detailed answer about various user queries.
                You have to use User's language, so for example, if the user asks you something in Dutch, you need to answer in Dutch.
                You are only a language model, so don't pretend to be a human.
                Use the next Context to generate answer about user query. If the Context has no relation to user query, you need to generate answer based on the knowledge that you know.
                And don't mention about the given Context. It is just a reference.
                Context: {page_content}
                query: {query}
    """
    ans = generate_text(openai_key, prompt)
    parts = ans.split(":")
    result = parts[1].strip()
    print("result ", result)
    return result
