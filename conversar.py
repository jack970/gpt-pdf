from langchain.embeddings.openai    import OpenAIEmbeddings
from langchain.vectorstores         import Chroma
from langchain.chains               import ConversationalRetrievalChain
from langchain.chat_models          import ChatOpenAI
from langchain.prompts.chat         import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate
)
from langchain.schema   import ( AIMessage, HumanMessage, SystemMessage )

# Prompt padrao utilizado para enviar os conteudo so gpt
system_template="""Use the following pieces of context to playfully answer users' question. 
If you don't know the answer, just say that you don't know, don't try to make up an answer.
----------------
{context}"""
messages = [
    SystemMessagePromptTemplate.from_template(system_template),
    HumanMessagePromptTemplate.from_template("{question}")
]
prompt = ChatPromptTemplate.from_messages(messages)

def setup(collection_name, model_name, openai_api_key):
    persist_directory="./db/chroma/" + collection_name
    embeddings = OpenAIEmbeddings(openai_api_key=openai_api_key)

    # Carrega o banco de vetor Embeddings
    vectordb = Chroma(
        persist_directory=persist_directory, 
        collection_name=collection_name, 
        embedding_function=embeddings).as_retriever()
    
    llm = ChatOpenAI(
            temperature=0, 
            max_tokens=400,
            model_name=model_name, #"gpt-4" or "gpt-3.5-turbo"
            openai_api_key=openai_api_key
        )
    
    # Objeto de conversa que utiliza conteudo do vetor e o modelo openAI
    qa = ConversationalRetrievalChain.from_llm(
        llm, vectordb,qa_prompt=prompt
    )
    return qa

# Utilizacao do objeto de conversa podendo ou nao ter historico 
def chat(qa, texto, chat_history=[] ):
    result = qa({"question": texto, "chat_history": chat_history})
    return result["answer"]

