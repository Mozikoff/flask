dictionary_schema = {
    "type": "object",
    "properties": {
        "key": {"type": "string"},
        "value": {"type": "string"}
    },
    "additionalProperties": False,
    "required": ["key", "value"]
}