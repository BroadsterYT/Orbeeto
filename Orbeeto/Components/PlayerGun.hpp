#pragma once
#include "Component.hpp"


struct PlayerGun : Component {
	uint32_t* owner;  // Pointer to player entity
	bool isLeft = true;  // Is this gun on Orbeeto's left? Left if true; right if false

	int maxCooldown = 500;  // The base rate at which the gun fires bullets
	int cooldown = 500;

	int bulletId = 0;  // The ID of the bullet the gun will fire

	float heatDissipation = 100.0f;
};