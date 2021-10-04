
import gym
from gym import spaces


import numpy as np

import config
from stable_baselines import logger

##############################################################################################################################
##############################################################################################################################
##################################################### WEAPONS ################################################################
##############################################################################################################################
##############################################################################################################################

import random

RANGED = "ranged"
MELEE = "melee"

WEAPON_LST = ['guth', 'punch', 'blood', 'maul', 'korasi', 'dbow', 'dbolt', 'smoke', 'ice', 'sgs', 'dds', 'msb', 'dclaws', 'ags', 'onyx', 'zgs', 'surge', 'storm']

class Weapon:
    """
    This is an abstract object.
    """
    
    def __init__(self):
        self.spec = 0
        self.freezing = False
        self.healing = False
        self.poisoning = False
        self.hp_restriction = 1501

    
    @property
    def percentile(self):
        percentile = random.randint(0, 100)
        return percentile


    def calc_damage(self):
        # every derived class should have a method calc_damage
        # this uses percentile to calculate damage from a custom function
        raise NotImplementedError


    def calc_heal(self):
        # some derived classes will have a calc_heal method
        # if class doesn't have, then heal is 0
        return 0


    def poisoned(self):
        # some derivced class will have a poisened method that
        # will return True if the weapon poisons the opponent
        return False


    def fighter_can_use(self, fighter):
        return fighter.spec >= self.spec and (not fighter.frozen or self.type == RANGED) and (fighter.health < self.hp_restriction)

    
    def attack(self, attacker, defender):
        # refresh percentile and caluclate damage
        # self.set_percentile()
        # print(self.percentile)
        # get damage
        damage = self.calc_damage()

        # apply damage
        defender.take_damage(damage)

        print("{} attacks {} with {} for {} damage.".format(attacker.name, defender.name, self.__class__.__name__, damage))

        # apply poison state
        if self.poisoned():
            defender.poisoned = True
            defender.poison_damage = 40
        
        if defender.poisoned:
            # apply poison damage
            defender.take_damage(defender.poison_damage)
            print(defender.name, ' suffers ', defender.poison_damage, ' from poison.')

            # update or reset poison damage
            if defender.poison_damage == 32:
                defender.poison_damage = 0
                defender.poisoned = False
            else:
                defender.poison_damage -= 2
        elif self.poisoning:
            if defender.poisoned:
                print(attacker.name, 'poisons ', defender.name, ' for ', defender.poison_damage, ' damage.')
            else:
                print(attacker.name, 'failed to poison ', defender.name)


        # get heal
        heal = self.calc_heal()
        if self.healing:
            if heal == 0:
                print("Healing failed.")
            else:
                print("{} heals for {} health.".format(attacker.name, heal))

        # apply heal
        attacker.take_heal(heal)

        # apply spec reduction
        attacker.apply_spec_reduction(self.spec)
        # print("{} health is {}".format(attacker.name, attacker.health))
        # print("{} health is {}".format(defender.name, defender.health))


class Guth(Weapon):
    def __init__(self):
        super().__init__()
        self.type = MELEE
        self.healing = True


    def calc_damage(self):
        percentile = self.percentile
        if percentile <= 20:
            damage = random.randint(1,149)
        elif percentile <= 81:
            damage = random.randint(150,275)
        else:
            damage = random.randint(276,320)
        self.damage_dealt = damage
        return damage


    def calc_heal(self):
        heal_chance = random.randint(1,10)
        if heal_chance <= 4:
            heal = self.damage_dealt
        else:
            heal = 0
        self.heal_dealt = heal
        return heal
        

class Punch(Weapon):
    def __init__(self):
        super().__init__()
        self.type = MELEE


    def calc_damage(self):
        percentile = self.percentile
        if percentile <= 20:
            damage = random.randint(1,125)
        else:
            damage = random.randint(126,225)
        self.damage_dealt = damage
        return damage


class Blood(Weapon):
    def __init__(self):
        super().__init__()
        self.type = RANGED
        self.healing = True
    

    def calc_damage(self):
        percentile = self.percentile
        if percentile <= 20:
            damage = random.randint(1,100)
        elif percentile <= 81:
            damage = random.randint(101,280)
        else:
            damage = random.randint(281,330)
        self.damage_dealt = damage
        return damage

    def calc_heal(self):
        heal = int(self.damage_dealt*.4)
        self.heal_dealt = heal
        return heal

class Maul(Weapon):
    def __init__(self):
        super().__init__()
        self.type = MELEE
        self.spec = 100
    

    def calc_damage(self):
        percentile = self.percentile
        if percentile <= 13:
            damage = random.randint(250,375)
        elif percentile <= 74:
            damage = random.randint(376,600)
        else:
            damage = random.randint(601,750)
        self.damage_dealt = damage
        return damage    

    
class Korasi(Weapon):
    def __init__(self):
        super().__init__()
        self.type = MELEE
        self.spec = 75


    def calc_damage(self):
        percentile = self.percentile
        if percentile <= 10:
            damage = random.randint(1,350)
        elif percentile <= 71:
            damage = random.randint(351,650)
        else:
            damage = random.randint(651,710)
        self.damage_dealt = damage
        return damage


class Dbow(Weapon):
    def __init__(self):
        super().__init__()
        self.type = RANGED
        self.spec = 75


    def calc_damage(self):
        percentile = self.percentile
        if percentile <= 15:
            damage = random.randint(100,220) + random.randint(100,220)
        elif percentile <= 70:
            damage = random.randint(221,300) + random.randint(221,300)
        else:
            damage = random.randint(301,350) + random.randint(301,350)
        self.damage_dealt = damage
        return damage


class Dbolt(Weapon):
    def __init__(self):
        super().__init__()
        self.type = RANGED


    def calc_damage(self):
        percentile = self.percentile
        if percentile <= 12:
            damage = random.randint(1,175)
        elif percentile <= 80:
            damage = random.randint(176,374)
        else:
            damage = random.randint(375,600)
        self.damage_dealt = damage
        return damage


class Smoke(Weapon):
    def __init__(self):
        super().__init__()
        self.type = RANGED
        self.poisoning = True
    

    def calc_damage(self):
        percentile = self.percentile
        if percentile <= 20:
            damage = random.randint(1,200)
        elif percentile <= 70:
            damage = random.randint(201,300)
        else:
            damage = random.randint(301,350)
        self.damage_dealt = damage
        return damage
    
    def poisoned(self):
        poison_chance = random.randint(1,10)
        if poison_chance <= 7:
            return True
        return False

class Ice(Weapon):
    def __init__(self):
        super().__init__()
        self.type = RANGED
        self.freezing = True
    
    def calc_damage(self):
        percentile = self.percentile
        if percentile <= 20:
            damage = random.randint(1,100)
        elif percentile <= 81:
            damage = random.randint(101,250)
        else:
            damage = random.randint(251,330)
        self.damage_dealt = damage
        return damage

class Sgs(Weapon):
    def __init__(self):
        super().__init__()
        self.type = MELEE
        self.spec = 50
        self.healing = True
    
    def calc_damage(self):
        percentile = self.percentile
        if percentile <= 15:
            damage = random.randint(50,200)
        elif percentile <= 70:
            damage = random.randint(201,350)
        else:
            damage = random.randint(351,450)
        self.damage_dealt = damage
        return damage

    def calc_heal(self):
        heal = int(self.damage_dealt*.5)
        self.heal_dealt = heal
        return heal

class Dds(Weapon):
    def __init__(self):
        super().__init__()
        self.type = MELEE
        self.spec = 25

    def calc_damage(self):
        percentile = self.percentile
        if percentile <= 20:
            damage = random.randint(1,100) + random.randint(1,100)
        elif percentile <= 71:
            damage = random.randint(101,175) + random.randint(101,175)
        else:
            damage = random.randint(176,230) + random.randint(176,230)
        self.damage_dealt = damage
        return damage

class Msb(Weapon):
    def __init__(self):
        super().__init__()
        self.type = RANGED
        self.spec = 50
    
    def calc_damage(self):
        percentile = self.percentile
        if percentile <= 20:
            damage = random.randint(75,150) + random.randint(75,150)
        elif percentile <= 81:
            damage = random.randint(151,230) + random.randint(151,230)
        else:
            damage = random.randint(231,300) + random.randint(231,300)
        self.damage_dealt = damage
        return damage

class Dclaws(Weapon):
    def __init__(self):
        super().__init__()
        self.type = MELEE
        self.spec = 50
    
    def calc_damage(self):
        percentile = self.percentile
        if percentile <= 20:
            damage = random.randint(1,50) + random.randint(1,50) + random.randint(1,50) + random.randint(1,50)
        else:
            damage = random.randint(51,140) + random.randint(51,140) + random.randint(51,140)+ random.randint(51,140)
        self.damage_dealt = damage
        return damage

class Ags(Weapon):
    def __init__(self):
        super().__init__()
        self.type = MELEE
        self.spec = 50
    def calc_damage(self):
        percentile = self.percentile
        if percentile <= 20:
            damage = random.randint(150,200)
        elif percentile <= 61:
            damage = random.randint(201,400)
        else:
            damage = random.randint(401,510)
        self.damage_dealt = damage
        return damage

class Onyx(Weapon):
    def __init__(self):
        super().__init__()
        self.type = RANGED
        self.healing = True
    
    def calc_damage(self):
        percentile = self.percentile
        if percentile <= 20:
            damage = random.randint(1,125)
        elif percentile <= 61:
            damage = random.randint(126,275)
        else:
            damage = random.randint(276,375)
        self.damage_dealt = damage
        return damage
    
    def calc_heal(self):
        heal_chance = random.randint(1,10)
        if heal_chance <= 5:
            heal = int(self.damage_dealt * .5)
            self.heal_dealt = heal
            return heal
        else:
            self.heal_dealt = 0
            return 0

class Zgs(Weapon):
    def __init__(self):
        super().__init__()
        self.type = MELEE
        self.spec = 50
    def calc_damage(self):
        percentile = self.percentile
        if percentile <= 20:
            damage = random.randint(1,220)
        elif percentile <= 81:
            damage = random.randint(221,330)
        else:
            damage = random.randint(331,420)
        self.damage_dealt = damage
        return damage


class Surge(Weapon):
    def __init__(self):
        super().__init__()
        self.type = RANGED
        self.hp_restriction = 250
    
    def calc_damage(self):
        percentile = self.percentile
        if percentile <= 40:
            damage = random.randint(200,350)
        else:
            damage = random.randint(351,500)
        self.damage_dealt = damage
        return damage
    
class Storm(Weapon):
    def __init__(self):
        super().__init__()
        self.type = RANGED
    
    def calc_damage(self):
        percentile = self.percentile
        damage = random.randint(100,330)
        self.damage_dealt = damage
        return damage

##############################################################################################################################
##############################################################################################################################
##################################################### FIGHT MODULE ###########################################################
##############################################################################################################################
##############################################################################################################################

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

##############################################################################################################################
##############################################################################################################################
##################################################### FIGHT MODULE ###########################################################
##############################################################################################################################
##############################################################################################################################
   
class Player(Fighter):
    def __init__(self, name):
        super().__init__(name)
        self.health = 1500
        self.spec = 100
        self.frozen = False
        self.poisoned = False
        self.poison_damage = 0

        self.enemy = None # this should be an Fighter object
        self.current_weapon = None # this should be Weapon object


    def available_weapons(self):
        return [weapon for weapon in WEAPON_LST if self.get_weapon(weapon).fighter_can_use(self)]
                

    def get_weapon(self, weapon_name):
        weapon = globals()[weapon_name.title()]() # get weapon class
        self.current_weapon = weapon
        return weapon
        

class Token():
    def __init__(self, symbol, number):
        self.number = number
        self.symbol = symbol
        
        
class DeathmatchEnv(gym.Env):
    """
    Description:
        2 Players are fighting.
        Each player has a selection of weapons they can choose from.
        This selection may change temporarily (for one turn) or permanently (for the rest of the game)
        depending on the given state of the game.
        
    Source:
        This environment corresponds to an in-game battle on the MMORPG Runescape.
    Observation:
        Type: Box(6)
        Num     Observation               Min                     Max
        0       Attacker Health             0                    1500
        1       Attacker Spec               0                    100
        2       Attacker poison_damage      0                    40
        3       Attacker frozen             0                    1
        4       Defender Health             0                    1500
        5       Defender Spec               0                    100
        6       Defender poison_damage      0                    40

    Actions:
        Type: Discrete(18) we can take up to 18 actions
        Num   Action
        0     Guth
        1     Punch
        2     Blood
        3     Maul
        4     Korasi
        5     Dbow
        6     Dbolt
        7     Smoke
        8     Ice
        9     Sgs
        10    Dds
        11    Msb
        12    Dclaws
        13    Ags
        14    Onyx
        15    Zgs
        16    Surge
        17    Storm
    Reward:
        for blackjack:
            you get -1 if you bust
            you get 0 if you draw
            you get 1 if you stick and win
        for cartpole:
            you get 1 if you don't die
        for deathmatch:
            you get -1 if you lose
            you get 1 if your opponent died
            you get 0 otherwise
    Starting State:
        All observations begin with
        0 Attacker Health           1500
        1 Attacker Spec             100
        2 Attacker poison_damage    0
        3 Attacker frozen           0
        4 Defender Health           1500
        5 Defender Spec             100
        6 Defender poison_damage    0
    Episode Termination:
        Defender health is less than 0
    """

    metadata = {'render.modes': ['human']}

    def __init__(self, verbose = False, manual = False):
        print('Initializing Deathmatch Environment')
        super(DeathmatchEnv, self).__init__()
        self.name = 'deathmatch'
        self.manual = manual

        self.weapons = WEAPON_LST
        self.n_players = 2
        self.action_space = gym.spaces.Discrete(len(WEAPON_LST))
        self.observation_space = gym.spaces.Box(0, 1, (7 + self.action_space.n,))
        self.verbose = verbose
        

    @property
    def observation(self):
        """
        The point of this is to return a observation from the perspective of the current player
        """
        player = self.get_current_player()
        # iterate through each player        
        # player metrics

        # all values must be between -1 and 1
        health = ((player.health * 2) - 1500) / 1500
        spec = ((player.spec * 2) - 100) / 100
        poison_damage = ((int(player.poison_damage) * 2) - 40) / 40
        frozen = ((int(player.frozen) * 2) - 1) / 1
        
        # enemy metrics
        enemy_health = ((player.enemy.health * 2) - 1500) / 1500
        enemy_spec = ((player.enemy.spec * 2) - 100) / 100
        enemy_poison_damage = ((int(player.enemy.poison_damage) * 2) - 40) / 40

        out = np.array([health, spec, poison_damage, frozen, enemy_health, enemy_spec, enemy_poison_damage])
        out = np.append(out, self.legal_actions)
        return out

    
    def is_legal(self, action):
        # check if action which is a string from weapons_lst, is legal
        player = self.get_current_player()

        # get list of weapons that player can use based on state of game
        # most importantly, being frozen restricts to ranged weapons and some weapons require spec
        available_weapons = player.available_weapons()
        if not type(action) == str:
            action = WEAPON_LST[action]

        if action in available_weapons:           
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
    
    @property
    def available_weapon_indices(self):
        # get list of weapons that player can use based on state of game
        # this is a list of 1s and 0s, where 1s are legal weapons
        # each index corresponds to a weapon in WEAPON_LST
        legal_actions = self.legal_actions

        weapons_dict = {}
        for i in range(len(legal_actions)):
            if legal_actions[i] == 1:
                weapons_dict[WEAPON_LST[i]] = i
        return weapons_dict

    
    def get_current_player(self):
        return self.players[self.current_player_num]


    def get_enemy(self):
        return self.players[(1 - self.current_player_num) % 2]


    def check_game_over(self):
        defender = self.get_enemy()
        if defender.health <= 0:
            return 1, True
        return 0, False #-0.01 here to encourage choosing the win?


    @property
    def current_player(self):
        return self.players[self.current_player_num]

    def step(self, action):
        # action should be a number between 0 and self.action_space.n, an integer

        # reward is 
        reward = [0,0]
        done = False
        
        player = self.get_current_player()
        enemy = self.get_enemy()

        weapon = WEAPON_LST[action] # action is index of list of strings

        # check if action is legal, based on string name of weapon
        if not self.is_legal(action): 
            done = True
            # 1 point to the winner, -1 to the loser(cheater)
            reward = [1,1]
            reward[self.current_player_num] = -1
        else:
            # get weapon class
            weapon_cls = player.get_weapon(weapon)
            
            # apply damage, health, etc
            weapon_cls.attack(player, enemy)

            print('Bot Health', self.players[0].health)
            print('Player Health', self.players[1].health)

            self.turns_taken += 1

            r, done = self.check_game_over()

            # if done, reward is 1 for the winner, -1 for the loser
            # if not done, reward is 0 for both
            reward = [-r,-r]
            reward[self.current_player_num] = r

        self.done = done

        if not done:
            self.current_player_num = (self.current_player_num + 1) % 2

        return self.observation, reward, done, {}

    def reset(self):
        self.players = [Player(name='Bot'), Player(name='Player')]
        self.players[0].enemy = self.players[1]
        self.players[1].enemy = self.players[0]
        self.current_player_num = 0
        self.turns_taken = 0
        self.done = False
        logger.debug(f'\n\n---- NEW GAME ----')
        return self.observation


    def render(self, mode='human', close=False):
        logger.debug('')
        if close:
            return
        if self.done:
            logger.debug(f'GAME OVER')
        else:
            logger.debug(f"It is Player {self.current_player.name}'s turn to move")

        if self.verbose:
            logger.debug(f'\nObservation: \n{self.observation}')
        
        if not self.done:
            print(f'\nLegal actions: {self.available_weapon_indices}')
            