# RAG 2.0 Search Engine

A two-stage Retrieval-Augmented Generation (RAG) search engine:

1. **Stage 1 — Retrieval:** FAISS similarity search over `all-MiniLM-L6-v2` embeddings.
2. **Stage 2 — Reranking:** Cross-encoder (`cross-encoder/ms-marco-MiniLM-L-6-v2`) reranks the retrieved candidates.
3. **Generation:** Gemini 2.5 Flash generates the final answer from the reranked context.
4. **UI:** Streamlit app (`app.py` → `ui.py`), which loads logic straight out of the notebooks via `notebook_executor.py`.

## Project structure

```
├── app.py                  # Streamlit entry point
├── ui.py                   # Streamlit UI
├── notebook_executor.py    # Executes notebook code cells and exposes their functions
├── Retrieval.ipynb         # Stage 1 + Stage 2 retrieval logic (used live by the app)
├── Gemini.ipynb            # Gemini Flash call (used live by the app)
├── Chunking.ipynb          # Semantic chunking of extracted PDF text (offline pipeline step)
├── Embedding.ipynb         # Builds the FAISS index from chunks (offline pipeline step)
├── text_extraction.ipynb   # Extracts text/tables/images from raw PDFs (offline pipeline step)
├── raw_data/                # Source PDFs
├── extracted/                # Text/tables/images/metadata extracted from PDFs
├── chunked/                   # Semantic chunks (.jsonl)
├── VectorDB/                  # faiss.index, texts.pkl, metadatas.pkl (used live by the app)
└── requirements.txt
```

## Setup

1. **Clone the repo and create a virtual environment**
   ```bash
   git clone <your-repo-url>
   cd RAG2.0
   python -m venv venv
   source venv/bin/activate      # Windows: venv\Scripts\activate
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set your API key**
   ```bash
   cp .env.example .env
   ```
   Then open `.env` and set:
   ```
   GEMINI_API_KEY=your_actual_key
   ```
   Get a key from [Google AI Studio](https://aistudio.google.com/apikey).

4. **Run the app**
   ```bash
   streamlit run app.py
   ```
   The app will open at `http://localhost:8501`.

## Rebuilding the pipeline from scratch (optional)

`VectorDB/` already ships with a prebuilt index, so the app works out of the box.
If you add new PDFs to `raw_data/` and want to rebuild the index, run the offline
notebooks in order from the project root:

1. `text_extraction.ipynb` — extract text/tables/images from `raw_data/`
2. `Chunking.ipynb` — semantic chunking → `chunked/`
3. `Embedding.ipynb` — build embeddings + FAISS index → `VectorDB/`

These notebooks resolve all paths relative to the project root (or `RAG_BASE_DIR`
in `.env` if you run them from elsewhere), so no machine-specific paths are needed.

## ⚠️ Important — rotate your Gemini API key

Your original notebook had a **live Gemini API key hardcoded in plain text**. I removed
it and switched the code to read `GEMINI_API_KEY` from the environment/`.env` file
instead. However, since that key was already embedded in the file, treat it as
**compromised**: revoke/regenerate it in [Google AI Studio](https://aistudio.google.com/apikey)
before or right after you push this repo, so the old key can't be used by anyone
who may have seen it.

## Deploying

- **Streamlit Community Cloud:** push this repo to GitHub, connect it at
  [share.streamlit.io](https://share.streamlit.io), set `app.py` as the entry point,
  and add `GEMINI_API_KEY` under the app's **Secrets**.
- **Any other host (Render, Railway, a VM, etc.):** install `requirements.txt` and
  run `streamlit run app.py`, making sure `GEMINI_API_KEY` is set as an environment
  variable on that host.
