#!/usr/bin/env python

import os
from dotenv import load_dotenv
from llama_cloud_services import LlamaParse
from typing_extensions import List, TypedDict

from langchain import hub
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import DirectoryLoader
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_core.documents import Document

from langchain_openai import OpenAIEmbeddings
from langchain.chat_models import init_chat_model

from langgraph.graph import START, StateGraph

load_dotenv()

embeddings = OpenAIEmbeddings(model = 'text-embedding-3-large')
vector_store = InMemoryVectorStore(embeddings)

llm = init_chat_model('gpt-4o', model_provider = 'openai')
prompt = hub.pull('rlm/rag-prompt')

def parse_documents(docs):
    parser = LlamaParse(
        api_key = "llx-J6g57bwTZau91dkpAKDUCpBh1tfthFw4XDbSnxmUal0MuBhc",
        result_type = "markdown",
        verbose = True,
        language = "en",
        num_workers = 10
    )
    
    for doc in docs:
        result = parser.parse(doc)
        markdown_documents = result.get_markdown_documents(split_by_page = False)

        file_name = os.path.basename(doc)
        name = os.path.splitext(file_name)[0]

        with open(f'data/{name}.md', 'w', encoding = 'utf-8') as md_result:
            md_result.write(markdown_documents[0].text)


def split_text():
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size = 1000,
        chunk_overlap = 200,
        add_start_index = True
    )

    loader = DirectoryLoader('data', glob = '*.md')
    documents = loader.load()

    chunks = text_splitter.split_documents(documents)
    return chunks


class State(TypedDict):
    question: str
    context: List[Document]
    answer: str


def retrieve(state: State):
    retrieved_docs = vector_store.similarity_search(state['question'])
    return {'context': retrieved_docs}


def generate(state: State):
    docs_content = "\n\n".join(doc.page_content for doc in state['context'])
    messages = prompt.invoke({'question': state['question'], 'context': docs_content})
    response = llm.invoke(messages)
    return {'answer': response.content}


def main():
    documents = [ '../files/partial_orders.pdf' ]

    parse_documents(documents)
    chunks = split_text()
    doc_ids = vector_store.add_documents(documents = chunks)

    graph_builder = StateGraph(State).add_sequence([retrieve, generate])
    graph_builder.add_edge(START, "retrieve"),
    graph = graph_builder.compile()

    while True:
        query = input('\n\nEnter your question > ')
        result = graph.invoke({'question': query})
        print(f"Context: {result['context']}\n\n")
        print(f"Answer: {result['answer']}")

if __name__ == '__main__':
    main()