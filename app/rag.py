from langchain_chroma import Chroma
from langchain_core.documents import Document as LCDocument
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama import ChatOllama, OllamaEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter


from app.store import DataStore

MAX_DISTANCE = 0.55
REFUSAL = "I don't have that in the documents."
COLLECTION = "hearthline_docs"

PROMPT = ChatPromptTemplate.from_template(
    """You are LineMate, a kitchen operations assistant for Hearthline restaurants.
Answer the question using ONLY the context below. If the context does not contain
the answer, say "I don't have that in the documents." Do not use outside knowledge.

Conversation so far:
{history}

Context:
{context}

Question: {question}"""
)


class RagService:
    def __init__(self, store: DataStore, persist_directory: str = "chroma_db"):
        self.store = store
        self.persist_directory = persist_directory
        self.embeddings = OllamaEmbeddings(model="nomic-embed-text")
        self.chain = PROMPT | ChatOllama(model="llama3.2", temperature=0) | StrOutputParser()
        self.vectorstore = None

    def index(self) -> int:
        """Chunk every document in the store and embed it into Chroma. Returns chunk count."""
        splitter = RecursiveCharacterTextSplitter(chunk_size=300, chunk_overlap=50)
        chunks = []
        for doc in self.store.list_documents():
            for piece in splitter.split_text(doc.body):
                chunks.append(LCDocument(
                    page_content=f"{doc.title}\n{piece}",
                    metadata={"document_id": doc.id, "title": doc.title, "category": doc.category.value},
                ))
        if not chunks:
            raise ValueError("No documents to index")

        # Rebuild from scratch so stale vectors from a previous run never linger
        old = Chroma(collection_name=COLLECTION, embedding_function=self.embeddings,
                     persist_directory=self.persist_directory)
        old.delete_collection()
        self.vectorstore = Chroma.from_documents(
            chunks, self.embeddings, collection_name=COLLECTION,
            persist_directory=self.persist_directory,
        )
        return len(chunks)

    def ask(self, question: str, conversation_id: str | None = None) -> dict:
        if self.vectorstore is None:
            raise RuntimeError("Call index() before ask()")
        if not question.strip():
            raise ValueError("Question must not be blank")

        history = self.store.get_conversation_history(conversation_id) if conversation_id else []
        history_text = "\n".join(f"Q: {t['question']}\nA: {t['answer']}" for t in history) or "None"

        search_query = f"{history_text}\n{question}" if history else question
        hits = self.vectorstore.similarity_search_with_score(search_query, k=4)
        relevant = [doc for doc, score in hits if score <= MAX_DISTANCE]
        if not relevant:
            result = {"answer": REFUSAL, "sources": []}
        else:
            context = "\n\n".join(d.page_content for d in relevant)
            answer = self.chain.invoke({"history": history_text, "context": context, "question": question})
            if REFUSAL.lower() in answer.lower():
                result = {"answer": REFUSAL, "sources": []}
            else:
                sources = {}
                for d in relevant:
                    sources.setdefault(d.metadata["document_id"], d.metadata["title"])
                result = {"answer": answer, "sources": [{"document_id": i, "title": t} for i, t in sources.items()]}

        if conversation_id:
            self.store.add_conversation_turn(conversation_id, question, result["answer"])
        return result