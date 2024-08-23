# Konverterar user input till en lista
def convert_to_list(user_input):
    user_input_list = list(user_input.split(" "))
    if len(user_input_list) == 3:  
        return user_input_list
    else: 
        return False
        
# Extraherar arithmetic symbolen
def get_arithmetic_operator(input_list):
    arithmetic_symbol = input_list[1]
    arithmetic_list= ["+", "-", "/", "*","//","%"]
    if arithmetic_symbol in arithmetic_list:
        return arithmetic_symbol
    else: 
        return False

# Extraherar operander
def get_operands(input_list):
    operand_1 = input_list[0]
    operand_2 = input_list[2]
    try:
        float(operand_1)
        float(operand_2)
        return float(operand_1), float(operand_2)
    
    except ValueError:
        return False


def do_calculation(operands, arithmetic_symbol):
    # Tar ut index från operanderna eftersom get_operands() returnerar en tuple
    operand_1 = operands[0]
    operand_2 = operands[1]
    if arithmetic_symbol == "+": 
        return operand_1 + operand_2
    elif arithmetic_symbol == "-":
        return operand_1 - operand_2
    elif arithmetic_symbol == "*": 
        return operand_1 * operand_2
    elif arithmetic_symbol == "/":
        if operand_2 != 0:
            return operand_1 / operand_2
        else:
            return False
    elif arithmetic_symbol == "//":
        if operand_2 != 0:
            return operand_1 // operand_2
        else: 
            return False
    elif arithmetic_symbol == "%":
        if operand_2 != 0:
            return operand_1 % operand_2
        else:
            return False
    else: 
        return False

# Huvudprogramloop
while True:
    user_input = input("Vad vill du räkna ut: ")
    user_input = convert_to_list(user_input)
    if user_input is not False:
        user_input_operands = get_operands(user_input)
        
        if user_input_operands is not False:
            user_input_arithmetic = get_arithmetic_operator(user_input)

            if user_input_arithmetic is not False:
                answer = do_calculation(user_input_operands, user_input_arithmetic)
                if answer is not False:
                    print(f"{user_input_operands[0]} {user_input_arithmetic} {user_input_operands[1]} = {answer}")
                else: 
                    print("Error: Division med 0")
            else: 
                print("Error: Felaktig operator")
        else:
            print("Error: Operand måste vara en siffra") 
    else: 
        print("Error: Ange operand, mellanslag, operator, mellanslag och operand")