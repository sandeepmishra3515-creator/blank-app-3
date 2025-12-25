import streamlit as st

st.set_page_config(page_title="MishraAlgoBot", layout="centered")

st.title("MishraAlgoBot — Streamlit demo")
st.write("This is a minimal working Streamlit app. It runs with only the 'streamlit' package.")

# Show info about Streamlit secrets (optional)
openai_key = None
try:
    openai_key = st.secrets.get("OPENAI_API_KEY") if hasattr(st, "secrets") else None
except Exception:
    openai_key = None

if openai_key:
    st.success("OpenAI key found in Streamlit secrets.")
else:
    st.info("No OpenAI key found. To enable API features, add OPENAI_API_KEY to Streamlit secrets.")

# Simple text processing demo
text = st.text_area("Enter text to process", height=150)
col1, col2 = st.columns(2)
with col1:
    if st.button("Word count"):
        words = len(text.split()) if text.strip() else 0
        st.write(f"Word count: {words}")
with col2:
    if st.button("Character count"):
        chars = len(text)
        st.write(f"Character count: {chars}")

st.markdown("---")

# File uploader example
uploaded = st.file_uploader("Upload a file (optional)")
if uploaded is not None:
    st.write("Uploaded file:", uploaded.name)
    try:
        content = uploaded.getvalue()
        # show first 1000 bytes/characters
        if isinstance(content, (bytes, bytearray)):
            preview = content[:1000]
            st.write(preview)
        else:
            st.write(str(content)[:1000])
    except Exception as e:
        st.write("Could not preview file:\", e)

# Small helper: show runtime info
st.sidebar.header("Info")
st.sidebar.write("Streamlit version:", st.__version__)
