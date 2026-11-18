DNI_LETTERS = "TRWAGMYFPDXBNJZSQVHLCKE"

def is_valid_dni(value: str) -> bool:
    if len(value) != 9 or not value[:8].isdigit() or not value[8].isalpha():
        return False
    return DNI_LETTERS[int(value[:8]) % 23] == value[8].upper()