#pragma once
#include "Component.hpp"
#include "glaze/glaze.hpp"


enum class BulletType {
	STANDARD,
	HOMING
};

// TODO: Separate bullet struct into specialized components for each bullet
struct Bullet : Component {
	// ----- Required ----- //
	BulletType bulletAI = BulletType::STANDARD;
	float lifeTime = 0.0f;

	// ----- General ----- //
	bool persistent = false; // Should the bullet disappear after a certain length of time?
	int damage = 5;
	uint32_t shotBy = 0;  // The entity responsible for shooting this bullet

	// ----- Extra ----- //
	uint64_t lastHomingCheck = 0;  // The time at which the hast homing check was performed
	int homingRange = 128;  // The range that the bullet can begin homing into its target
	uint32_t closestTarget = 0;  // The entity to home towards
};


struct BulletData {
	BulletType bulletAI = BulletType::STANDARD;
	float lifeTime = 0.0f;

	bool persistent = false;
	int damage = 5;
	uint32_t shotBy = 0;

	uint64_t lastHomingCheck = 0;
	int homingRange = 128;
	uint32_t closestTarget = 0;
};

template <>
struct glz::meta<BulletData> {
	static constexpr auto value = glz::object(
		"bulletAI", &BulletData::bulletAI,
		"lifeTime", &BulletData::lifeTime,
		"persistent", &BulletData::persistent,
		"damage", &BulletData::damage,
		"shotBy", &BulletData::shotBy,
		"lastHomingCheck", &BulletData::lastHomingCheck,
		"homingRange", &BulletData::homingRange,
		"closestTarget", &BulletData::closestTarget
	);
};