from pathlib import Path

window_settings = {
    "resolution": (854, 480),
    "window_name": "Event Handler | 0001"
}

pyside_size = {
    'button_size': 50,
    'log_menu_size': 100,
    
}

games_supported = [
    "Arknights",
    "Limbus Company",
    "Azur Lane"
]

current_path = Path(__file__)
parent_folder = Path(current_path).parent.parent
to_json = Path(parent_folder/'backend'/'local_user.json')