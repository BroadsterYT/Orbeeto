import math

def loadPlayerXpReq():
    """Loads a list of the xp amounts needed for each player level.
    
    ### Returns
        - ``list``: A list containing the xp amounts needed to reach each level
    """    
    # Find difference between current level's xp and previous
    xpToReach = []
    xpRequired = []

    for a in range(250):
        if a < 125:
            value = math.floor(17.84 * a)
        else:
            value = math.floor(pow(1.061726202, a))
        xpToReach.append(value)
    for b in range(250):
        countup = 0
        total = 0
        while countup <= b:
            total = total + xpToReach[countup]
            countup += 1
        xpRequired.append(total)

    return xpRequired

def updatePlayerLevel(any_player):
    """Updates the level of a player sprite.
    
    ### Parameters
        - ``any_player`` ``(pygame.sprite.Sprite)``: The player whose level should be updated
    """    
    xpRequired = loadPlayerXpReq()
    for i in range(250):
        if any_player.xp < xpRequired[i + 1]:
            any_player.level = i
            break
        if any_player.xp > xpRequired[249]:
            any_player.level = 249
            break