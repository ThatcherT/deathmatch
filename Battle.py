import random
import numpy as np
import math
class fighter:
    pass
class attacks:
    def punch():
        percentile = random.randint(1,100)
        if percentile <= 20:
            hit = random.randint(1,125)
        else:
            hit = random.randint(126,225)
        spec = 0
        heal = 0
        return [percentile, hit, spec, heal]
    def guth():
        percentile = random.randint(1,100)
        if percentile <= 20:
            hit = random.randint(1,149)
        elif percentile <= 81:
            hit = random.randint(150,275)
        else:
            hit = random.randint(276,320)

        heal_chance = random.randint(1,10)
        if heal_chance <= 4:
            heal = hit
        else:
            heal = 0
        total = heal + hit
        spec = 0
        return [percentile, hit, spec, heal]
    def blood():
        percentile = random.randint(1,100)
        if percentile <= 20:
            hit = random.randint(1,100)
        elif percentile <= 81:
            hit = random.randint(101,280)
        else:
            hit = random.randint(281,330)

        heal = hit*.4
        total = heal + hit
        spec = 0
        return [percentile, hit, spec, heal]
    def maul():
        percentile = random.randint(1,100)
        if percentile <= 13:
            hit = random.randint(250,375)
        elif percentile <= 74:
            hit = random.randint(376,600)
        else:
            hit = random.randint(601,750)
        spec = 100
        heal = 0
        return [percentile, hit, spec, heal]
    def korasi():
        percentile = random.randint(1,100)
        if percentile <= 10:
            hit = random.randint(1,350)
        elif percentile <= 71:
            hit = random.randint(351,650)
        else:
            hit = random.randint(651,710)
        spec = 75
        heal = 0
        return [percentile, hit, spec, heal]
    def dbow():
        percentile = random.randint(1,100)
        if percentile <= 15:
            hit = random.randint(100,220) + random.randint(100,220)
        elif percentile <= 70:
            hit = random.randint(221,300) + random.randint(221,300)
        else:
            hit = random.randint(301,350) + random.randint(301,350)
        spec = 75
        heal = 0
        return [percentile, hit, spec, heal]
    def dbolt():
        percentile = random.randint(1,100)
        if percentile <= 12:
            hit = random.randint(1,175)
        elif percentile <= 80:
            hit = random.randint(176,374)
        else:
            hit = random.randint(375,600)
        spec = 0
        heal = 0
        return [percentile, hit, spec, heal]
    def smoke():
        percentile = random.randint(1,100)
        if percentile <= 20:
            hit = random.randint(1,200)
        elif percentile <= 70:
            hit = random.randint(201,300)
        else:
            hit = random.randint(301,350)
        poison_chance = random.randint(1,10)
        if poison_chance <= 7:
            poison = True
        else:
            poison = False
    #     if poison is True:
    #         hit += 40
        spec = 0
        heal = 0
        return [percentile, hit, spec, heal, poison]
    def ice():
        percentile = random.randint(1,100)
        if percentile <= 20:
            hit = random.randint(1,100)
        elif percentile <= 81:
            hit = random.randint(101,250)
        else:
            hit = random.randint(251,330)
        spec = 0
        heal = 0
        return [percentile, hit, spec, heal]
    def sgs():
        percentile = random.randint(1,100)
        if percentile <= 15:
            hit = random.randint(50,200)
        elif percentile <= 70:
            hit = random.randint(201,350)
        else:
            hit = random.randint(351,450)

        heal = hit*.5
        total = heal + hit
        spec = 50
        return [percentile, hit, spec, heal]
    def dds():
        percentile = random.randint(1,100)
        if percentile <= 20:
            hit = random.randint(1,100) + random.randint(1,100)
        elif percentile <= 71:
            hit = random.randint(101,175) + random.randint(101,175)
        else:
            hit = random.randint(176,230) + random.randint(176,230)
        spec = 25
        heal = 0
        return [percentile, hit, spec, heal]
    def msb():
        percentile = random.randint(1,100)
        if percentile <= 20:
            hit = random.randint(75,150) + random.randint(75,150)
        elif percentile <= 81:
            hit = random.randint(151,230) + random.randint(151,230)
        else:
            hit = random.randint(231,300) + random.randint(231,300)
        spec = 50
        heal = 0
        return [percentile, hit, spec, heal]
    def dclaws():
        percentile = random.randint(1,100)
        if percentile <= 20:
            hit = random.randint(1,50) + random.randint(1,50) + random.randint(1,50) + random.randint(1,50)
        elif percentile <= 100:
            hit = random.randint(51,140) + random.randint(51,140) + random.randint(51,140)+ random.randint(51,140)
        spec = 50
        heal = 0
        return [percentile, hit, spec, heal]
    def ags():
        percentile = random.randint(1,100)
        if percentile <= 20:
            hit = random.randint(150,200)
        elif percentile <= 61:
            hit = random.randint(201,400)
        else:
            hit = random.randint(401,510)
        spec = 50
        heal = 0
        return [percentile, hit, spec, heal]
    def onyx():
        percentile = random.randint(1,100)
        if percentile <= 20:
            hit = random.randint(1,125)
        elif percentile <= 61:
            hit = random.randint(126,275)
        else:
            hit = random.randint(276,375)
        heal_chance = random.randint(1,10)
        if heal_chance <=5:
            heal = hit*.5
        else:
            heal = 0
        total = heal + hit
        spec = 0
        return [percentile, hit, spec, heal]
    def zgs():
        percentile = random.randint(1,100)
        if percentile <= 20:
            hit = random.randint(1,220)
        elif percentile <= 81:
            hit = random.randint(221,330)
        else:
            hit = random.randint(331,420)
        spec = 50
        heal = 0
        return [percentile, hit, spec, heal]
    def surge():
        percentile = random.randint(1,100)
        if percentile <= 40:
            hit = random.randint(200,350)
        else:
            hit = random.randint(351,500)
        spec = 0
        heal = 0
        #hp must be less than 200
        return [percentile, hit, spec, heal]
    def storm():
        hit = random.randint(100,330)
        percentile = math.ceil(((hit-100)/230)*100)
        spec = 0
        heal = 0
        return [percentile, hit, spec, heal]
    def poly():
        percentile = random.randint(1,100)
        if percentile <= 40:
            hit = random.randint(1,300)
        else:
            hit = random.randint(301,750)
        spec = 0
        heal = 0
        return [percentile, hit, spec, heal]
    def whip():
        percentile = random.randint(1,100)
        if percentile <= 40:
            hit = random.randint(1,225)
        else:
            hit = random.randint(226,350)
        spec = 0
        heal = 0
        return [percentile, hit, spec, heal]
def takedamage(fighter, hit):
    fighter.health -= hit
    return fighter.health
def fight():
    p1 = fighter()
    p2 = fighter()
    p1.health = 1500
    p2.health = 1500
    p1.spec = 100
    p2.spec = 100
    p1.poison = 0
    p2.poison = 0
    p1.frozen = False
    p2.frozen = False
    print('Starting a DM between P1 and P2 for 50m bet on 07 - Go Fight now.')
    print('P1 gets the first hit!')
    while True:
        while True:
            p1_attack = str(input("\nP1: Select an attack: "))
            if p1.frozen == True:
                weapons = ['blood', 'onyx', 'dbolt', 'msb', 'dbow','ice']
            else:
                weapons = ['guth', 'ags', 'sgs', 'poly', 'whip', 'dbolt', 'dclaws', 'korasi', 'storm', 'blood', 'smoke', 'dds', 'ice', 'punch', 'zgs', 'maul', 'dh', 'dbow', 'onyx', 'msb', 'surge']
            if not p1_attack in weapons:
                continue
            elif p1_attack == 'dh' and p1.frozen == False:
                break
            else:
                hit = getattr(attacks, p1_attack)()
                if hit[2] > p1.spec:
                    continue
                elif p1_attack == 'surge' and p1.health > 250:
                    continue
                else:
                    break
        if p1_attack == 'dh' and p1.frozen == False:
            if p1.health >= 500:
                hit = random.randint(1, 350)
                p2.health -= hit
            elif p1.health >= 200:
                hit = random.randint(100,450)
                p2.health -= hit
            elif p1.health >= 100:
                hit = random.randint(175, 550)
                p2.health -= hit
            else:
                hit = random.randint(200,910)
                p2.health -= hit
            print('P1 casts at P2 with dh dealing', hit, 'damage.')
        else:
            hit = getattr(attacks, p1_attack)() #hit is percentile, damage, spec, heal
            if p1_attack == 'ice' or p1_attack == 'zgs':
                p2.frozen = True
            if p1_attack == 'smoke' and hit[4] == True:
                p2.poison = 40
            p1.spec -= hit[2]
            p2.health -= hit[1] + p2.poison
            if p2.poison >0:
                print('P2 suffers', p2.poison, 'damage from poison.')
            if hit[3] == 0:
                print('P1 casts at P2 with', hit[0], '% hit chance a', p1_attack, 'dealing', hit[1], 'damage.')
            elif hit[3] != 0:
                p1.health += hit[3]
                print('P1 casts at P2 with', hit[0], '% hit chance a', p1_attack, 'dealing', hit[1], 'damage, healing',
                      hit[3], '.')
        p2.poison -= 2
        if p2.poison < 30:
            p2.poison = 0
        if p1.health > 1500:
            pl.health = 1500
        if p2.health > 1500:
            p2.health = 1500
        if p1.health < 0:
            pl.health = 0
        if p2.health < 0:
            p2.health = 0
        p1.frozen = False
        print('P1 health:', p1.health, 'P2 health:', p2.health)
        if p2.health ==0:
            print('GG P1, P2 is dead')
            break
        while True:
            if p2.frozen == True:
                weapons = ['blood', 'onyx', 'dbolt', 'msb', 'dbow','ice']
            else:
                weapons = ['guth', 'ags', 'sgs', 'poly', 'whip', 'dbolt', 'dclaws', 'korasi', 'storm', 'blood', 'smoke', 'dds', 'ice', 'punch', 'zgs', 'maul', 'dh', 'dbow', 'onyx', 'msb', 'surge']
            p2_attack = str(input("\nP2: Select an attack: "))
            if not p2_attack in weapons:
                continue
            elif p2_attack == 'dh' and p2.frozen == False:
                break
            else:
                hit = getattr(attacks, p2_attack)()
                if hit[2] > p2.spec:
                    continue
                elif p2_attack == 'surge' and p2.health > 250:
                    continue
                else:
                    break
        if p2_attack == 'dh' and p2.frozen == False:
            if p2.health >= 500:
                hit = random.randint(1, 350)
                p1.health -= hit
            elif p2.health >= 200:
                hit = random.randint(100,450)
                p1.health -= hit
            elif p2.health >= 100:
                hit = random.randint(175, 550)
                p1.health -= hit
            else:
                hit = random.randint(200,910)
                p1.health -= hit
            print('P2 casts at P1 with dh dealing', hit, 'damage.')
        else:
            hit = getattr(attacks, p2_attack)()  # hit is percentile, damage, spec, heal
            if p2_attack == 'ice':
                p1.frozen = True
            if p2_attack == 'smoke' and hit[4] == True:
                p1.poison = 40
            p2.spec -= hit[2]
            p1.health -= hit[1] + p1.poison
            if p1.poison > 0:
                print('P1 suffers', p1.poison, 'damage from poison.')
            if hit[3] == 0:
                print('P2 casts at P1 with', hit[0], '% hit chance a', p2_attack, 'dealing', hit[1], 'damage.')
            elif hit[3] != 0:
                p2.health += hit[3]
                print('P2 casts at P1 with', hit[0], '% hit chance a', p2_attack, 'dealing', hit[1], 'damage, healing', hit[3],'.')
        p1.poison -= 2
        if p1.poison < 30:
            p1.poison = 0
        if p1.health > 1500:
            pl.health = 1500
        if p2.health > 1500:
            p2.health = 1500
        if p1.health < 0:
            p1.health = 0
        if p2.health < 0:
            p2.health = 0
        p2.frozen = False
        print('P1 health:', p1.health, 'P2 health:', p2.health)
        if p1.health ==0:
            print('GG P2, P1 is dead')
            break
    return

fight()