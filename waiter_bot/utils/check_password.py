def validate_password(password: str) -> str:
    if len(password) < 8:
        return "Parol 8 ta belgidan kam bo'lmasligi kerak!"
    if len(password) > 32:
        return "Parol 32 ta belgidan ko'p bo'lmasligi kerak!"
    if not password.isalpha():
        return "Parolni ichida kamida 1 ta raqam bo'lishi kerak!"
    if not password.isdigit():
        return "Parolni ichida kamida 1 ta harf bo'lishi kerak!"
