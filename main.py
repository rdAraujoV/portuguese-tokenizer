from src.pt_tokenizer.databaseload import ptbr_only_dataset
from src.pt_tokenizer.evaluation import evaluate_tokenizer, plot_results
from src.pt_tokenizer.tokenizer import PtbrTokenizer
import json

texts = []

for i, ex in enumerate(ptbr_only_dataset):
    if i > 100000:
        break
    texts.append(ex["instruction"])
    if ex.get("input"):
        texts.append(ex["input"])
    texts.append(ex["output"])

text = " ".join(texts)


# ------- RUN EVALUATION --------

#results = evaluate_tokenizer(
#    text,
#    merge_range=range(0, 20000, 50)
#)

#plot_results(results)

# ------- RUN TOKENIZER TRAINING ---------
num_merges = 3500
file_name = f"vocab_pt_br_{num_merges}.json"

tokenizer = PtbrTokenizer()
final_tokens, final_id_to_token, final_merges = tokenizer.train(text, num_merges)
with open(file_name, "w", encoding="utf-8") as file:
    json.dump(final_id_to_token, file, ensure_ascii=False, indent=4)
print(f"\nFinal tokenizer saved to {file_name}!")