#include "CollisionSystem.hpp"
#include "../Components/AccelTransform.hpp"
#include "../Components/Collision.hpp"
#include <iostream>


void CollisionSystem::init(Coordinator* coord) {
	coordinator = coord;
}

void CollisionSystem::update() {
	for (const auto& entity : mEntities) {
		auto& accelTransform = coordinator->getComponent<AccelTransform>(entity);
		auto& collision = coordinator->getComponent<Collision>(entity);

		// Assign hitbox to sprite center
		collision.hitPos.x = accelTransform.pos.x;
		collision.hitPos.y = accelTransform.pos.y;
		
		// Checking every collidable entity for a collision
		for (const auto& e : mEntities) {
			if (e == entity) continue;
			auto& eCollide = coordinator->getComponent<Collision>(e);

			if (collision.checkCollision(eCollide)) {
				std::cout << "Entity " << entity << " is colliding with Entity " << e << std::endl;
			}
		}
	}
}