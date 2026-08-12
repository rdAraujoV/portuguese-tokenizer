import os
from datasets import load_dataset
from dotenv import load_dotenv

load_dotenv()
hf_token = os.getenv("HF_TOKEN")

os.environ["HF_TOKEN"]= hf_token

ptbr_only_dataset = load_dataset("dominguesm/Canarim-Instruct-PTBR-Dataset", streaming=True, split='train', token=hf_token)