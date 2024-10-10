#pragma once
#include "../ECS/System.hpp"
#include "../ECS/Coordinator.hpp"

#include "../Components/AccelTransform.hpp"
#include "../Components/PushCollision.hpp"


class CollisionSystem : public System {
private:
	Coordinator* coordinator;

public:
	void init(Coordinator* coord);

	/// <summary>
	/// Instigates the "pushing" of an entity. The instigator gets pushed by the recipient
	/// </summary>
	/// <param name="coll1">Collision component of instigator entity</param>
	/// <param name="trans1">AccelTransform component of instigator entity</param>
	/// <param name="coll2">Collision component of recipient entity</param>
	/// <param name="trans2">AccelTransform component of recipient entity</param>
	static void pushCollision(PushCollision& coll1, AccelTransform& trans1,
		PushCollision& coll2, AccelTransform& trans2);
	
	void update();
};
