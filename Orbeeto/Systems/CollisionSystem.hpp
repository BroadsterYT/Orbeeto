#pragma once
#include "System.hpp"


class CollisionSystem : public System {
public:
	CollisionSystem();

	void update();

private:
	/// <summary>
	/// Checks for a collision between two entites given their collision components
	/// </summary>
	/// <param name="eColl">Pointer to the collision component of the instigating entitiy</param>
	/// <param name="oColl">Pointer to the collision component of the receiving entity</param>
	/// <returns>True if the entities are colliding, false otherwise</returns>
	bool checkForCollision(const Collision* eColl, const Collision* oColl);
	/// <summary>
	/// Returns the side a receiving entity is being hit by the instigating entity.
	/// NOTE: This should only be called after a collision has been detected!
	/// </summary>
	/// <param name="eColl">Pointer to the collision component of instigating entity</param>
	/// <param name="oColl">Pointer to the collision component of receiving entity</param>
	/// <returns>0 = South, 1 = East, 2 = North, 3 = West. If an error occurs, returns -1.
	/// </returns>
	int intersection(const Collision* eColl, const Collision* oColl);

	/// <summary>
	/// Causes entity 1 to be pushed by entity 2
	/// </summary>
	/// <param name="coll1">Pointer to entity 1's collision component</param>
	/// <param name="trans1">Pointer to entity 1's transform component</param>
	/// <param name="coll2">Pointer to entity 2's collision component</param>
	/// <param name="trans2">Pointer to entity 2's transform component</param>
	void pushEntity(Collision* coll1, Transform* trans1, Collision* coll2, Transform* trans2);
	void evaluateCollision(Entity& entity, Collision* eColl, Transform* eTrans, Entity& other, Collision* oColl);
	bool hasPhysicsTag(const Collision* coll, std::string tag);
};