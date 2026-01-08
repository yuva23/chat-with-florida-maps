def handle_intent(intent):
    return {
        "type": "map",
        "layers": intent["layers"],
        "message": f"Displaying {', '.join(intent['layers'])} for {intent['location']}"
    }
