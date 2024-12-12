#pragma once
#include "System.hpp"


class CollisionSystem : public System {
private:
	/// <summary>
	/// Causes entity 1 to be pushed by entity 2
	/// </summary>
	/// <param name="coll1">Pointer to entity 1's collision component</param>
	/// <param name="trans1">Pointer to entity 1's transform component</param>
	/// <param name="coll2">Pointer to entity 2's collision component</param>
	/// <param name="trans2">Pointer to entity 2's transform component</param>
	void pushEntity(Collision* coll1, Transform* trans1, Collision* coll2, Transform* trans2) {
		int side = coll1->intersection(coll2);

		if (side == 0
			&& (trans1->vel.y < 0 || trans2->vel.y > 0)
			&& trans1->pos.y <= trans2->pos.y + coll2->hitHeight / 2) {
			trans1->vel.y = 0;
			trans1->pos.y = trans2->pos.y + coll2->hitHeight / 2;
		}
		else if (side == 1
			&& (trans1->vel.x < 0 || trans2->vel.x > 0)
			&& trans1->pos.x <= trans2->pos.x + coll2->hitWidth / 2) {
			trans1->vel.x = 0;
			trans1->pos.x = trans2->pos.x + coll2->hitWidth / 2;
		}
		else if (side == 2
			&& (trans1->vel.y > 0 || trans2->vel.y < 0)
			&& trans1->pos.y >= trans2->pos.y - coll2->hitHeight / 2) {
			trans1->vel.y = 0;
			trans1->pos.y = trans2->pos.y - coll2->hitHeight / 2;
		}
		else if (side == 3
			&& (trans1->vel.x > 0 || trans2->vel.x < 0)
			&& trans1->pos.x >= trans2->pos.x - coll2->hitWidth / 2) {
			trans1->vel.x = 0;
			trans1->pos.x = trans2->pos.x - coll2->hitWidth / 2;
		}
	}
	
	void evaluateCollision(Entity& entity, Collision* eColl, Transform* eTrans, Entity& other, Collision* oColl) {
		// Pushing entities that can be pushed
		if (eColl->canBePushed && oColl->canPush) {
			Transform* oTrans = Game::ecs.getComponent<Transform>(other);
			pushEntity(eColl, eTrans, oColl, oTrans);
		}
	}

public:
	CollisionSystem() {}
	
	void update() {
		for (Entity& entity : Game::ecs.getSystemGroup<Collision, Transform>()) {
			Collision* collision = Game::ecs.getComponent<Collision>(entity);
			Transform* transform = Game::ecs.getComponent<Transform>(entity);

			collision->hitPos = transform->pos;

			// Evaluating every entity in the system for a collision
			for (Entity& other : Game::ecs.getSystemGroup<Collision, Transform>()) {
				if (other == entity) continue;
				Collision* oCollide = Game::ecs.getComponent<Collision>(other);

				if (collision->checkCollision(oCollide)) {
					evaluateCollision(entity, collision, transform, other, oCollide);
				}
			}
		}
	}
};