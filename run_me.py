import json
import pathlib
import typing as tp
import time

import final_solution


PATH_TO_TEST_DATA = pathlib.Path("data") / "test_texts.json"
PATH_TO_OUTPUT_DATA = pathlib.Path("results") / "output_scores.json"


def load_data(path: pathlib.PosixPath = PATH_TO_TEST_DATA) -> tp.List[str]:
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    return data


def save_data(data, path: pathlib.PosixPath = PATH_TO_OUTPUT_DATA):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=1, ensure_ascii=False)


def main():
    model_path = 'weights/best_model_0_6734842951059167.pth'
    alias_path = 'data/alias_dict.pickle'
    synonyms_path = 'data/new_names_and_synonyms_i_already_letter_maybe.csv'
    cfg = final_solution.solution.create_cfg(model_path, alias_path, synonyms_path)

    texts = load_data()
    scores = final_solution.solution.score_texts(texts, cfg)
    save_data(scores)


if __name__ == '__main__':
    main()
