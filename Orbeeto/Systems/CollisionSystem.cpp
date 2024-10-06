#include "CollisionSystem.hpp"
#include <iostream>


void CollisionSystem::init(Coordinator* coord) {
	coordinator = coord;
}

void CollisionSystem::pushCollision(Collision& coll1, AccelTransform& trans1, Collision& coll2, AccelTransform& trans2) {
	if (coll1.canBePushed != true && coll2.canPush == true) return;
	
	int side = coll1.intersection(coll2);

	if (side == 0
		&& (trans1.vel.y < 0 || trans2.vel.y > 0)
		&& trans1.pos.y <= trans2.pos.y + coll2.hitHeight / 2) {
		trans1.vel.y = 0;
		trans1.pos.y = trans2.pos.y + coll2.hitHeight / 2;
	}
	else if (side == 1 
		&& (trans1.vel.x < 0 || trans2.vel.x > 0)
		&& trans1.pos.x <= trans2.pos.x + coll2.hitWidth / 2) {
		trans1.vel.x = 0;
		trans1.pos.x = trans2.pos.x + coll2.hitWidth / 2;
	}
	else if (side == 2 
		&& (trans1.vel.y > 0 || trans2.vel.y < 0)
		&& trans1.pos.y >= trans2.pos.y - coll2.hitHeight / 2) {
		trans1.vel.y = 0;
		trans1.pos.y = trans2.pos.y - coll2.hitHeight / 2;
	}
	else if (side == 3 
		&& (trans1.vel.x > 0 || trans2.vel.x < 0)
		&& trans1.pos.x >= trans2.pos.x - coll2.hitWidth / 2) {
		trans1.vel.x = 0;
		trans1.pos.x = trans2.pos.x - coll2.hitWidth / 2;
	}
}

void CollisionSystem::update() {
	for (const auto& entity : mEntities) {
		auto& accelTransform = coordinator->getComponent<AccelTransform>(entity);
		auto& collision = coordinator->getComponent<Collision>(entity);

		// Assign hitbox to entity center
		collision.hitPos = accelTransform.pos;
		
		// Checking every collidable entity for a collision
		// TODO: First check if entity should move if collided with
		for (const auto& e : mEntities) {
			if (e == entity) continue;
			auto& eCollide = coordinator->getComponent<Collision>(e);

			if (collision.checkCollision(eCollide)) {
				auto& eTransform = coordinator->getComponent<AccelTransform>(e);
				this->pushCollision(collision, accelTransform, eCollide, eTransform);
			}
		}
	}
}