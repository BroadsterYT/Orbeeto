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
	void pushEntity(Collision* coll1, Transform* trans1, Collision* coll2, Transform* trans2);
	void evaluateCollision(Entity& entity, Collision* eColl, Transform* eTrans,
		Entity& other, Collision* oColl);

public:
	CollisionSystem();
	void update();
};