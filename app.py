import streamlit as st
import json

# --- Page Config ---
st.set_page_config(page_title="Token Visualizer", page_icon="🔠")

# --- Load Data ---
@st.cache_data # This keeps the app fast by not reloading the file every time
def load_vocab():
    try:
        with open("src/pt_tokenizer/data/vocab_pt_br_3500.json", "r", encoding="utf-8") as file:
            vocab = json.load(file)
        reverse = {v: k for k, v in vocab.items()}
        max_len = max(len(k) for k in reverse)
        return reverse, max_len
    except FileNotFoundError:
        st.error("Vocab file not found! Please ensure 'src/pt_tokenizer/data/vocab_pt_br_3500.json' exists.")
        return None, 0

reverse_vocab, max_token_len = load_vocab()

# --- UI Layout ---
st.title("🔠 Portuguese Tokenizer Visualizer")
st.markdown("Enter text below to see how the 'Longest Match' algorithm breaks it down.")

input_text = st.text_area("Input Text", "Para miletar o jogo e conseguir a platina...", height=150)

if st.button("Tokenize ✨") and reverse_vocab:
    # --- Logic ---
    tokens = []
    pieces = []
    i = 0
    n = len(input_text)

    while i < n:
        found = False
        for j in range(min(max_token_len, n - i), 0, -1):
            piece = input_text[i:i+j]
            if piece in reverse_vocab:
                tokens.append(reverse_vocab[piece])
                pieces.append(piece)
                i += j
                found = True
                break
        
        if not found:
            # Handle unknown characters gracefully in UI
            pieces.append(input_text[i])
            tokens.append("UNK")
            i += 1

    # --- Visualization ---
    st.subheader("Token Preview")
    
    # Custom HTML styling for tokens
    colors = ["#ffadad", "#ffd6a5", "#fdffb6", "#caffbf", "#9bf6ff", "#a0c4ff", "#bdb2ff", "#ffc6ff"]
    
    html_output = '<div style="line-height: 2.5; font-size: 1.2rem;">'
    for idx, p in enumerate(pieces):
        color = colors[idx % len(colors)]
        # Replacing newlines with <br> for HTML display
        display_piece = p.replace("\n", "↵<br>")
        html_output += f'<span style="background-color: {color}; padding: 4px 6px; border-radius: 4px; margin: 2px; color: black; font-family: monospace;">{display_piece}</span>'
    html_output += '</div>'

    st.markdown(html_output, unsafe_allow_html=True)

    # --- Data Display ---
    with st.expander("View Raw Token IDs"):
        st.write(tokens)
    
    st.metric("Total Tokens", len(tokens))