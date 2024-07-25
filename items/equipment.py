"""
Module containing all armor, weapons, and accessories.
"""


class ArmorData:
    """A data class for features of armor sets"""
    def __init__(self, name: str, hp_mod: int = 0, def_mod: int = 0, ammo_mod: int = 0):
        """A data class for the modifications an armor set has on the player

        :param name: The name of the armor set
        :param hp_mod: The value to modify maximum HP by. 0 by default.
        :param def_mod: The value to modify maximum defense by. 0 by default.
        :param ammo_mod: The value ot modify maximum ammo by. 0 by default.
        """
        self.name = name
        self.hp_mod = hp_mod
        self.def_mod = def_mod
        self.ammo_mod = ammo_mod

    def __repr__(self):
        return f'ArmorData({self.name}, {self.hp_mod}, {self.def_mod}, {self.ammo_mod})'


ARMOR = {
    0: ArmorData('standard_A000'),
    1: ArmorData('placeholder_A001', hp_mod=10),
    2: ArmorData('placeholder_A002'),
}

WEAPONS = {
    0: 'standard_L000',
    1: 'standard_R000',
    2: 'laser_L001',
    3: 'laser_R001',
}
