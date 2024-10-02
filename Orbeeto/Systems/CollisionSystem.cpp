#include "CollisionSystem.hpp"
#include "../Components/AccelTransform.hpp"
#include "../Components/Collision.hpp"
#include <iostream>


void CollisionSystem::init(Coordinator* coord) {
	coordinator = coord;
}

const Entity* CollisionSystem::checkCollision(const Entity& refEntity) {
	const Entity* output = nullptr;
	for (const auto& entity : mEntities) {
		//if (entity == refEntity) continue;

		output = &entity;
	}
	return output;
}

void CollisionSystem::update() {
	for (const auto& entity : mEntities) {
		auto& accelTransform = coordinator->getComponent<AccelTransform>(entity);
		auto& collision = coordinator->getComponent<Collision>(entity);

		// Assign hitbox to sprite center
		collision.hitPos.x = accelTransform.pos.x;
		collision.hitPos.y = accelTransform.pos.y;

		this->checkCollision(entity);
	}
}