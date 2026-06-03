import json
import os


def load_prompts_from_folder(folder_path="prompts"):
    prompts = []

    for file_name in os.listdir(folder_path):
        if file_name.endswith(".json"):
            file_path = os.path.join(folder_path, file_name)

            with open(file_path, "r", encoding="utf-8") as file:
                prompt_data = json.load(file)

            prompts.append(prompt_data)

    return prompts