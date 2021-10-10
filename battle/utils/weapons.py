import random
import inspect

RANGED = "ranged"
MELEE = "melee"

WEAPON_LST = [
    "guth",
    "punch",
    "blood",
    "maul",
    "korasi",
    "dbow",
    "dbolt",
    "smoke",
    "ice",
    "sgs",
    "dds",
    "msb",
    "dclaws",
    "ags",
    "onyx",
    "zgs",
    "surge",
    "storm",
]


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

    def set_percentile(self):
        self.percentile = random.randint(0, 100)

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
        return (
            fighter.spec >= self.spec
            and (not fighter.frozen or self.type == RANGED)
            and (fighter.health < self.hp_restriction)
        )

    def attack(self, attacker, defender):
        # refresh percentile and caluclate damage
        self.set_percentile()
        # get damage
        damage = self.calc_damage()

        # apply damage
        defender.take_damage(damage)

        attack_log = "{} attacks {} with {} for {} damage.".format(
            attacker.name, defender.name, self.__class__.__name__, damage
        )

        # apply poison state
        if self.poisoned():
            defender.poisoned = True
            defender.poison_damage = 40

        if defender.poisoned:
            # apply poison damage
            defender.take_damage(defender.poison_damage)
            attack_log += (
                " "
                + defender.name
                + " suffers "
                + str(defender.poison_damage)
                + " from poison."
            )

            # update or reset poison damage
            if defender.poison_damage == 32:
                defender.poison_damage = 0
                defender.poisoned = False
            else:
                defender.poison_damage -= 2

        # get heal
        heal = self.calc_heal()
        if self.healing:
            if heal == 0:
                attack_log += " Healing failed."
            else:
                attack_log += " {} heals {} for health.".format(attacker.name, heal)

        # apply heal
        attacker.take_heal(heal)

        # apply spec reduction
        attacker.apply_spec_reduction(self.spec)

        return attack_log


class Guth(Weapon):
    def __init__(self):
        super().__init__()
        self.type = MELEE
        self.healing = True

    def calc_damage(self):
        percentile = self.percentile
        if percentile <= 20:
            damage = random.randint(1, 149)
        elif percentile <= 81:
            damage = random.randint(150, 275)
        else:
            damage = random.randint(276, 320)
        self.damage_dealt = damage
        return damage

    def calc_heal(self):
        heal_chance = random.randint(1, 10)
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
            damage = random.randint(1, 125)
        else:
            damage = random.randint(126, 225)
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
            damage = random.randint(1, 100)
        elif percentile <= 81:
            damage = random.randint(101, 280)
        else:
            damage = random.randint(281, 330)
        self.damage_dealt = damage
        return damage

    def calc_heal(self):
        heal = int(self.damage_dealt * 0.4)
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
            damage = random.randint(250, 375)
        elif percentile <= 74:
            damage = random.randint(376, 600)
        else:
            damage = random.randint(601, 750)
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
            damage = random.randint(1, 350)
        elif percentile <= 71:
            damage = random.randint(351, 650)
        else:
            damage = random.randint(651, 710)
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
            damage = random.randint(100, 220) + random.randint(100, 220)
        elif percentile <= 70:
            damage = random.randint(221, 300) + random.randint(221, 300)
        else:
            damage = random.randint(301, 350) + random.randint(301, 350)
        self.damage_dealt = damage
        return damage


class Dbolt(Weapon):
    def __init__(self):
        super().__init__()
        self.type = RANGED

    def calc_damage(self):
        percentile = self.percentile
        if percentile <= 12:
            damage = random.randint(1, 175)
        elif percentile <= 80:
            damage = random.randint(176, 374)
        else:
            damage = random.randint(375, 600)
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
            damage = random.randint(1, 200)
        elif percentile <= 70:
            damage = random.randint(201, 300)
        else:
            damage = random.randint(301, 350)
        self.damage_dealt = damage
        return damage

    def poisoned(self):
        poison_chance = random.randint(1, 10)
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
            damage = random.randint(1, 100)
        elif percentile <= 81:
            damage = random.randint(101, 250)
        else:
            damage = random.randint(251, 330)
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
            damage = random.randint(50, 200)
        elif percentile <= 70:
            damage = random.randint(201, 350)
        else:
            damage = random.randint(351, 450)
        self.damage_dealt = damage
        return damage

    def calc_heal(self):
        heal = int(self.damage_dealt * 0.5)
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
            damage = random.randint(1, 100) + random.randint(1, 100)
        elif percentile <= 71:
            damage = random.randint(101, 175) + random.randint(101, 175)
        else:
            damage = random.randint(176, 230) + random.randint(176, 230)
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
            damage = random.randint(75, 150) + random.randint(75, 150)
        elif percentile <= 81:
            damage = random.randint(151, 230) + random.randint(151, 230)
        else:
            damage = random.randint(231, 300) + random.randint(231, 300)
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
            damage = (
                random.randint(1, 50)
                + random.randint(1, 50)
                + random.randint(1, 50)
                + random.randint(1, 50)
            )
        else:
            damage = (
                random.randint(51, 140)
                + random.randint(51, 140)
                + random.randint(51, 140)
                + random.randint(51, 140)
            )
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
            damage = random.randint(150, 200)
        elif percentile <= 61:
            damage = random.randint(201, 400)
        else:
            damage = random.randint(401, 510)
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
            damage = random.randint(1, 125)
        elif percentile <= 61:
            damage = random.randint(126, 275)
        else:
            damage = random.randint(276, 375)
        self.damage_dealt = damage
        return damage

    def calc_heal(self):
        heal_chance = random.randint(1, 10)
        if heal_chance <= 5:
            heal = int(self.damage_dealt * 0.5)
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
            damage = random.randint(1, 220)
        elif percentile <= 81:
            damage = random.randint(221, 330)
        else:
            damage = random.randint(331, 420)
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
            damage = random.randint(200, 350)
        else:
            damage = random.randint(351, 500)
        self.damage_dealt = damage
        return damage


class Storm(Weapon):
    def __init__(self):
        super().__init__()
        self.type = RANGED

    def calc_damage(self):
        percentile = self.percentile
        damage = random.randint(100, 330)
        self.damage_dealt = damage
        return damage


class Toenail(Weapon):
    def __init__(self):
        super().__init__()
        self.type = RANGED

    def calc_damage(self):
        damage = random.randint(1, 1000)
        self.damage_dealt = damage
        return damage
