#pragma once
#include "Component.hpp"


struct PlayerGun : Component {
	Entity owner = 0;  // Player entity
	bool isLeft = true;  // Is this gun on Orbeeto's left? Left if true; right if false

	float shotBuildup = 60.0f;  /// The time since the last shot was fired
	float cooldown = 0.10f; // The base rate at which the gun fires bullets

	BulletType bulletId = BulletType::STANDARD;  // The ID of the bullet the gun will fire

	float heatDissipation = 100.0f;


	void serialize(std::ofstream& out) override {
		uint32_t rawId = static_cast<uint32_t>(bulletId);
		SerialHelper::serialize(out, &rawId);

		SerialHelper::serialize(out, &owner, &isLeft, &shotBuildup, &cooldown, &heatDissipation);
	}

	void deserialize(std::ifstream& in) override {
		uint32_t rawId;
		SerialHelper::deserialize(in, &rawId);
		bulletId = static_cast<BulletType>(rawId);

		SerialHelper::deserialize(in, &owner, &isLeft, &shotBuildup, &cooldown, &heatDissipation);
	}
};