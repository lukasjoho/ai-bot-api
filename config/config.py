import os

def load_system_prompt(is_new_user: bool):
    """Load system prompt from config file and replace dynamic values"""
    # Get project root directory
    project_root = os.path.dirname(os.path.dirname(__file__))
    config_path = os.path.join(project_root, "config", "system_prompt.txt")
    
    with open(config_path, 'r', encoding='utf-8') as file:
        system_prompt = file.read().strip()
    
    # Replace dynamic values
    new_user_value = "Ja" if is_new_user else "Nein"
    system_prompt = system_prompt.replace("[NEW_USER]", new_user_value)
    
    return system_prompt
