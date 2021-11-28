from system import System
import datetime
import random
import time

def login(game_system):

    user = None
    
    while user == None:
        username = input("\nNombre de usuario: ")
        password = input("Contraseña: ")
        
        try:
            user = game_system.loginUser(username, password)
        except NameError as error:
           
            print(error)
            register_now = input("¿Registrar ahora? (S-N): ").lower()
            
            while register_now != "s" and register_now != "n":
                register_now = input("Ingrese una opción correcta (S-N): ").lower()

            if register_now == "s":
                user = register(game_system, username)

        except Exception as ex:
            print(ex)

    print("\n ** Bienvenido/a " + user[0] + " **")
    return user

def register(game_system, username):
    
    name = input("\nPrimer nombre: ")
    lastname = input("Primer apellido: ")
    birth_date = askBirthDate()
    password = input("Contraseña: ")

    return game_system.registerUser(username, password, name, lastname, birth_date)

def askBirthDate():
    birth_date = input("Fecha de nacimiento (aaaa-mm-dd): ")

    while not dateValidation(birth_date):
        print("\n** ERROR, fecha de nacimiento inválida **")
        birth_date = input("Ingrese fecha de nacimiento (aaaa-mm-dd): ")

    return birth_date

def dateValidation(date):

    date_array = date.split("-")
    
    if len(date_array) != 3:
        return False

    for i in range(len(date_array)):
        try:
            number = int(date_array[i])
        except ValueError:
            return False

    day = int(date_array[2])
    month = int(date_array[1])
    year = int(date_array[0])

    # El juego solamente soporta usuarios mayores de 150 y menores de 100 años.
    if day < 1 or day > 31 or month < 1 or month > 12 or year < (datetime.datetime.now().year - 100)  or year > (datetime.datetime.now().year - 10):
        return False
   
    return True

def askOption(options_number, message = None):

    option_validated = False

    while not option_validated:

        if message == None:
            option = input("Ingrese una opción: ")
        else:
            option = input(message)

        try:
            option = int(option)
            option_validated = True
        except ValueError:
            option_validated = False

        if option_validated:
            if option >= 1 and option <= options_number:
                return option
            option_validated = False

def showUserProfile(game_system, user):
    close = False

    while not close:

        print("\n+ Entrenador: " + user[2], user[3])
        print("\n1. Creatudex")
        print("2. Equipo Lucha")
        print("3. Expedición")
        print("4. Lucha")
        print("5. Cerrar sesión\n")
        option = askOption(5)

        if option == 1:
            showUserCreatudex(game_system, user)

        elif option == 2:
            game_system.showUserFightingTeam(user[0])

        elif option == 3:
            expedition(game_system, user)

        elif option == 4:
            fight(game_system, user[0])

        else:
            close = True

def fight(game_system, username):

    opponent = game_system.getOpponentTo(username)
    print(opponent)

def showUserCreatudex(game_system, user):
    species = game_system.getRegisteredSpecies(user[0])

    print("\n ++++ CREATUDEX ++++\n")
    print("Estas especies has registrado en tu creatudex:")

    for specie in species:
        print("\nID Especie:", specie[0])
        print("Nombre:", specie[1])

        types = game_system.getSpecieTypes(specie[0])
        for i in range(len(types)):
            t = types[i]
            print("Tipo " + str(i + 1) + ": " + t[0])

def expedition(game_system, user):
    
    print("\n** Para salir de expedición escribe 'salir' al intentar capturar un monstruo **\n")
    species = game_system.getSpecies()

    while True:
        specie = species[random.randint(1, len(species)) - 1]
        
        time.sleep(random.randint(2, 5))
        print("\n¡Te has encontrado con " + specie[1] + "!")
        capture = input("¿Quieres intentar capturarlo? (S - n): ").lower()

        while capture != "s" and capture != "n" and capture != "salir":
            capture = input("Ingrese una opción correcta (S - n): ").lower()

        if capture == "salir":
            break

        if capture == "s":
            capturingAnimation()

            if isCaptured():
                print("\n¡Has capturado a " + specie[1] + "!,")
                monster = game_system.createNewMonster(specie)
                game_system.registerSpecie(specie[0], user[0])
                print("estos son sus atributos: \n")
                print(" - Velocidad: " + str(monster[0]))
                attacks = monster[1]
                
                for i in range(len(attacks)):
                    attack = attacks[i]
                    print(" - Ataque " + str(i + 1) + " => nombre: " + attack[0])
                    print("               tipo: " + str(attack[1]))
                    print("               daño base: " + str(attack[2]))

                save = input("\n¿Quieres agregarlo a tu equipo de lucha? (s-n): ").lower()
                while save != "s" and save != "n":
                    save = input("** Ingrese una opcion correcta (s-n) **: ").lower()

                if save == "s":
                    game_system.showUserFightingTeam(user[0])
                    monster.append(specie[1])
                    monster.append(100)
                    position = askOption(6, "¿En qué posición desea agregarlo?: ") 
                    game_system.addMonsterToFightingTeam(monster, user[0], position)
                    
                else:
                    print("\n¡" + specie[1] + " ha sido transferido!")

            else:
                print("\n* " + specie[1] + " se ha escapado :c *")

    
def isCaptured():
    return random.random() > 0.4

def capturingAnimation():
    time.sleep(0.5)
    print("\n.")
    time.sleep(1)
    print(".")
    time.sleep(1)
    print(".")
    time.sleep(1)
    print(".")
    time.sleep(0.3)
    print(".")
    time.sleep(0.3)
    print(".")
    time.sleep(1)

def startGame():
    
    game_system = System()
    user = login(game_system)
    showUserProfile(game_system, user)
    game_system.close()

startGame()
