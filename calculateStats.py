import math

xpToReach = []
xpRequired = []

def loadXpRequirements():
    # Find difference between current level's xp and previous
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

def updateLevel(selfEntity):
    for i in range(250):
        if selfEntity.xp < xpRequired[i + 1]:
            selfEntity.level = i
            break
        if selfEntity.xp > xpRequired[249]:
            selfEntity.level = 249
            break