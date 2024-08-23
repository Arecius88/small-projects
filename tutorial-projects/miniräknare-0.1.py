program_loop = True
inner_loop = True


while program_loop == True:
    multiplikationstabbell = int(input("Ange tabell: "))
    start_värde = int(input("Ange startintervall: "))
    stopp_värde = int(input("Ange stoppintervall: "))
    start_värde = start_värde - 1

    print(23 * "-")
    print(f"{multiplikationstabbell}:ans tabell")
    print(23 * "-")


    for step in range(int(start_värde), int(stopp_värde)):
        step +=1
        print(f"{step:3} * {multiplikationstabbell} = {step*multiplikationstabbell:3}")

    end_program = input("\nVill du avsluta (j/n): ").lower()
    while inner_loop == True:

        if len(end_program)== 1 and end_program == "j":
            program_loop = False
            print("\nProgrammet avslutas!")
            inner_loop = False
            
        elif end_program !="n": 
            end_program = input("\nVill du avsluta (j/n): ").lower()
        
        if end_program == "n":
            inner_loop=False


