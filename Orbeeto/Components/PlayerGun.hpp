#pragma once
#include "Component.hpp"


struct PlayerGun : Component {
	uint32_t owner;  // Pointer to player entity
	bool isLeft = true;  // Is this gun on Orbeeto's left? Left if true; right if false

	uint64_t lastShot = 0;
	int cooldown = 250; // The base rate at which the gun fires bullets

	int bulletId = BulletType::STANDARD;  // The ID of the bullet the gun will fire

	float heatDissipation = 100.0f;
};