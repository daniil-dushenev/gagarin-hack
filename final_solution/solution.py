from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
from pickle import load
import pandas as pd
import ast
import copy
import typing as tp
import re


def get_id(r, cfg):
    r = preprocess_text(r).strip().split()
    dict_mine = cfg['dict_mine']
    l1 = set()
    l2 = set()

    # первый перебор
    for i in r:
        if i in dict_mine:
            l1.add(dict_mine[i])

    # второй перебор
    if len(r) == 0:
        return l1
    first = r[0]
    for i in range(1, len(r)):
        word = first + ' ' + r[i]
        first = r[i]
        if word in dict_mine:
            l2.add(dict_mine[word])

    l = l1.union(l2)
    return l


def replace_on_token(text, names_company):
    if type(names_company) == type('sf'):
        names_company = [names_company]
    for name in names_company:
        old_text = copy.copy(text)
        name = name.lower()
        text = text.replace(name, "[COMP]")
        text = text.replace(name.split()[0], "[COMP]")
    return text


def create_cfg(model_path, alias_path):
    tokenizer = AutoTokenizer.from_pretrained("./weights/tokenizer/", local_files_only=True)
    tokenizer.add_tokens(['[COMP]'])
    device = 'cuda' if torch.cuda.is_available() else 'cpu'
    model = torch.load(model_path, map_location=torch.device(device))
    synonyms = pd.read_csv('data/new_names_and_synonyms_i_already_letter_maybe.csv')
    dict_mine = {}
    for index, row in synonyms.iterrows():
        issuerid = row['issuerid']
        combined = [preprocess_text(i) for i in ast.literal_eval(row['combined'])]
        r = set(combined)
        for j in r:
            dict_mine[j] = issuerid
    with open(alias_path, 'rb') as f:
        alias_dict = load(f)
    need_utils = {
        'model': model,
        'tokenizer': tokenizer,
        'device': device,
        'alias_dict': alias_dict,
        'dict_mine':dict_mine
    }
    return need_utils


def add_spec_token(text, id_comp, dict_alias):
    post, name_company = text, dict_alias[id_comp]
    post = replace_on_token(post, name_company)
    return post


def inference_sample(text, id_company, cfg):
    alias_dict = cfg['alias_dict']
    text = add_spec_token(text, id_company, alias_dict)
    tokenizer = cfg['tokenizer']
    model = cfg['model']
    model.eval()
    device = cfg['device']
    tokenized_text = tokenizer(text, truncation=True, padding=True, max_length=512)
    data = torch.tensor(tokenized_text.input_ids).unsqueeze(0).to(device)
    att_mask = torch.tensor(tokenized_text.attention_mask).unsqueeze(0).to(device)

    output = model(data, attention_mask=att_mask)
    label = output.logits.squeeze().argmax(-1) + 1
    return float(label.item())


def preprocess_text(raw_code):
    processed_text = re.sub(r'#(\w+)', r'\1', raw_code)
    processed_text = re.sub(r'[^\w\s]', ' ', processed_text)
    processed_text = processed_text.lower()
    return processed_text



def score_texts(messeges, cfg):
    otv = []
    for text in list(messeges):
        idx_comp = get_id(text, cfg)
        text_otv = []
        for el in idx_comp:
            score = inference_sample(text, el, cfg)
            text_otv.append((el, score))
        otv.append(text_otv)
    return otv

