import psycopg2
import datetime
from random import randint

class System:
    
    def __init__(self):
        self.db_connection = psycopg2.connect(
            dbname="db_taller3",
            user="postgres",
            password="Dgo951mz",
            host="localhost"
        )
        self.db_cursor = self.db_connection.cursor()

    def loginUser(self, username, password):

        self.db_cursor.execute("select * from entrenador where entrenador.username = '" + username + "'")
        response = self.db_cursor.fetchall()

        if len(response) == 0:
            raise NameError("** ERROR, usuario no registrado **")
        user = response[0] 
        
        if user[1] != password:
            raise Exception("** ERROR, contraseña incorrecta **")
        
        return user

    def registerUser(self, username, password, name, lastname, birth_date):
        
        self.db_cursor.execute("insert into entrenador values ('" + username + "', '" + password + "', '" + name + "', '" + lastname + "', " + str(self.__calculateAge(birth_date)) + ", '" + birth_date + "')")
        self.db_connection.commit()
        self.db_cursor.execute("insert into equipo_lucha (username_entrenador) values ('" + username + "')")
        self.db_connection.commit()
        self.db_cursor.execute("insert into creatudex (username_entrenador) values ('" + username + "')")
        self.db_connection.commit()
       
        return self.loginUser(username, password)

    def getSpecies(self):

        self.db_cursor.execute("select * from especie")
        return self.db_cursor.fetchall()

    def registerSpecie(self, specie_id, username_creatudex):

        self.db_cursor.execute("select especie.nombre_especie from creatudex "
                                + "inner join entrenador "
                                + "on creatudex.username_entrenador = entrenador.username "
                                + "inner join especies_registradas "
                                + "on creatudex.id_creatudex = especies_registradas.id_creatudex "
                                + "inner join especie "
                                + "on especies_registradas.id_especie = especie.id_especie "
                                + "where entrenador.username = '" + username_creatudex + "' and especie.id_especie = " + str(specie_id))

        response = self.db_cursor.fetchall()

        if len(response) == 0:
            
            self.db_cursor.execute("select creatudex.id_creatudex from creatudex inner join entrenador on creatudex.username_entrenador = entrenador.username where entrenador.username = '" + username_creatudex + "'")
            response = self.db_cursor.fetchall()
            specie = response[0]
            creatudex_id = int(specie[0])
            self.db_cursor.execute("insert into especies_registradas values (" + str(specie_id) + ", " + str(creatudex_id) + ")")
            self.db_connection.commit()

    def createNewMonster(self, specie):
        monster = []
        query = "select ataque.nombre_ataque, tipo.nombre, ataque.base_damage from ataque inner join tipo on (ataque.id_tipo = tipo.id_tipo) where "
        
        if specie[3] == None:
            query += "ataque.id_tipo = " + str(specie[2])
        else:
            query += "(ataque.id_tipo = " + str(specie[2]) + " or ataque.id_tipo = " + str(specie[3]) + ")"

        self.db_cursor.execute(query)
        compatible_attacks = self.db_cursor.fetchall()
        attacks_number = randint(1, 4)
        attacks = []

        for i in range(len(compatible_attacks)):
            if i + 1 <= attacks_number:
                selected = False

                while not selected:
                    attack = compatible_attacks[randint(0, len(compatible_attacks) - 1)]
                    
                    if attack not in attacks:
                        selected = True
                        attacks.append(attack)

        monster.append(randint(1, 4)) # velocidad
        monster.append(attacks) # ataques

        return monster

    # returns a tuple of every specie registered on the creatudex of
    # an specific user.
    def getRegisteredSpecies(self, username):

        self.db_cursor.execute("select especie.id_especie, especie.nombre_especie nombre, especie.id_tipo1, especie.id_tipo2 "
                        + "from creatudex "
                        + "inner join entrenador "
                        + "on creatudex.username_entrenador = entrenador.username "
                        + "inner join especies_registradas "
                        + "on creatudex.id_creatudex = especies_registradas.id_creatudex "
                        + "inner join especie "
                        + "on especies_registradas.id_especie = especie.id_especie "
                        + "where entrenador.username = '" + username + "'")
        return self.db_cursor.fetchall()

    def getSpecieTypes(self, specie_id):
        self.db_cursor.execute("select tipo.nombre from especie inner join tipo on especie.id_tipo1 = tipo.id_tipo or especie.id_tipo2 = tipo.id_tipo where especie.id_especie = " + str(specie_id))
        return self.db_cursor.fetchall()

    def getOpponentTo(self, username):
        self.db_cursor.execute("select * from entrenador where entrenador.username != '" + username + "'")
        opponents = self.db_cursor.fetchall()

        return opponents[randint(0, len(opponents) - 1)]

    def showUserFightingTeam(self, username):
        
        query = "select especie.nombre_especie, monstruo.velocidad, monstruo.puntos_salud, monstruo.posicion_equipo, nombre_ataque1, nombre_ataque2, nombre_ataque3, nombre_ataque4 from monstruo inner join equipo_lucha on monstruo.id_equipo = equipo_lucha.id_equipo inner join especie on monstruo.id_especie = especie.id_especie where equipo_lucha.username_entrenador = '" + username + "'"
        self.db_cursor.execute(query)
        team = self.db_cursor.fetchall()
        team = self.__orderTeamByPosition(team)
        i = 0

        for j in range(6):
            if i < len(team):
                monster = team[i]
                
                if monster[3] != j + 1:
                    print("\n* Posición " + str(j + 1) + " => VACÍO")
                else:
                    i += 1
                    print("\n* Posición " + str(j + 1) + " => Monstruo: " + monster[0])
                    print("                Velocidad: " + str(monster[1]))
                    print("                Puntos de Salud: " + str(monster[2]))

                    for j in range(len(monster[4:])):
                        if monster[j + 4] != None:
                            print("                Ataque " + str(j + 1) + ": " + str(monster[j + 4]))
            else:
                print("\n* Posición " + str(j + 1) + " => VACÍO")
                

    def addMonsterToFightingTeam(self, monster, owner_username, position):
        
        # monster has the structure [speed, attacks, specie_name, health_points]
        self.db_cursor.execute("select equipo_lucha.id_equipo from equipo_lucha inner join entrenador on equipo_lucha.username_entrenador = entrenador.username where entrenador.username = '" + owner_username + "'")    
        response = self.db_cursor.fetchall()
        team = response[0]
        team_id = str(team[0])
        
        if self.__occupiedPosition(team_id, position):
            self.__changeMonsterPosition(owner_username, team_id, position)

        self.db_cursor.execute("select id_especie from especie where especie.nombre_especie = '" + monster[2] + "'")
        response = self.db_cursor.fetchall()
        specie = response[0]
        specie_id = str(specie[0])

        creation_query = "insert into monstruo(id_equipo, id_especie, posicion_equipo, puntos_salud, velocidad"
        
        for i in range(len(monster[1])):
            creation_query += ", nombre_ataque" + str(i + 1)
        
        creation_query += ") values (" + team_id + ", " + specie_id + ", " + str(position) + ", 100, " + str(monster[0])
        
        for attack in monster[1]:
            creation_query += ", '" + attack[0] + "'"
        creation_query += ")"

        self.db_cursor.execute(creation_query)
        self.db_connection.commit()

    def close(self):
        self.db_connection.close()
        self.db_cursor.close()

    def __changeMonsterPosition(self, username, team_id, destiny_position):
        
        existing_monsters = self.__monsterOnPosition(team_id, destiny_position)
        existing_monster = existing_monsters[0]
        print("\n* La posición " + str(destiny_position) + " está ocupada por " + existing_monster[1] + ", ¿qué quieres hacer con él?")
        print("1. Transferirlo")
        print("2. Cambiar de posición")
        option = self.__askOption(2, "-> ")

        if option == 1:
            self.db_cursor.execute("delete from monstruo where (monstruo.id_equipo = " + team_id + " and monstruo.posicion_equipo = " + str(destiny_position) + ")")
            self.db_connection.commit()

        else:
            new_position = self.__askOption(6, "¿En qúe posición quiere dejarlo? (1 - 6): ")

            while new_position == destiny_position:
                new_position = self.__askOption(6, "** Elija otra posición que no sea la actual **: ")
            
            if self.__occupiedPosition(team_id, new_position):
               self.__changeMonsterPosition(username, team_id, new_position)

            print("updating")
            self.db_cursor.execute("update monstruo set posicion_equipo = " + str(new_position) + " where monstruo.id_monstruo = " + str(existing_monster[0]))
            self.db_connection.commit()

    def __askOption(self, options_number, message = None):
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

    def __monsterOnPosition(self, team_id, position):
        self.db_cursor.execute("select monstruo.id_monstruo, especie.nombre_especie from monstruo inner join especie on especie.id_especie = monstruo.id_especie where (monstruo.id_equipo = " + str(team_id) + " and monstruo.posicion_equipo = " + str(position) + ")")
        return self.db_cursor.fetchall()

    def __occupiedPosition(self, team_id, position):
        self.db_cursor.execute("select * from monstruo where (monstruo.id_equipo = " + str(team_id) + " and monstruo.posicion_equipo = " + str(position) + ")")
        return len(self.db_cursor.fetchall()) > 0

    def __orderTeamByPosition(self, team_array):

        if len(team_array) <= 1:
            return team_array

        monster_pivot = team_array[int(len(team_array) / 2)]
        pivot = int(monster_pivot[3])
        smallers = []
        biggers = []

        for monster in team_array:
            if pivot != int(monster[3]):
                if int(monster[3]) < pivot:
                    smallers.append(monster)
                else:
                    biggers.append(monster)

        return self.__orderTeamByPosition(smallers) + [monster_pivot] + self.__orderTeamByPosition(biggers)

    def __calculateAge(self, birth_date_string):
        
        birth_date = birth_date_string.split("-")
        birth_year = int(birth_date[0])
        birth_month = int(birth_date[1])
        birth_day = int(birth_date[2])
        actual_date = datetime.datetime.now()
        age = actual_date.year - birth_year

        if actual_date.month - birth_month < 0:
            age -= 1
        elif actual_date.month - birth_month == 0:
            if actual_date.day - birth_day < 0:
                age -= 1

        return age
