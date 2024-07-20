"""
Module containing all materials and material-related content.
"""


# Dictionary of all materials in the game
MATERIALS = [
    'metal_scrap_000',
    'bolt_001',
    'placeholder_002',
    'placeholder_003',
    'placeholder_004',
    'placeholder_005',
    'placeholder_006',
    'placeholder_007',
    'placeholder_008',
    'placeholder_009',
    'placeholder_010',
    'placeholder_011',
    'placeholder_012',
    'placeholder_013',
    'placeholder_014',
    'placeholder_015',
    'placeholder_016',
    'placeholder_017',
    'placeholder_018',
    'placeholder_019',
    'placeholder_020',
    'placeholder_021',
    'placeholder_022',
    'placeholder_023',
    'placeholder_024',
]

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
