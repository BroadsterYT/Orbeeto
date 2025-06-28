#pragma once
#include "Component.hpp"


struct PlayerGun : Component {
	uint32_t owner = 0;  // Pointer to player entity
	bool isLeft = true;  // Is this gun on Orbeeto's left? Left if true; right if false

	float shotBuildup = 60.0f;  /// The time since the last shot was fired
	float cooldown = 1.0f; // The base rate at which the gun fires bullets

	int bulletId = BulletType::STANDARD;  // The ID of the bullet the gun will fire

	float heatDissipation = 100.0f;
};