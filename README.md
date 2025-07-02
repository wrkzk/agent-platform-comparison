
<p float="left">
  <img src="https://raw.githubusercontent.com/langchain-ai/langchain/master/docs/static/img/logo-light.svg" width="300">
  &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
  <img src="https://raw.githubusercontent.com/langroid/langroid/main/docs/assets/langroid-card-lambda-ossem-rust-1200-630.png" width="150">
  &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
  <img src="https://raw.githubusercontent.com/SmythOS/smyth-docs/refs/heads/main/static/img/smythos-500px.png" width="75">
</p>

# AI Agent Platform Comparison
In this repo, I compare three different agent builder libraries to assess their relative advantages and disadvantages. The three libraries that I decided to compare are LangChain, Langroid, and the SmythOS SDK. To carry out this comparison, I completed the same task in all three platforms: building a very simple agent that uses RAG to respond to user queries based on a given document.

## Overview
[LangChain](https://www.langchain.com/) is the established dominant platform for agentic AI. While it covers many use cases and has a very feature rich set of tools and integrations, many users are dissatisfied with the perceived bloat and complexity that comes with using LangChain. [Langroid](https://langroid.github.io/langroid/), another platform for agentic AI, seeks to solve this issue, but creating a more streamlined developer experience. Finally, [SmythOS](https://github.com/SmythOS/sre) is a relative newcomer to the field of agentic AI, having recently open-sourced their SDK and SRE. SmythOS claims to build upon OS kernel architecture, treating AI agents like OS processes.

## Comparison
|                      | LangChain  | Langroid | SmythOS    |
|----------------------|------------|----------|------------|
| RAG Support          | Yes        | Yes      | Yes        |
| License              | Apache 2.0 | MIT      | MIT        |
| Language             | Python or Javascript | Python | JavaScript |
| Local LLM Support    | [Yes](https://python.langchain.com/docs/how_to/local_llms/) - Ollama, Llama.cpp, GPT4All, llamafile | [Yes](https://langroid.github.io/langroid/tutorials/local-llm-setup/) - Ollama, LMStudio, llama.cpp, vLLM | Planned |
| Supported LLM Providers | [Numerous](https://python.langchain.com/docs/integrations/llms/) | Primarily via OpenAI API, although can use `litellm` to interface with many others | Via OpenAI API |
| Supported Vector DBs | [Numerous](https://python.langchain.com/docs/integrations/vectorstores/) | Qdrant, Chroma, LanceDB | Milvus, Pinecone, in-RAM |
| Documentation | Comprehensive, see [here](https://python.langchain.com/docs/introduction/) | Minimal but complete, see [here](https://langroid.github.io/langroid/quick-start/) | Somewhat lacking |
| Ease of Setup | More involved | Very simple | Relatively simple

## Dependencies and Hardware Requirements
To run `langchain_agent`, ensure that the following dependencies are installed via `pip`, or your operating system package manager:
- `llama-cloud-services`
- `langchain-text-splitters`
- `langchain-community`
- `langgraph`
- `langchain[openai]`
- `langchain-openai`
- `langchain-core`

To run `langroid_agent`, ensure that `langroid[doc-chat,db]` is installed via `pip` or another package manager.

Finally, to run `smythos_agent`, install the SDK with `npm i -g @smythos/sdk`.

In terms of hardware requirements, these agent platforms can run on a wide variety of hardware, assuming that they are relying on API calls to interface with the LLMs and embeddings models. Running local language and embedding models require significantly more powerful hardware. For example, to run larger language open source models such as `qwen3-30b` or `gemma-27b`, which would provide the highest accuracy, you would need a dedicated GPU with 24+ GB of VRAM. Powerful open source embedding models such as `qwen3-embedding-8B` require less system resources, although a powerful GPU is still necessary to vectorize text quickly.

## Conclusion
LangChain overwhelmingly has the most complete documentation, and seems to be the most feature rich platform to develop AI agents on among these three libraries. It supports the most LLMs, both local and through a remote provider, and it supports a multitude of vector database providers. Additionally, it takes a slightly less abstracted approach. In the examples in this repository, this meant manually configuring the retrieval and generations steps of the RAG pipline. However, both Langroid and SmythOS take a much more streamlined, organized, and higher-level approach, making development simpler. They come with preconfigured chat agents, which reduces the need to manually configure the details of an agent. A downside of this is that the support fewer features and are less configurable. If running a llm locally is a requirement, through somthing like Ollama, then either Langroid or LangChain are currently the better two options, as SmythOS currently does not support this.
