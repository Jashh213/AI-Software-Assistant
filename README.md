# 🤖 AI Software Engineering Assistant

An AI-powered software engineering assistant that helps developers **understand, explore, and interact with software repositories** using **RAG, semantic search, LLM-based planning, and Model Context Protocol (MCP)**.

The assistant can answer questions about a repository, retrieve relevant code and documentation, explore files through MCP tools, and perform supported repository/GitHub operations through tool execution.

---

## 🚀 Features

* **Repository Understanding** — Ask questions about the current project or repository.
* **RAG-based Code Retrieval** — Retrieves relevant code and documentation using semantic search.
* **Content-Aware Chunking** — Uses different chunking strategies for Python, Markdown, and other text files.
* **Local Embeddings** — Generates embeddings locally using Sentence Transformers.
* **FAISS Vector Search** — Stores and retrieves repository embeddings efficiently.
* **LLM-based Planning** — Classifies user requests and decides whether they require:

  * General LLM response
  * Repository RAG
  * Tool execution
* **MCP Integration** — Uses Model Context Protocol to connect the assistant with external tools.
* **Filesystem MCP** — Allows the assistant to explore and read repository files.
* **GitHub MCP** — Provides GitHub-related repository and collaboration operations.
* **Tool Registry & Executor** — Dynamically discovers and executes available MCP tools.
* **Memory System** — Maintains project, working, conversational, and long-term memory components.
* **Streamlit UI** — Provides a simple conversational interface.

---

## 🏗️ Architecture

```text
                         ┌─────────────────────┐
                         │    Streamlit UI     │
                         └──────────┬──────────┘
                                    │
                                    ▼
                    ┌──────────────────────────┐
                    │ Software Engineering     │
                    │        Agent             │
                    └────────────┬─────────────┘
                                 │
                                 ▼
                       ┌──────────────────┐
                       │     Planner      │
                       │   LLM-powered    │
                       └────────┬─────────┘
                                │
              ┌─────────────────┼─────────────────┐
              │                 │                 │
              ▼                 ▼                 ▼
        ┌───────────┐     ┌───────────┐     ┌────────────┐
        │  GENERAL  │     │    RAG    │     │    TOOL    │
        └─────┬─────┘     └─────┬─────┘     └──────┬─────┘
              │                 │                  │
              ▼                 ▼                  ▼
           OpenRouter      FAISS + Local       MCP Runtime
                              Embeddings            │
                                                   │
                                      ┌────────────┴────────────┐
                                      ▼                         ▼
                              Filesystem MCP              GitHub MCP
```

---

## 🔄 How It Works

### 1. User Query

The user asks a question or requests an action through the Streamlit interface.

Example:

```text
Explain how authentication is implemented in this repository.
```

### 2. Planner

The planner uses an LLM to determine what type of request it is.

It routes the request to one of three paths:

```text
GENERAL → General programming / AI / technical questions

RAG     → Questions requiring understanding of the current repository

TOOL    → Requests that require executing an available tool
```

### 3. RAG Pipeline

For repository-related questions, the RAG pipeline:

```text
Repository Files
      ↓
Document Loader
      ↓
Content-Aware Chunking
      ↓
Local Embeddings
      ↓
FAISS Vector Store
      ↓
Semantic Retrieval
      ↓
Relevant Context
      ↓
LLM
      ↓
Answer
```

### 4. Tool Execution

For action-oriented requests, the planner selects an available MCP tool.

The tool registry discovers available tools and the executor handles their execution.

For example:

```text
User
 ↓
Planner
 ↓
TOOL route
 ↓
Tool Registry
 ↓
Tool Executor
 ↓
MCP Runtime
 ↓
GitHub / Filesystem MCP
 ↓
Result
```

---

## 🧠 RAG Pipeline

The project uses a repository indexing and retrieval pipeline.

### Document Loading

The loader reads supported repository files and extracts their contents and metadata.

### Content-Aware Chunking

Different file types use different chunking strategies.

#### Python

Python files are parsed using the AST and can be divided around logical structures such as:

* Classes
* Functions
* Async functions

Large logical sections are further divided when necessary.

#### Markdown

Markdown documents are divided around headings and sections.

#### Other Files

Other supported text files use a general chunking strategy with configurable chunk size and overlap.

Each chunk stores metadata such as:

```text
path
relative_path
filename
extension
language
chunk_id
chunk_type
hash
size
```

### Local Embeddings

Repository chunks are converted into vector representations using a local Sentence Transformer embedding model.

This avoids depending on a remote embedding API for repository indexing.

### FAISS

FAISS is used as the vector store for efficient similarity-based retrieval.

---

## 🔌 Model Context Protocol (MCP)

The assistant uses **Model Context Protocol (MCP)** to connect the application with external tools.

The application acts as an MCP client/runtime and connects to MCP servers.

### Filesystem MCP

Used for repository file operations such as:

* Reading files
* Searching files
* Listing directories
* Creating directories
* Writing files
* Editing files
* Moving files
* Getting file information

### GitHub MCP

Used for GitHub-related operations such as:

* Repository search
* Reading repository files
* Creating or updating files
* Creating branches
* Creating issues
* Creating pull requests
* Listing commits
* Managing issues and pull requests
* Searching code

The available tools are discovered dynamically when the MCP clients connect.

---

## 🧩 Project Structure

```text
AI Software Assistant/
│
├── app/
│   ├── agent/
│   │   └── software_engineering_agent.py
│   │
│   ├── config/
│   │   └── settings.py
│   │
│   ├── embeddings/
│   │   └── local_embedder.py
│   │
│   ├── llm/
│   │   ├── base.py
│   │   ├── factory.py
│   │   └── openrouter_llm.py
│   │
│   ├── mcp/
│   │   ├── client.py
│   │   ├── runtime.py
│   │   ├── filesystem.py
│   │   └── github.py
│   │
│   ├── memory/
│   │   ├── base_memory.py
│   │   ├── conversation_memory.py
│   │   ├── longterm_memory.py
│   │   ├── memory_manager.py
│   │   ├── project_memory.py
│   │   └── working_memory.py
│   │
│   ├── planner/
│   │   ├── planner.py
│   │   ├── planner_response.py
│   │   └── routes.py
│   │
│   ├── rag/
│   │   ├── chunker.py
│   │   ├── indexer.py
│   │   ├── loader.py
│   │   ├── rag_pipeline.py
│   │   ├── retriever.py
│   │   └── vector_store.py
│   │
│   ├── repository/
│   │   ├── git_manager.py
│   │   ├── project.py
│   │   └── repository_manager.py
│   │
│   ├── tools/
│   │   ├── executor.py
│   │   ├── registry.py
│   │   ├── tool.py
│   │   └── validator.py
│   │
│   └── ui/
│       ├── chat.py
│       ├── components.py
│       ├── sidebar.py
│       ├── state.py
│       └── styles.py
│
├── tests/
│
├── main.py
├── streamlit_app.py
├── requirements.txt
├── README.md
└── .gitignore
```

---

## 🛠️ Tech Stack

| Technology            | Purpose                    |
| --------------------- | -------------------------- |
| Python                | Core application           |
| Streamlit             | User interface             |
| OpenRouter            | LLM access                 |
| Sentence Transformers | Local embeddings           |
| FAISS                 | Vector similarity search   |
| MCP                   | Tool integration           |
| Filesystem MCP        | Repository/file operations |
| GitHub MCP            | GitHub operations          |
| Git                   | Repository management      |
| Pytest                | Testing                    |

---

## ⚙️ Setup

### 1. Clone the repository

```bash
git clone https://github.com/Jashh213/AI-Software-Assistant.git
cd AI-Software-Assistant
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

Activate it on Windows:

```bash
venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file in the project root.

```env
LLM_PROVIDER=openrouter
OPENROUTER_API_KEY=your_openrouter_api_key
GITHUB_TOKEN=your_github_token
```

Do **not** commit `.env` to GitHub.

The project already includes `.gitignore` rules to keep environment variables and generated runtime data out of version control.

---

## ▶️ Running the Application

Start the Streamlit application:

```bash
streamlit run streamlit_app.py
```

The application will start the Streamlit interface in your browser.

---

## 💬 Example Queries

### Repository Understanding

```text
Explain the architecture of this repository.
```

```text
Where is the RAG pipeline implemented?
```

```text
Explain how the planner works.
```

```text
How does the application connect to GitHub?
```

### Filesystem Operations

```text
Read app/rag/chunker.py
```

```text
Show the files inside the app/rag directory.
```

### GitHub Operations

```text
Create a new branch called testing-mcp.
```

```text
Create an issue describing a bug in the retrieval system.
```

The exact operations available depend on the connected MCP tools and their permissions.

---

## 🧪 Testing

The project contains tests for several components including:

```text
tests/
├── test_chunker.py
├── test_embedder.py
├── test_env.py
├── test_github_tools.py
├── test_indexer.py
└── test_loader.py
```

Run the test suite using:

```bash
pytest
```

---

## 🔐 Security

The following should remain local and must not be committed:

```text
.env
repositories/
storage/
__pycache__/
*.pyc
*.faiss
*.pkl
```

API keys and GitHub tokens should always be stored through environment variables.

---

## 🎯 Project Goals

This project was built to explore how modern AI software-engineering systems can combine:

* Large Language Models
* Retrieval-Augmented Generation
* Semantic search
* Vector databases
* Intelligent request planning
* Tool calling
* Model Context Protocol
* Repository management
* External developer tools

The goal is to move beyond a simple chatbot toward an assistant capable of **understanding software repositories and interacting with development tools**.

---

## 🔮 Future Improvements

Potential future improvements include:

* Hybrid lexical + semantic retrieval
* Retrieval reranking
* Query rewriting
* Parent-child document retrieval
* Improved code-aware retrieval
* More robust planner output validation
* Better repository-level context management
* Additional MCP integrations
* Improved automated evaluation of RAG responses
* More GitHub workflow automation

---

## 👩‍💻 Author

**Jasmitha Dhulipalla**

Computer Science & Engineering Graduate | AI & Software Engineering

GitHub: [Jashh213](https://github.com/Jashh213)
