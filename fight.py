import random
import numpy as np
import math
from weapons import *
class Fight():
    def __init__(self):
        # create fighters
        self.fighter0 = Fighter(name='Fighter 0')
        self.fighter1 = Fighter(name='Fighter 1')

        # set each fighter to enemy of each other
        self.fighter0.enemy = self.fighter1
        self.fighter1.enemy = self.fighter0

        # store lst of fighters to track turn selection and such
        self.fighters = [self.fighter0, self.fighter1]

        # randomly set turn to 0 or 1, use this to index list later
        self.turn = random.randint(0, 1)

        # start fight
        self.do_turn()
        return

    def get_attacking_fighter(self):
        # return the attacking fighter
        return self.fighters[self.turn % 2]
    

    def do_turn(self):
        attacker = self.get_attacking_fighter()
        defender = attacker.enemy
        
        print(f'{attacker.name}({attacker.health}) is attacking {defender.name}({defender.health})')

        # get user input for weapon
        weapon_name = input("Choose your weapon: ")

        # get weapon class
        weapon = attacker.select_weapon(weapon_name)

        if not weapon:
            # this weapon doesn't exist yet!
            print("That weapon doesn't exist yet!")
            self.do_turn()

        else:
            # check if fighter can use weapon, return bool
            if attacker.can_use_weapon:
                # fight
                attacker.attack()

                # check if defender is dead
                if defender.health <= 0:
                    print(defender.name, ' is dead!')
                    print(attacker.name, ' wins!')
                    # end fight
                    return
                else:
                    # defender is still alive, do turn
                    # reset vars
                    attacker.frozen = False
                    
                    # switch turn
                    self.turn += 1
                    # do turn again
                    print('Switching turn to', self.fighters[self.turn % 2].name)
                    print('----------------------------------------')
                    self.do_turn()
            else:
                print("You can't use that weapon!")
                self.do_turn()

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
        weapon.attack(self, self.enemy)
    
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

    def __str__(self):
        return "Fighter with health " + str(self.health) + " and spec " + str(self.spec)