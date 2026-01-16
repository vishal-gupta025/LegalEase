from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from rag.simple_rag import build_vector_store, semantic_search
from dotenv import load_dotenv
load_dotenv()


# load LLM
llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0.2)


def ask_question(question, chat_history=""):
    """
    Main RAG function:
    - retrieve relevant sections
    - send to LLM
    - get final answer
    """

    # make sure vector store is built
    build_vector_store()

    # retrieve relevant documents
    docs = semantic_search(question, top_k=3)

    # combine context
    context = ""
    for doc in docs:
        context += doc.page_content + "\n\n"

    # prompt template
    prompt_template = """
        You are a legal assistant. Use the following legal context to answer the question.

        chat history:
        {chat_history}

        Context:
        {context}

        Question:
        {question}

        Answer in simple and clear language.
        """

    prompt = PromptTemplate(
        input_variables=["chat_history", "context", "question"],
        template=prompt_template
    )

    final_prompt = prompt.format(chat_history=chat_history, context=context, question=question)
    # get answer from LLM
    response = llm.predict(final_prompt)

    return response


def summarize_case():

    build_vector_store()

    docs = semantic_search("Summarize the case", top_k=5)

    context = ""
    for doc in docs:
        context += doc.page_content + "\n\n"
    
    prompt_template = """
        You are a legal assistant. Summarize the following case in simple language.
        Context:
        {context}

        Give a clear and short summary.
        """
    prompt = PromptTemplate(
        input_variables=["context"],
        template=prompt_template
    )

    final_prompt = prompt.format(context=context)

    response = llm.predict(final_prompt)
    return response

def build_argument(side="plaintiff"):

    build_vector_store()

    docs = semantic_search("arguments reasoning judgement", top_k=5)

    context = ""
    for doc in docs:
        context += doc.page_content + "\n\n"

    prompt_template = """
        Using the following legal context, build a strong legal argument for the {side}.
        Context:    
        {context}

        Structure:
        1. Background
        2. Legal points
        3. Reasoning
        4. Conclusion
        """
    prompt = PromptTemplate(
        input_variables=["context", "side"],
        template=prompt_template
    )

    final_prompt = prompt.format(context=context, side=side)

    response = llm.predict(final_prompt)
    return response

