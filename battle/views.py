from django.http.response import JsonResponse
from django.shortcuts import render
from battle.utils.fight import Fighter
from battle.utils.weapons import *
from stable_baselines import PPO1
import numpy as np
from battle.models import Player

ppo_model = PPO1.load("zoo/deathmatch/best_model.zip", env=None)
# Create your views here.


def home(request):
    return render(request, "home.html")


def battle(request):
    players = Player.objects.all()
    # aggregate all wins of all players
    total_wins = sum([player.wins for player in players])
    total_losses = sum([player.losses for player in players])

    context = {
        "players": players,
        "total_wins": total_wins,
        "total_losses": total_losses,
    }
    return render(request, "battle.html", context)


def get_player(request):
    if request.method == "POST":
        name = request.POST["name"]
        player, created = Player.objects.get_or_create(name=name)
        request.session["player"] = player.name
        return JsonResponse(
            {"personal_wins": player.wins, "personal_losses": player.losses}
        )


def update_stats(request):
    if request.method == "POST":
        # get player from name
        player = Player.objects.get(name=request.POST["name"])
        # update stats
        print(request.POST)
        if request.POST["win"] == "true":
            player.wins += 1
        else:
            player.losses += 1
        player.save()
        total_wins = sum([player.wins for player in Player.objects.all()])
        total_losses = sum([player.losses for player in Player.objects.all()])
        print("totalwins", total_wins)
        print("totallosses", total_losses)
        return JsonResponse(
            {
                "total_wins": total_wins,
                "total_losses": total_losses,
                "personal_wins": player.wins,
                "personal_losses": player.losses,
            }
        )


def start_battle(request):
    player = fighter_from_stats(
        health=1500,
        spec=100,
        frozen=False,
        poison_damage=0,
        name=request.session.get("player"),
    )

    enemy = fighter_from_stats(
        health=1500, spec=100, frozen=False, poison_damage=0, name="Bot"
    )
    player.enemy = enemy
    enemy.enemy = player

    # get prediction from PPO model
    choice = ppo_prediction(enemy)
    weapon = WEAPON_LST[choice[0]]

    enemy.select_weapon(weapon)

    enemy_attack_log = enemy.attack()

    # recommend weapon for player
    choice = ppo_prediction(player)
    recommended_weapon = WEAPON_LST[choice[0]]
    
    return JsonResponse(
        {
            "health_player": player.health,
            "health_enemy": enemy.health,
            "spec_player": player.spec,
            "spec_enemy": enemy.spec,
            "poison_damage_player": player.poison_damage,
            "poison_damage_enemy": enemy.poison_damage,
            "frozen_player": int(player.frozen),
            "frozen_enemy": int(enemy.frozen),
            "enemy_attack_log": enemy_attack_log,
            "recommended_weapon": recommended_weapon,
        }
    )


def attack(request):
    if request.method == "POST":
        # get selected weapon
        weapon = request.POST["weapon"].lower()

        # get weapon object

        # if weapon illegal, return error
        health_player = int(request.POST["health_player"])
        health_enemy = int(request.POST["health_enemy"])
        spec_player = int(request.POST["spec_player"])
        spec_enemy = int(request.POST["spec_enemy"])
        poison_damage_player = int(request.POST["poison_damage_player"])
        poison_damage_enemy = int(request.POST["poison_damage_enemy"])
        frozen_player = bool(int(request.POST["frozen_player"]))
        frozen_enemy = bool(int(request.POST["frozen_enemy"]))

        player = fighter_from_stats(
            health_player,
            spec_player,
            frozen_player,
            poison_damage_player,
            name="Player",
        )
        player.select_weapon(weapon)
        # check if weapon is legal
        legal_weapon = player.is_legal(weapon)
        if not legal_weapon:
            # get reason for illegal weapon
            reason = player.illegal_reason
            print(reason)
            return JsonResponse({"error": reason})

        enemy = fighter_from_stats(
            health_enemy, spec_enemy, frozen_enemy, poison_damage_enemy, name="Bot"
        )
        player.enemy = enemy
        enemy.enemy = player
        player_attack_log = player.attack()
        health_player_before_attack = player.health

        if enemy.health <= 0:
            enemy_attack_log = "Enemy has been defeated, you win!"

        else:
            # get prediction from PPO model
            choice = ppo_prediction(enemy)
            weapon = WEAPON_LST[choice[0]]
            enemy.select_weapon(weapon)
            enemy_attack_log = enemy.attack()

        if player.health <= 0:
            player_attack_log = "You have been defeated, you lose!"
        
        # get recommendation for next move
        choice = ppo_prediction(player)
        recommended_weapon = WEAPON_LST[choice[0]]
        

    return JsonResponse(
        {
            "health_player": player.health,
            "health_enemy": enemy.health,
            "spec_player": player.spec,
            "spec_enemy": enemy.spec,
            "poison_damage_player": player.poison_damage,
            "poison_damage_enemy": enemy.poison_damage,
            "frozen_player": int(player.frozen),
            "frozen_enemy": int(enemy.frozen),
            "enemy_attack_log": enemy_attack_log,
            "player_attack_log": player_attack_log,
            "health_player_before_attack": health_player_before_attack,
            "recommended_weapon": recommended_weapon,
        }
    )


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

    out = np.array(
        [
            health,
            spec,
            poison_damage,
            frozen,
            enemy_health,
            enemy_spec,
            enemy_poison_damage,
        ]
    )
    obs = np.append(out, player.legal_actions)
    return ppo_model.predict(obs)
