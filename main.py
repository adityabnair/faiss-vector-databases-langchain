import os
from dotenv import load_dotenv
from langchain.document_loaders import PyPDFLoader    
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import FAISS #useful for performing local similarity search and provding context to the embeddings
from langchain.chains import RetrievalQA
from langchain.chat_models import ChatOpenAI

load_dotenv()

if __name__ == "__main__":
    print("Hi")

    pdf_path = r'D:\IDrive-Sync\vector-db-memory\SABRE I2CT Review Paper Final.pdf'
    loader = PyPDFLoader(file_path=pdf_path)
    document = loader.load()
    # print(documents)
    text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=30, separator="\n")
    docs = text_splitter.split_documents(documents = document)
    embeddings = OpenAIEmbeddings()
    vectorstore = FAISS.from_documents(docs, embeddings) #
    vectorstore.save_local("faiss_index") #usage of faiss_cpu package to save the index
    new_vectorstore = FAISS.load_local("faiss_index", embeddings) #loading the index

    qa = RetrievalQA.from_chain_type(
    llm=ChatOpenAI(temperature=1, model_name="gpt-3.5-turbo"),
    chain_type="stuff",
    retriever = new_vectorstore.as_retriever()
    ) 
    res = qa.run("Give me the gist of the review in three sentences")
    print(res)




