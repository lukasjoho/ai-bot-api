import os

def load_system_prompt():
    project_root = os.path.dirname(os.path.dirname(__file__))
    config_path = os.path.join(project_root, "config", "system_prompt.txt")
    
    with open(config_path, 'r', encoding='utf-8') as file:
        prompt = file.read().strip()
    
    return prompt
