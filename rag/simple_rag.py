from cases.models import CaseSection
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS  
from langchain_core.documents import Document

# load embedding model
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

# global variable
vector_store = None


def build_vector_store():
    """
    Reads CaseSection from DB and builds FAISS vector store.
    """
    global vector_store

    sections = CaseSection.objects.all()

    if not sections.exists():
        print("No CaseSection found in database.")
        return

    documents = []

    for section in sections:
        doc = Document(
            page_content=section.content,
            metadata={
                "id": section.id,
                "section_type": section.section_type
            }
        )
        documents.append(doc)

    vector_store = FAISS.from_documents(documents, embeddings)

    print(f"FAISS vector store built with {len(documents)} sections.")


def semantic_search(query, top_k=3):
    """
    Perform semantic search using FAISS.
    """
    global vector_store

    if vector_store is None:
        raise Exception("Vector store not built. Call build_vector_store() first.")

    results = vector_store.similarity_search(query, k=top_k)

    return results
