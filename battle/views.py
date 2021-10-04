from django.http.response import JsonResponse
from django.shortcuts import render
from battle.utils.fight import Fighter
from battle.utils.weapons import *
from stable_baselines import PPO1
import numpy as np

ppo_model = PPO1.load("zoo/deathmatch/best_model.zip", env=None)
# Create your views here.

def home(request):
    return render(request, 'home.html')

def battle(request):
    return render(request, 'battle.html')

def start_battle(request):
    player = fighter_from_stats(health=1500, spec=100, frozen=False, poison_damage=0, name="Player")

    enemy = fighter_from_stats(health=1500, spec=100, frozen=False, poison_damage=0, name="Bot")
    player.enemy = enemy
    enemy.enemy = player

    # get prediction from PPO model
    choice = ppo_prediction(enemy)
    weapon = WEAPON_LST[choice[0]]

    enemy.select_weapon(weapon)

    enemy_attack_log = enemy.attack()
    return JsonResponse({'health_player': player.health, 'health_enemy': enemy.health, 'spec_player': player.spec, 'spec_enemy': enemy.spec, 'poison_damage_player': player.poison_damage, 'poison_damage_enemy': enemy.poison_damage, 'frozen_player': int(player.frozen), 'frozen_enemy': int(enemy.frozen), 'enemy_attack_log': enemy_attack_log})


def attack(request):
    if request.method == 'POST':
        print(request.POST)
        # get selected weapon
        weapon = request.POST['weapon'].lower()

        # get weapon object

        # if weapon illegal, return error
        health_player = int(request.POST['health_player'])
        health_enemy = int(request.POST['health_enemy'])
        spec_player = int(request.POST['spec_player'])
        spec_enemy = int(request.POST['spec_enemy'])
        poison_damage_player = int(request.POST['poison_damage_player'])
        poison_damage_enemy = int(request.POST['poison_damage_enemy'])
        frozen_player = bool(int(request.POST['frozen_player']))
        frozen_enemy = bool(int(request.POST['frozen_enemy']))

        player = fighter_from_stats(health_player, spec_player, frozen_player, poison_damage_player, name="Player")
        player.select_weapon(weapon)
        # check if weapon is legal
        legal_weapon = player.is_legal(weapon)
        if not legal_weapon:
            return JsonResponse({'error': 'Illegal weapon'})

        enemy = fighter_from_stats(health_enemy, spec_enemy, frozen_enemy, poison_damage_enemy, name="Bot")
        player.enemy = enemy
        enemy.enemy = player
        player_attack_log = player.attack()

        if enemy.health <= 0:
            enemy_attack_log = 'Enemy has been defeated, you win!'
            
        else:
            # get prediction from PPO model
            choice = ppo_prediction(enemy)
            weapon = WEAPON_LST[choice[0]]
            enemy.select_weapon(weapon)
            enemy_attack_log = enemy.attack()
        
        if player.health <= 0:
            player_attack_log = 'You have been defeated, you lose!'

    return JsonResponse({'health_player': player.health, 'health_enemy': enemy.health, 'spec_player': player.spec, 'spec_enemy': enemy.spec, 'poison_damage_player': player.poison_damage, 'poison_damage_enemy': enemy.poison_damage, 'frozen_player': int(player.frozen), 'frozen_enemy': int(enemy.frozen), 'enemy_attack_log': enemy_attack_log, 'player_attack_log': player_attack_log})


def fighter_from_stats(health, spec, frozen, poison_damage, name):
    # create player object
    fighter = Fighter(name=name)
    fighter.health = health
    fighter.spec = spec
    fighter.frozen = frozen
    fighter.poison_damage = poison_damage
    if poison_damage > 0:
        fighter.poisoned = True

    return fighter


def ppo_prediction(player):
    """
    get model prediction from environment
    """
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
    obs = np.append(out, player.legal_actions)
    return ppo_model.predict(obs)

