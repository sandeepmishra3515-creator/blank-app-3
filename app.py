import streamlit as st
import os

st.set_page_config(page_title="MishraAlgoBot", layout="centered")
st.title("MishraAlgoBot — Streamlit demo with OpenAI example")
st.write("This Streamlit app demonstrates optional OpenAI usage via st.secrets. Add OPENAI_API_KEY in Streamlit Cloud secrets to enable API calls.")

# Read OpenAI key from Streamlit secrets (preferred) or environment (fallback)
openai_key = None
try:
    # st.secrets is available on Streamlit Cloud; use .get to avoid KeyError
    openai_key = st.secrets.get("OPENAI_API_KEY") if hasattr(st, "secrets") else None
except Exception:
    openai_key = None

if not openai_key:
    # fallback to environment variable (useful for local testing)
    openai_key = os.environ.get("OPENAI_API_KEY")

if openai_key:
    st.success("OpenAI key found (will be used for API calls).")
else:
    st.info("No OpenAI key found. Add OPENAI_API_KEY in Streamlit Cloud Secrets or set it as an environment variable for local testing.")

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

# OpenAI chat example
st.header("OpenAI quick demo (optional)")
prompt = st.text_input("Prompt for OpenAI (e.g. 'Summarize this text')")
if st.button("Ask OpenAI"):
    if not openai_key:
        st.error("OPENAI_API_KEY is not set. Add it to Streamlit secrets or environment variables before using this feature.")
    elif not prompt.strip():
        st.warning("Please enter a prompt.")
    else:
        try:
            import openai
            openai.api_key = openai_key
            # Use ChatCompletion if supported; fall back to Completion
            response_text = None
            try:
                completion = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=[{"role": "user", "content": prompt}],
                    max_tokens=300,
                    temperature=0.7,
                )
                response_text = completion.choices[0].message.content.strip()
            except Exception:
                # fallback to text completion
                completion = openai.Completion.create(
                    engine="text-davinci-003",
                    prompt=prompt,
                    max_tokens=300,
                    temperature=0.7,
                )
                response_text = completion.choices[0].text.strip()

            st.subheader("OpenAI response")
            st.write(response_text)
        except Exception as e:
            st.error(f"Error calling OpenAI API: {e}")

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
