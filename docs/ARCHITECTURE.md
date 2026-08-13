# Architecture & Training Pipeline

This document walks through the full pipeline used to build and use the tokenizer, from raw text to a trained vocabulary to inference.

The cycle is: **Prepare Data** → **(Evaluate)** → **Train & Save Vocabulary** → **Load Vocabulary & Tokenize New Text**.

## Step 1: Data Loading and Preparation (`main.py`)

The process begins with a large corpus of text, which serves as the raw material for training. To handle this efficiently without loading the entire dataset into memory, the data is streamed.

1. **Streaming the Dataset**: `main.py` imports `ptbr_only_dataset` from `databaseload.py`. This object doesn't download the dataset; instead, it's configured with `streaming=True` to fetch data on the fly. This is crucial for working with large datasets that might not fit into RAM.
2. **On-the-Fly Aggregation**: The script iterates through the streaming dataset (up to a limit of 100,000 entries for a manageable training size) and concatenates text from the `instruction`, `input`, and `output` fields into a single, large string variable named `text`.
3. **Result**: At the end of this step, you have one large string containing a representative sample of the Portuguese language. This was assembled piece by piece, keeping memory usage low.

## Step 2: Evaluation — Optional, but Recommended (`evaluation.py`)

Before committing to a final vocabulary size, it's wise to evaluate the trade-offs. A larger vocabulary can represent text with fewer tokens but takes up more space and memory.

1. **Running the Evaluation**: The commented-out code in `main.py` shows how to use `evaluate_tokenizer` from `evaluation.py`. This function runs the training process multiple times, creating checkpoints at various merge counts (e.g., every 50 merges from 0 to 20,000).
2. **Measuring Efficiency**: For each checkpoint, it calculates the average number of tokens required to represent a single word. The goal is to find the "sweet spot" where adding more merges (and more vocabulary) yields diminishing returns in compression.
3. **Plotting the Results**: `plot_results` generates two plots:
   - **Average Tokens per Word vs. Number of Merges** — shows how well the tokenizer is compressing text. Ideally, this line goes down.
   - **Vocabulary Size vs. Number of Merges** — shows how large the vocabulary is growing.
4. **Choosing `num_merges`**: By looking at these plots, a developer can decide on a good final vocabulary size. In this project, `3500` was chosen as that sweet spot.

## Step 3: Training the Tokenizer (`tokenizer.py`)

Once the target number of merges is decided, the final tokenizer is trained. `train.py` is a cleaned-up version of `main.py` specifically for this purpose.

1. **Initial State**: The `train` method in the `PtbrTokenizer` class starts by creating a base vocabulary of all unique single characters present in the text. The text is then represented as a sequence of these character IDs.
2. **Iterative Merging**: The core of training is a loop that runs for `num_merges` (3500) iterations:
   - It finds the most frequently occurring adjacent pair of tokens (e.g., `('t', 'e')`).
   - It merges this pair into a new, single token (`'te'`).
   - It adds this new token to the vocabulary with a new ID.
   - It replaces all occurrences of the original pair in the text sequence with the new token's ID.
3. **Merge Rules**: The `is_merge_allowed` method provides custom logic that prevents merges across punctuation or newlines, ensuring meaningful units are preserved.
4. **Saving the Vocabulary**: After the loop completes, `train.py` saves the final vocabulary (the mapping of token strings to integer IDs) into `src/pt_tokenizer/data/vocab_pt_br_3500.json`. This JSON file **is** the trained tokenizer.

## Step 4: Using the Trained Tokenizer (`app.py` and `demo.py`)

With `vocab_pt_br_3500.json` created, the training phase is complete. The vocabulary can now be used to tokenize new, unseen text. This is demonstrated in two ways:

1. **Command-Line Demo (`demo.py`)**:
   - Loads the vocabulary from the JSON file.
   - Implements a "Longest Match" encoding algorithm: it iterates through the input text and, at each position, finds the longest possible substring that exists in the loaded vocabulary.
   - Prints a color-coded visualization of the tokenized text directly in the terminal.

2. **Web Application (`app.py`)**:
   - The main user-facing application. It does almost the exact same thing as `demo.py`, but in a user-friendly web interface built with Streamlit.
   - Loads the vocabulary (using `@st.cache_data` for efficiency).
   - Takes user input from a text area.
   - Runs the same "Longest Match" logic to break the text into pieces.
   - Generates and displays colorful HTML to visualize how the text was segmented, along with the total token count and the raw token IDs.