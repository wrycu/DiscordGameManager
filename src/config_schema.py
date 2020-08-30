config_schema = {
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
                "required": ["name", "properties", "commands"],
                "properties": {
                    "name": {"type": "string"},
                    "admins": {
                        "type": "array",
                        "items": {"type": "integer"},
                        "uniqueItems": True
                    },
                    "properties": {
                        "type": "object",
                        "properties": {
                            "install_dir": {
                                "type": "string",
                                "pattern": ".*/$",
                            },
                            "ip_addr": {"type": "string"},
                            "port": {"type": "integer"},
                            "password": {"type": "string"},
                            "app_id": {"type": "integer"},
                            "proc_name": {"type": "string"},
                        },
                    },
                    "commands": {
                        "type": "object",
                        "required": ["start", "stop", "connect", "delay"],
                        "properties": {
                            "start": {
                                "type": "object",
                                "properties": {
                                    "text": {"type": "string"},
                                    "type": {"type": "string"},
                                },
                            },
                            "stop": {
                                "type": "object",
                                "properties": {
                                    "text": {"type": "string"},
                                    "type": {"type": "string"},
                                },
                            },
                            "update": {
                                "type": "object",
                                "properties": {
                                    "text": {"type": "string"},
                                    "type": {"type": "string"},
                                },
                            },
                            "connect": {
                                "type": "object",
                                "properties": {
                                    "text": {"type": "string"},
                                    "type": {"type": "string"},
                                },
                            },
                            "players": {
                                "type": "object",
                                "properties": {
                                    "text": {"type": "string"},
                                    "type": {"type": "string"},
                                },
                            },
                            "version": {
                                "type": "object",
                                "properties": {
                                    "text": {"type": "string"},
                                    "type": {"type": "string"},
                                },
                            },
                            "delay": {
                                "type": "object",
                                "properties": {
                                    "text": {"type": "string"},
                                    "type": {"type": "string"},
                                },
                            },
                        }
                    },
                },
            },
            "uniqueItems": True
        },
    },
}
