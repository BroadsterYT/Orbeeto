#pragma once
#include "Component.hpp"
#include "../TimeManip.hpp"


enum BulletType {
	STANDARD,
	HOMING
};


struct Bullet : Component {
	// ----- Required ----- //
	int bulletAI = BulletType::STANDARD;
	uint64_t birthTime = TimeManip::getTime();

	// ----- General ----- //
	int damage = 5;
	uint32_t shotBy = 0;  // The entity responsible for shooting this bullet

	// ----- Extra ----- //
	uint64_t lastHomingCheck = 0;  // The time at which the hast homing check was performed
	int homingRange = 128;  // The range that the bullet can begin homing into its target
	uint32_t closestTarget = 0;  // The entity to home towards
};