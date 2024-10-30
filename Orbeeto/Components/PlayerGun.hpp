#pragma once
#include "Component.hpp"


struct PlayerGun : Component {
	float cooldown;  // The base rate at which the gun fires bullets
	float heatDissipation;  // 
};