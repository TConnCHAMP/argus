# ARGUS

**Personal Knowledge & Memory Assistant**

ARGUS is a RAG-powered knowledge management system that helps you organize, query, and connect information from your personal documents. Built on [LightRAG](https://github.com/HKUDS/LightRAG), it adds features tailored for personal knowledge management.

## Features

- **Knowledge Graph Visualization** - See how your documents and concepts connect
- **Conversational Threads** - Ask follow-up questions with context retained
- **Date-Aware Queries** - Ask questions like "what's on my schedule this week?"
- **Duplicate Detection** - Identify redundant content across documents
- **Multi-Format Support** - PDF, DOCX, TXT, and more

## Quick Start

### Prerequisites

- Python 3.10+
- [Bun](https://bun.sh/) (for web UI development)
- OpenAI API key (or compatible LLM provider)

### Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/argus.git
cd argus

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -e '.[api]'

# Copy and configure environment
cp .env.example .env
# Edit .env with your API keys
```

### Running ARGUS

```bash
# Start the server
source .venv/bin/activate
lightrag-server
```

Access the web UI at **http://localhost:9621**

### Configuration

Key settings in `.env`:

| Variable | Description | Default |
|----------|-------------|---------|
| `LLM_BINDING_API_KEY` | Your LLM API key | - |
| `LLM_MODEL` | Model to use | `gpt-4o-mini` |
| `EMBEDDING_BINDING_API_KEY` | Embedding API key | - |
| `WEBUI_TITLE` | UI title | `ARGUS` |

## Usage

1. **Upload Documents** - Drag and drop files or use the upload button
2. **Wait for Processing** - Documents are chunked and indexed into the knowledge graph
3. **Query** - Ask questions in natural language
4. **Explore** - Visualize the knowledge graph to discover connections

## Roadmap

- [ ] Slack integration
- [ ] Email integration
- [ ] Calendar sync
- [ ] Mobile companion app
- [ ] Multi-user support

## Project Structure

```
argus/
├── lightrag/           # Core RAG engine
│   ├── api/            # REST API server
│   └── kg/             # Knowledge graph storage
├── lightrag_webui/     # React web interface
├── rag_storage/        # Local data storage
└── inputs/             # Document upload directory
```

## Built On

ARGUS is built on [LightRAG](https://github.com/HKUDS/LightRAG) by HKUDS. For detailed information about the underlying RAG architecture, see the [LightRAG documentation](https://github.com/HKUDS/LightRAG).

## License

MIT License - See [LICENSE](LICENSE) for details.
