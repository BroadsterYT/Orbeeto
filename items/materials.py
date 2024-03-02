"""
Module containing all materials and material-related content.
"""

# Dictionary of all materials in the game
MATERIALS = {
    0: 'm_metal_scrap_000',
    1: 'm_bolt_001',
    2: 'm_placeholder_002',
    3: 'm_placeholder_003',
    4: 'm_placeholder_004',
    5: 'm_placeholder_005',
    6: 'm_placeholder_006',
    7: 'm_placeholder_007',
    8: 'm_placeholder_008',
    9: 'm_placeholder_009',
    10: 'm_placeholder_010',
    11: 'm_placeholder_011',
    12: 'm_placeholder_012',
    13: 'm_placeholder_013',
    14: 'm_placeholder_014',
    15: 'm_placeholder_015',
    16: 'm_placeholder_016',
    17: 'm_placeholder_017',
    18: 'm_placeholder_018',
    19: 'm_placeholder_019',
    20: 'm_placeholder_020',
    21: 'm_placeholder_021',
    22: 'm_placeholder_022',
    23: 'm_placeholder_023',
    24: 'm_placeholder_024',
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
