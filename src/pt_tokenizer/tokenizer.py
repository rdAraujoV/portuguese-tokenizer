import string
import unicodedata
import re

class PtbrTokenizer:
    def __init__(self):
        self.letters_with_accent = "áàâãéêíóôõúüçÁÀÂÃÉÊÍÓÔÕÚÜÇ"
        self.essential_chars = (
            string.ascii_letters + 
            string.digits + 
            string.punctuation + 
            self.letters_with_accent +
            " " + "\n"
        )
    
    def cleaning_text(self, text):
        return "".join(
            char for char in text
            if char in self.essential_chars
        )
    
    def pre_tokenize(self, clean_text):
        pattern = r" ?[A-Za-zÀ-ÿ]+| ?\d+| ?[^\w\s]"
        return re.findall(pattern, clean_text)
    
    def get_stats(self, ids):
        counts = {}
        for pair in zip(ids, ids[1:]):
            counts[pair] = counts.get(pair,0) +1
        return counts

    def is_punctuation(self, token):
        return all(unicodedata.category(c).startswith("P") for c in token)

    def is_merge_allowed(self, pair, id_to_token):
        a, b = pair
        token_a = id_to_token[a]
        token_b = id_to_token[b]

        # Disallow merging across punctuation boundaries
        if any(ch in string.punctuation for ch in token_a) or any(ch in string.punctuation for ch in token_b):
            return False

        # Disallow merging across newlines
        if '\n' in token_a or '\n' in token_b:
            return False

        # Disallow merging if the second token ends with a space (prevents merging into trailing spaces)
        if token_b.endswith(" "):
            return False

        # Disallow merging if the second token starts with a space (prevents merging leading spaces)
        if token_b.startswith(" "):
            return False

        return True

    def merge_pair(self, ids, pair, new_id):
        new_ids = []
        i = 0
        while i < len(ids):
            if i < len(ids) - 1 and (ids[i], ids[i+1]) == pair:
                new_ids.append(new_id)
                i += 2
            else:
                new_ids.append(ids[i])
                i += 1
        return new_ids
   
    def train(self, text, num_merges, checkpoints=None):

        if checkpoints is None:
            checkpoints = set()

        history = []

        # ----- preprocessing -----
        text = self.cleaning_text(text)
        text = " ".join(text.split())
        text = " " + text

        pieces = self.pre_tokenize(text)
        text = "".join(pieces)

        chars = sorted(list(set(text)))
        vocab = {i: ch for i, ch in enumerate(chars)}

        reverse = {v: k for k, v in vocab.items()}
        tokens = [reverse[ch] for ch in text]

        merges = {}

        # ----- merge loop -----
        for i in range(num_merges):

            if i % 10 == 0:
                print(f"\rMerge {i}/{num_merges}", end="")

            stats = self.get_stats(tokens)

            stats = {
                pair: c
                for pair, c in stats.items()
                if self.is_merge_allowed(pair, vocab)
            }

            if not stats:
                break

            top_pair = max(stats, key=stats.get)

            next_id = len(vocab)

            a, b = top_pair

            vocab[self.new_id] = vocab[a] + vocab[b]
            merges[top_pair] = self.new_id

            tokens = self.merge_pair(tokens, top_pair, self.new_id)

            # log checkpoint
            if i in checkpoints:
                history.append(
                    (i, len(tokens), len(vocab))
                )

        if checkpoints:
            return history
        
        print("\rMerge done.")
        
        return tokens, vocab, merges