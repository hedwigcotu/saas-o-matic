from ..errors import InvalidTaxIdError

CIF_LETTERS = "JABCDEFGHI"

def is_valid_cif(value: str) -> bool:
    if len(value) != 9:
        return False
    
    first_letter = value[0]
    digits = value[1:8]
    control = value[8]

    if not digits.isdigit() or first_letter not in "ABCDEFGHJKLMNPQRSUVW":
        return False

    # Suma las posiciones pares (índices 1, 3, 5) tal cual
    sum_even = sum(int(digits[i]) for i in [1, 3, 5])
    
    # Suma las posiciones impares (índices 0, 2, 4, 6) duplicadas
    sum_odd = 0
    for i in [0, 2, 4, 6]:
        double = int(digits[i]) * 2
        sum_odd += double if double < 10 else double - 9

    total_sum = sum_even + sum_odd
    control_digit = (10 - (total_sum % 10)) % 10

    # Validación según el tipo de letra inicial
    if first_letter in "ABEH":
        return control == str(control_digit)
    elif first_letter in "KPQS":
        return control == CIF_LETTERS[control_digit]
    elif first_letter in "CDFGJNRUVW":
        return control == str(control_digit)
        
    return False