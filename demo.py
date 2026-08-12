import json

with open("src/pt_tokenizer/data/vocab_pt_br_3500.json", "r", encoding="utf-8") as file:
    vocab = json.load(file)

text = "Amanhã, talvez, o relógio comerá três nuvens roxas."

reverse = {v: k for k, v in vocab.items()}
max_len = max(len(k) for k in reverse)

tokens = []
pieces = []

i = 0
n = len(text)

# encode
while i < n:
    found = False
    
    for j in range(min(max_len, n - i), 0, -1):
        piece = text[i:i+j]
        
        if piece in reverse:
            tokens.append(reverse[piece])
            pieces.append(piece)
            i += j
            found = True
            break
    
    if not found:
        raise ValueError(f"Unknown token at position {i}")

colors = [
    "\033[101m",  # bright red background
    "\033[102m",  # bright green background
    "\033[103m",  # bright yellow background
    "\033[104m",  # bright blue background
    "\033[105m",  # bright magenta background
    "\033[106m",  # bright cyan background
]

reset = "\033[0m"


colored_text = ""

for i, p in enumerate(pieces):
    color = colors[i % len(colors)]
    colored_text += color + p + reset

print("\nOriginal:")
print(text)

print("\nToken preview:")
print(colored_text)

print("\nTokens:")
print(tokens)