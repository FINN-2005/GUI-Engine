import json

# Load from JSON string or file
with open('gui.json', 'r') as f:
    gui_data = json.load(f)

# Access style color
color = gui_data['style']['button']['text_color']

# Access button text
text = gui_data['structure']['button']['text']

print(color, text)
