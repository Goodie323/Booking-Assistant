def is_booking_confirmation(text):
    text = text.lower().strip()

    confirmations = [
        "yes",
        "yes please",
        "book it",
        "please book",
        "book",
        "confirm",
        "confirm it",
        "go ahead",
        "sure",
        "ok book",
        "okay book"
    ]

    return any(phrase in text for phrase in confirmations)
