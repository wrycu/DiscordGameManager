configSchema = {
    "type": "object",
    "required": ["discord"],
    "properties": {
        "discord": {
            "type": "object",
            "required": ["username", "oauth_token"],
            "properties": {
                "username": {"type": "string"},
                "oauth_token": {"type": "string"},
                "channels": {
                    "type": "array",
                    "items": {"type": "string"},
                    "uniqueItems": True
                },
                "global_admins": {
                    "type": "array",
                    "items": {"type": "integer"},
                    "uniqueItems": True
                },
                "required_roles": {
                    "type": "array",
                    "items": {"type": "string"},
                    "uniqueItems": True
                },
            }
        },
        "games": {
            "type": "array",
            "items": {
                "type": "object",
                "required": ["name", "type", "app_id", "install_dir", "commands"],
                "properties": {
                    "name": {"type": "string"},
                    "type": {"type": "string"},
                    "app_id": {"type": "string"},
                    "install_dir": {"type": "string"},
                    "commands": {
                        "type": "object",
                        "required": ["start", "stop", "connect", "delay"],
                        "properties": {
                            "start": {"type": "string"},
                            "stop": {"type": "string"},
                            "update": {"type": "string"},
                            "connect": {"type": "string"},
                            "players": {"type": "string"},
                            "version": {"type": "string"},
                            "delay": {"type": "string"},
                        }
                    },
                    "admins": {
                        "type": "array",
                        "items": {"type": "integer"},
                        "uniqueItems": True
                    },
                }
            },
            "uniqueItems": True
        },
    },
}