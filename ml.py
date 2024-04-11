from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig
import torch
import accelerate
import bitsandbytes
import time

from transformers import MBartTokenizer, MBartForConditionalGeneration


def load_llm(model_name):
    bnb_config = BitsAndBytesConfig(
        load_in_4bit=True,
        bnb_4bit_use_double_quant=True,
        bnb_4bit_quant_type="nf4",
        bnb_4bit_compute_dtype=torch.bfloat16
    )

    model = AutoModelForCausalLM.from_pretrained(
        model_name,
        quantization_config=bnb_config,
        device_map="auto",
        trust_remote_code=True,
        # attn_implementation="flash_attention_2"
    )

    tokenizer = AutoTokenizer.from_pretrained(model_name, add_bos_token=True, trust_remote_code=True)

    return model, tokenizer


def generate_response_llm(model, tokenizer, prompt):
    prompt = f"GPT4 Correct User: {prompt}<|end_of_turn|>GPT4 Correct Assistant:"
    input_ids = tokenizer(prompt, return_tensors="pt").input_ids.to(device)
    outputs = model.generate(
        input_ids,
        max_length=2048,
        pad_token_id=tokenizer.pad_token_id,
        eos_token_id=tokenizer.eos_token_id,
    )
    response_ids = outputs[0]
    response_text = tokenizer.decode(response_ids, skip_special_tokens=True)

    # Удаляем промпт из ответа
    prompt_index = response_text.find("GPT4 Correct Assistant:")
    if prompt_index != -1:
        response_text = response_text[prompt_index + len("GPT4 Correct Assistant:"):]

    return response_text


def load_bart():
    model_name = "IlyaGusev/mbart_ru_sum_gazeta"
    tokenizer = MBartTokenizer.from_pretrained(model_name)
    model = MBartForConditionalGeneration.from_pretrained(model_name)
    return model, tokenizer


def generate_response_bart(model, tokenizer, prompt, device='cpu'):
    input_ids = tokenizer(
        [prompt],
        max_length=600,
        truncation=True,
        return_tensors="pt",
    )["input_ids"].to(device)

    output_ids = model.generate(
        input_ids=input_ids,
        no_repeat_ngram_size=4
    )[0]

    summary = tokenizer.decode(output_ids, skip_special_tokens=True)
    return summary