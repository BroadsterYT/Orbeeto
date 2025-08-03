#pragma once
#include "Component.hpp"


enum BulletType {
	STANDARD,
	HOMING
};


struct Bullet : Component {
	// ----- Required ----- //
	int bulletAI = BulletType::STANDARD;
	float lifeTime = 0.0f;

	// ----- General ----- //
	bool persistent = false; // Should the bullet disappear after a certain length of time?
	int damage = 5;
	uint32_t shotBy = 0;  // The entity responsible for shooting this bullet

	// ----- Extra ----- //
	uint64_t lastHomingCheck = 0;  // The time at which the hast homing check was performed
	int homingRange = 128;  // The range that the bullet can begin homing into its target
	uint32_t closestTarget = 0;  // The entity to home towards


	void serialize(std::ofstream& out) override {
		uint32_t rawAi = static_cast<uint32_t>(bulletAI);
		SerialHelper::serializeOne(out, &rawAi);
		
		SerialHelper::serialize(out, &lifeTime, &persistent, &damage, &shotBy, &lastHomingCheck, &homingRange, &closestTarget);
	}

	void deserialize(std::ifstream& in) override {
		uint32_t rawAi;
		SerialHelper::deserializeOne(in, &rawAi);
		bulletAI = static_cast<BulletType>(rawAi);

		SerialHelper::deserialize(in, &lifeTime, &persistent, &damage, &shotBy, &lastHomingCheck, &homingRange, &closestTarget);
	}

	void print() {
		std::cout << "BulletAI: " << bulletAI << std::endl;
		std::cout << "lifeTime: " << lifeTime << std::endl;
		std::cout << "Persistent: " << persistent << std::endl;
		std::cout << "Damage: " << damage << std::endl;
		std::cout << "ShotBy: " << shotBy << std::endl;
		std::cout << "lastHomingCheck: " << lastHomingCheck << std::endl;
		std::cout << "homingRange: " << homingRange << std::endl;
		std::cout << "closestTarget: " << closestTarget << std::endl;
	}
};