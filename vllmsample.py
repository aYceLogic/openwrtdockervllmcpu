import os
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

def test_smollm2_gguf_cpu_fixed():
    # 1. Define Repositories
    original_hf_repo = "HuggingFaceTB/SmolLM2-135M-Instruct"

    # 2. Performance Environment Variable Configuration for CPU
    os.environ["VLLM_CPU_KVCACHE_SPACE"] = os.getenv("VLLM_CPU_KVCACHE_SPACE", "0")
    os.environ["VLLM_WORKER_MULTIPROC_METHOD"] = "spawn"

    print("\nLoading tokenizer and model...")
    tokenizer = AutoTokenizer.from_pretrained(original_hf_repo)
    model = AutoModelForCausalLM.from_pretrained(
        original_hf_repo, 
        torch_dtype=torch.float16,
        low_cpu_mem_usage=True
    ).to("cpu")

    # 5. Define Conversation Prompts
    conversation = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "List three fun facts about space."}
    ]

    # Apply chat template
    prompt = tokenizer.apply_chat_template(conversation, tokenize=False, add_generation_prompt=True)
    inputs = tokenizer(prompt, return_tensors="pt").to("cpu")

    print("\nGenerating response...")
    with torch.no_grad():
        outputs = model.generate(
            **inputs,
            max_new_tokens=150,
            temperature=0.7,
            top_p=0.9,
            do_sample=True
        )

    # Decode and print output
    response = tokenizer.decode(outputs[0][inputs.input_ids.shape[1]:], skip_special_tokens=True)
    print("\n--- Model Response ---")
    print(response)
    print("----------------------")

if __name__ == "__main__":
    test_smollm2_gguf_cpu_fixed()

