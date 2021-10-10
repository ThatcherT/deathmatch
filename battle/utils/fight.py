from battle.utils.weapons import *

class Fighter:
    def __init__(self, name):
        self.name = name
        self.health = 1500
        self.spec = 100
        self.frozen = False
        self.poisoned = False
        self.poison_damage = 0

        self.enemy = None # this should be an Fighter object
        self.current_weapon = None # this should be Weapon object
    

    def select_weapon(self, weapon_name):
        try:
            weapon = globals()[weapon_name.title()]()
            self.current_weapon = weapon
            return weapon
        except:
            # Weapon doesn't exist yet!
            return


    @property
    def can_use_weapon(self):
        # return bool if fighter can use weapon
        return self.current_weapon.fighter_can_use(self)

    def attack(self):
        # use weapon to attack enemy, and if needed, heal self
        weapon = self.current_weapon
        attack_log = weapon.attack(self, self.enemy)
        return attack_log
    
    def take_damage(self, damage):
        # take damage from enemy
        self.health = max(self.health - damage, 0)
        return
    
    def take_heal(self, health):
        self.health = min(self.health + health, 1500)
        return

    def apply_spec_reduction(self, spec_used):
        # reduce spec by spec_used
        self.spec -= spec_used
        return


    def is_legal(self, action):
        available_weapons = self.available_weapons()
        if not type(action) == str:
            action = WEAPON_LST[action]
        if action in available_weapons or action == "toenail":         
            return True
        else:
            return False

    @property
    def legal_actions(self):
        legal_actions = []
        for i in range(len(WEAPON_LST)):
            weapon = WEAPON_LST[i]
            if self.is_legal(weapon):
                legal_actions.append(1)
            else:
                legal_actions.append(0)
        return legal_actions


    def available_weapons(self):
        return [weapon for weapon in WEAPON_LST if self.get_weapon(weapon).fighter_can_use(self)]
    
    def get_weapon(self, weapon_name):
        weapon = globals()[weapon_name.title()]() # get weapon class
        # self.current_weapon = weapon
        return weapon

    def __str__(self):
        return "Fighter with health " + str(self.health) + " and spec " + str(self.spec)