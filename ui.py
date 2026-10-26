import streamlit as st
from notebook_executor import load_notebook_functions


# --------------------------------------------------
# Load notebooks ONCE
# --------------------------------------------------
@st.cache_resource
def load_backends():
    retrieval_ns = load_notebook_functions("Retrieval.ipynb")
    gemini_ns = load_notebook_functions("Gemini.ipynb")

    return (
        retrieval_ns["stage1_retrieve"],
        retrieval_ns["stage2_rerank"],
        gemini_ns["call_gemini_flash"]
    )


stage1_retrieve, stage2_rerank, call_gemini_flash = load_backends()


def rag_2_0_search_engine():

    st.set_page_config(
        page_title="RAG 2.0 SEARCH ENGINE",
        layout="wide"
    )

    st.title("🔎 RAG 2.0 SEARCH ENGINE")
    st.write("Two-stage retrieval with FAISS + Cross-Encoder + Gemini Flash")

    # ---------------- Sidebar ----------------
    st.sidebar.header("⚙️ Retrieval Settings")

    faiss_k = st.sidebar.slider(
        "FAISS Top-K",
        min_value=5,
        max_value=30,
        value=20
    )

    final_k = st.sidebar.slider(
        "Reranked Top-K",
        min_value=1,
        max_value=10,
        value=5
    )

    # ---------------- Query Input ----------------
    query = st.text_area(
        "Enter your question",
        placeholder="Example: Explain MPC based soft start in EVs",
        height=120
    )

    if st.button("🔍 Search"):

        if not query.strip():
            st.warning("Please enter a valid query.")
            return

        # -------- Stage 1: FAISS Retrieval --------
        with st.spinner("🔍 Retrieving documents (FAISS)..."):
            stage1_results = stage1_retrieve(query, top_k=faiss_k)

        if not stage1_results:
            st.error("No relevant documents found.")
            return

        # -------- Stage 2: Reranking --------
        with st.spinner("📊 Reranking documents..."):
            stage2_results = stage2_rerank(
                query,
                stage1_results,
                top_k=final_k
            )

        # -------- Gemini Flash --------
        with st.spinner("🤖 Generating answer using Gemini Flash..."):
            answer = call_gemini_flash(query, stage2_results)

        # ---------------- Output ----------------
        st.subheader("✅ Answer")
        st.write(answer)

        st.subheader("📚 Sources")
        for i, r in enumerate(stage2_results, 1):
            meta = r["metadata"]
            st.markdown(
                f"{i}. **{meta['pdf_name']}**, page {meta['page']}"
            )
