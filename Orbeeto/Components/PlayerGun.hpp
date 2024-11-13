#pragma once
#include "Component.hpp"


struct PlayerGun : Component {
	uint32_t* owner;  // Pointer to player entity
	float cooldown;  // The base rate at which the gun fires bullets
	float heatDissipation;
};