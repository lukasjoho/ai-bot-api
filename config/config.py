import os

def load_system_prompt(name: str = None, is_new_user: bool = None):
    project_root = os.path.dirname(os.path.dirname(__file__))
    config_path = os.path.join(project_root, "config", "system_prompt.txt")
    
    with open(config_path, 'r', encoding='utf-8') as file:
        prompt = file.read().strip()
    
    # Replace placeholders with actual values
    if name is not None:
        prompt = prompt.replace("{name}", name)
    if is_new_user is not None:
        prompt = prompt.replace("{is_new_user}", "Ja" if is_new_user else "Nein")
    
    return prompt
