import sys
sys.path.append('../../../') # Adjust path to run script from its directory
from src.pt_tokenizer.databaseload import ptbr_only_dataset
from src.pt_tokenizer.evaluation import evaluate_tokenizer, plot_results
from src.pt_tokenizer.tokenizer import train_tokenizer
import json

texts = []
# ------- RUN TOKENIZER TRAINING ---------
num_merges = 3500
file_name = f"vocab_pt_br_{num_merges}.json"
output_path = f"../data/{file_name}"

final_tokens, final_id_to_token, final_merges = train_tokenizer(text, num_merges)
with open(output_path, "w", encoding="utf-8") as file:
    json.dump(final_id_to_token, file, ensure_ascii=False, indent=4)
print(f"\nFinal tokenizer saved to {output_path}!")