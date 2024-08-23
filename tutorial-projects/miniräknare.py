
program_loop = True
while program_loop == True:

    # Skapar en tom lista för att samla all input på en container. 
    user_input_list = []
    
    # Steg 1: första input av användaren. 
    user_operand_1 = input("Ange operand1: ").strip()
    
    # Väjer try för att felhantera
    try:
        user_operand_1 = int(user_operand_1)
    
    except ValueError:
        print("Error 1: Operanden behöver vara ett heltal. Börja om")
        
    # Steg 2: kontrollerar om user input är int
    if type(user_operand_1) == int:
        user_input_list.append(user_operand_1)
        user_operand = input("Ange räknesätt: ").strip()
                
        # Steg 3 kontrollerar om operand
        if user_operand in ["+", "-", "/", "*","//","%"]:
            user_input_list.append(user_operand)
            user_operand_2 = input("Ange operand2: ").strip()
            
            # Väjer try för att felhantera
            try:
                user_operand_2 = int(user_operand_2)
            except ValueError:
                print("Error 3: Operanden behöver vara ett heltal. Börja om")
                
            #Steg 4: Sista kontrollen om user input är int
            if type(user_operand_2) == int:
                user_input_list.append(user_operand_2)

                #Bryter ut alla delar från listan
                operand_1 = user_input_list[0]
                operator = user_input_list[1]
                operand_2 = user_input_list[2]
                
                # Steg 5: Påbörjar beräkningarna
                if operator == "+":
                    print(f"Svar {operand_1} {operator} {operand_2} = {operand_1 + operand_2}")

                elif operator == "-":
                    print(f"Svar {operand_1} {operator} {operand_2} = {operand_1 - operand_2}")
                
                elif operator == "*":
                    print(f"Svar {operand_1} {operator} {operand_2} = {operand_1 * operand_2}")

                elif operator == "/":
                    if operand_2 != 0:
                        print(f"Svar {operand_1} {operator} {operand_2} = {operand_1 / operand_2}")
                    else: 
                        print("Error 4: Division med nolla är ej möjligt")

                elif  operator == "%":
                    if operand_2 != 0:
                        print(f"Svar {operand_1} {operator} {operand_2} = {operand_1 % operand_2}")
                    else: 
                        print("Error 5: Modulus med nolla är ej möjligt")

                elif operator == "//":
                    if operand_2 != 0:
                        print(f"Svar {operand_1} {operator} {operand_2} = {operand_1 // operand_2}")
                    else:
                        print("Error 4: Heltalsdividison med nolla är ej möjligt")
                
                # Steg 6: Kontrollera om användaren vill avsluta programmet. 
                continue_program = input("Vill du göra en ny beräkning (j/n)? ").lower()
                while continue_program not in["j", "n"]:
                    continue_program = input("Vill du göra en ny beräkning (j/n)? ").lower()

                if continue_program == "n":
                    print("Programmet avslutas")
                    program_loop = False
        else: 
            print("Error 2: Felaktig operator. Börja om") 




    













