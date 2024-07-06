from langchain_text_splitters import CharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain_openai import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.chains.conversational_retrieval.base import ConversationalRetrievalChain


class AnswerGeneration:

    def get_text_chunks(self, text):
        splitter = CharacterTextSplitter(separator="\n", chunk_size=1200, chunk_overlap=200)
        text_chunks = splitter.split_text(text)
        return text_chunks


    def get_vector_store(self, text_chunks, openai_api_key):
        embeddings = OpenAIEmbeddings(api_key=openai_api_key)
        vector_store = FAISS.from_texts(texts = text_chunks, embedding = embeddings)
        return vector_store

    def get_conversation_chain(self, vectorstore, openai_api_key):
        llm = ChatOpenAI(temperature=0, api_key=openai_api_key)
        memory = ConversationBufferMemory(memory_key='chat_history', return_messages=True)
        conversation_chain = ConversationalRetrievalChain.from_llm(llm=llm, retriever=vectorstore.as_retriever(), memory=memory)
        return conversation_chain
    
    def get_answer(self, text, openai_api_key):
        chunks = self.get_text_chunks(text)
        vectorstore = self.get_vector_store(chunks, openai_api_key)
        conversation_chain = self.get_conversation_chain(vectorstore, openai_api_key)
        return conversation_chain