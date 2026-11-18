from .dni import DNI_LETTERS

def is_valid_nie(value: str) -> bool:
    if len(value) != 9 or value[0] not in "XYZ" or not value[1:8].isdigit() or not value[8].isalpha():
        return False
    
    prefix_map = {"X": "0", "Y": "1", "Z": "2"}
    num_str = prefix_map[value[0]] + value[1:8]
    return DNI_LETTERS[int(num_str) % 23] == value[8].upper()