# 🎉 LightRAG is Running!

## ✅ **Servers Status**

Both servers are now live and ready to use:

### **API Server** ✓
- **Address**: http://localhost:9621
- **Status**: Running on Uvicorn
- **API Docs**: http://localhost:9621/docs
- **Redoc**: http://localhost:9621/redoc
- **Process**: Uvicorn running on port 9621

### **Web UI (Development Server)** ✓
- **Address**: http://localhost:5173/webui/
- **Status**: Vite dev server running
- **Port**: 5173
- **Hot Reload**: Enabled (changes auto-reflect)

---

## 🌐 **Access Points**

| Service | URL | Purpose |
|---------|-----|---------|
| **Web UI** | http://localhost:5173/webui/ | Interactive RAG interface |
| **API** | http://localhost:9621 | RESTful API endpoint |
| **API Docs** | http://localhost:9621/docs | Swagger documentation |
| **API Redoc** | http://localhost:9621/redoc | ReDoc documentation |

---

## 📝 **Next Steps**

1. **Try the Web UI**: Open http://localhost:5173/webui/ in your browser
   - Upload documents
   - Build knowledge graphs
   - Query your documents
   - Visualize relationships

2. **Try the API**: Visit http://localhost:9621/docs for interactive API testing
   - Insert documents
   - Query RAG system
   - Retrieve entities and relations

---

## 🛠️ **Terminal Commands Reference**

### Stop servers:
```bash
# In the API server terminal: Press Ctrl+C
# In the Web UI terminal: Press Ctrl+C
```

### Restart servers:
```bash
# API Server
cd /Users/tylerconn/Documents/projects/lightRAG
source .venv/bin/activate
lightrag-server

# Web UI (in another terminal)
cd /Users/tylerconn/Documents/projects/lightRAG/lightrag_webui
/Users/tylerconn/.bun/bin/bun run dev
```

### Build production Web UI:
```bash
cd /Users/tylerconn/Documents/projects/lightRAG/lightrag_webui
/Users/tylerconn/.bun/bin/bun run build
```

### Run tests:
```bash
cd /Users/tylerconn/Documents/projects/lightRAG
source .venv/bin/activate
python -m pytest tests
```

### Lint Python code:
```bash
cd /Users/tylerconn/Documents/projects/lightRAG
source .venv/bin/activate
ruff check .
```

---

## 📊 **Configuration Details**

**LLM**: OpenAI GPT-4 Mini
**Embeddings**: OpenAI Text-Embedding-3-Small
**Storage**: Local JSON-based (no database needed)
**Cache**: Enabled for faster queries

View full config: `.env` file

---

## 🚀 **Ready to Go!**

Your LightRAG instance is fully operational. Start by visiting:
- **http://localhost:5173/webui/** (Web UI)
- **http://localhost:9621/docs** (API Documentation)

Happy RAG-ing! 🎉
