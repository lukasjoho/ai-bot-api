import os

def load_knowledge_prompt():
    project_root = os.path.dirname(os.path.dirname(__file__))
    config_path = os.path.join(project_root, "config", "knowledge_prompt.txt")
    
    with open(config_path, 'r', encoding='utf-8') as file:
        prompt = file.read().strip()
    
    return prompt

def load_communication_prompt(original_message: str, name: str, is_new_user: bool = False):
    project_root = os.path.dirname(os.path.dirname(__file__))
    config_path = os.path.join(project_root, "config", "communication_prompt.txt")
    
    with open(config_path, 'r', encoding='utf-8') as file:
        prompt_template = file.read().strip()
    
    new_user_note = "Ja - zeige interaktive Fragenliste!" if is_new_user else "Nein"
    
    return prompt_template.format(
        original_message=original_message,
        name=name,
        new_user_note=new_user_note
    )
