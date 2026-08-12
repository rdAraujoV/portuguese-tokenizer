from src.pt_tokenizer.tokenizer import train_tokenizer
import matplotlib.pyplot as plt

def evaluate_tokenizer(text, merge_range):

    history = train_tokenizer(
        text,
        num_merges=max(merge_range),
        checkpoints=set(merge_range)
    )

    words = text.split()
    word_count = len(words)

    results = []

    for m, token_count, vocab_size in history:

        avg = token_count / word_count

        results.append((m, avg, vocab_size))
    return results

def plot_results(results):
    merges = [r[0] for r in results]
    avg_tokens_per_word = [r[1] for r in results]
    vocab_sizes = [r[2] for r in results]

    plt.figure(figsize=(12, 6))

    plt.subplot(1, 2, 1)
    plt.plot(merges, avg_tokens_per_word, marker='o')
    plt.title('Average Tokens per Word vs. Number of Merges')
    plt.xlabel('Number of Merges')
    plt.ylabel('Average Tokens per Word')
    plt.grid(True)

    plt.subplot(1, 2, 2)
    plt.plot(merges, vocab_sizes, marker='o', color='red')
    plt.title('Vocabulary Size vs. Number of Merges')
    plt.xlabel('Number of Merges')
    plt.ylabel('Vocabulary Size')
    plt.grid(True)

    plt.tight_layout()
    plt.show()