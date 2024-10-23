#include "CollisionSystem.hpp"
#include <iostream>


void CollisionSystem::init(Coordinator* coord) {
	coordinator = coord;
}

void CollisionSystem::pushEntity(Collision& coll1, Transform& trans1, Collision& coll2, Transform& trans2) {
	if (!coll1.canBePushed && coll2.canPush) return;
	
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

void CollisionSystem::evaluateCollison(Entity& entity, Transform& eTrans, Collision& eColl, Entity& other, Collision& oColl) {
	// Pushing entities that can be pushed
	if (eColl.canBePushed && oColl.canPush) {
		auto& oTrans = coordinator->getComponent<Transform>(other);
		this->pushEntity(eColl, eTrans, oColl, oTrans);
	}

	// Taking damage if entity has stats and is hit by a projectile that does damage
	if (eColl.canHurt && oColl.isProj) {
		
	}
}

void CollisionSystem::update() {
	for (Entity entity : mEntities) {
		auto& transform = coordinator->getComponent<Transform>(entity);
		auto& collision = coordinator->getComponent<Collision>(entity);

		// Assign hitbox to entity center
		collision.hitPos = transform.pos;
		
		// Checking every collidable entity for a collision
		for (Entity e : mEntities) {
			if (e == entity) continue;
			auto& eCollide = coordinator->getComponent<Collision>(e);

			if (collision.checkCollision(eCollide)) {
				this->evaluateCollison(entity, transform, collision, e, eCollide);
			}
		}
	}
}