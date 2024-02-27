"""
Package containing all projectile-related classes and functions.

├-- projectiles
    ├-- bulletbase.py \n
    ├-- enemy_bullets.py \n
    ├-- explosions.py \n
    ├-- player_bullets.py \n
"""
# __init__.py
from .bulletbase import BulletBase
from .enemy_bullets import *
from .explosions import *
from .player_bullets import *
