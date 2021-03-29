class Pokemon:
    
    def __init__(self, name:str, power_factor:float):
        self.name = name
        self.power_factor =  power_factor
        self.energy = 5
    
    def __add__(self, another):
        if type(another) == type(Pokemon):
            return another.power_factor + self.power_factor

    def is_hibernating(self):
        return self.energy <= 0


    

def valid_party(party:[Pokemon]):
    for pokemon in party:
        if (pokemon.is_hibernating()):
            return False
    return True


def battle_cost(difficult:int,party:[Pokemon]):

    party_power = sum(party)

    time = difficult/party_power

    return time