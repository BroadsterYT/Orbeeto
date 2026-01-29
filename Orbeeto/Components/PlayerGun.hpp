#pragma once
#include "Component.hpp"


struct PlayerGun : Component {
	Entity owner = 0;  // Player entity
	bool isLeft = true;  // Is this gun on Orbeeto's left? Left if true; right if false

	float shotBuildup = 60.0f;  /// The time since the last shot was fired
	float cooldown = 0.10f; // The base rate at which the gun fires bullets

	BulletType bulletId = BulletType::STANDARD;  // The ID of the bullet the gun will fire

	float heatDissipation = 100.0f;
};