# Load model directly
from transformers import AutoTokenizer, AutoModelForCausalLM

tokenizer = AutoTokenizer.from_pretrained("allenai/OLMo-2-0425-1B-Instruct")
olmo = AutoModelForCausalLM.from_pretrained("allenai/OLMo-2-0425-1B-Instruct")


message = ["Language modeling is "]
inputs = tokenizer(message, return_tensors='pt', return_token_type_ids=False)
# optional verifying cuda
inputs = {k: v.to('cuda') for k,v in inputs.items()}
olmo = olmo.to('cuda')


response = olmo.generate(
            **inputs, 
            max_new_tokens=100, 
            do_sample=True, 
            top_k=50, 
            top_p=0.95)
print(tokenizer.batch_decode(response, skip_special_tokens=True)[0])
