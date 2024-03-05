"""
Module containing all materials and material-related content.
"""

# Dictionary of all materials in the game
MATERIALS = {
    0: 'metal_scrap_000',
    1: 'bolt_001',
    2: 'placeholder_002',
    3: 'placeholder_003',
    4: 'placeholder_004',
    5: 'placeholder_005',
    6: 'placeholder_006',
    7: 'placeholder_007',
    8: 'placeholder_008',
    9: 'placeholder_009',
    10: 'placeholder_010',
    11: 'placeholder_011',
    12: 'placeholder_012',
    13: 'placeholder_013',
    14: 'placeholder_014',
    15: 'placeholder_015',
    16: 'placeholder_016',
    17: 'placeholder_017',
    18: 'placeholder_018',
    19: 'placeholder_019',
    20: 'placeholder_020',
    21: 'placeholder_021',
    22: 'placeholder_022',
    23: 'placeholder_023',
    24: 'placeholder_024',
}

ENEMY_LOOT_TABLES = {
    0: [[(MATERIALS[0],), (MATERIALS[0],), (MATERIALS[0],), ],  # Standard Grunt
        [(MATERIALS[0],), (MATERIALS[0],), (MATERIALS[0], MATERIALS[0]), ],
        [(MATERIALS[0],), (MATERIALS[0], MATERIALS[0],), (MATERIALS[0], MATERIALS[0],), ], ],

    1: [[(MATERIALS[0],), (MATERIALS[0],), (MATERIALS[1],), ],  # Octo grunt
        [(MATERIALS[0],), (MATERIALS[0],), (MATERIALS[1],), ],
        [(MATERIALS[1],), (MATERIALS[0], MATERIALS[1],), (MATERIALS[1], MATERIALS[1],), ], ],

    2: [[(MATERIALS[0],), (MATERIALS[1],), (MATERIALS[1],), ],  # Ambusher
        [(MATERIALS[1],), (MATERIALS[0], MATERIALS[1],), (MATERIALS[0], MATERIALS[1],), ],
        [(MATERIALS[0],), (MATERIALS[1], MATERIALS[1],), (MATERIALS[0], MATERIALS[1], MATERIALS[1]), ], ],
}
