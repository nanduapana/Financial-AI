from huggingface_hub import login
from transformers import AutoModelForCausalLM, AutoTokenizer

# Hard-coded Hugging Face token (replace this with your actual token)
huggingface_token = "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"

# Perform login with the token and add it to git credentials
login(token=huggingface_token, add_to_git_credential=True)

# Model name for the gated model
model_name = "meta-llama/Llama-2-7b-hf"

# Load the tokenizer and model using the token (replacing deprecated use_auth_token with token)
tokenizer = AutoTokenizer.from_pretrained(model_name, token=huggingface_token)
model = AutoModelForCausalLM.from_pretrained(model_name, token=huggingface_token)

# Example usage: Generate a response
input_text = "What is the future of artificial intelligence?"
input_ids = tokenizer(input_text, return_tensors="pt").input_ids
output = model.generate(input_ids)

# Decode the output and print the result
generated_text = tokenizer.decode(output[0], skip_special_tokens=True)
print(generated_text)

