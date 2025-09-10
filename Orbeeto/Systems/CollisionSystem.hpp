#pragma once
#include <memory>
#include <unordered_set>
#include "../QuadTree.hpp"
#include "System.hpp"


class ICollisionHandler {
public:
	virtual ~ICollisionHandler() {};
	virtual bool handle(Entity a, Collision* aColl, Transform* aTrans,
						Entity b, Collision* bColl, Transform* bTrans) = 0;

	virtual int intersection(const Collision* aColl, const Collision* bColl);
};


class CollisionSystem : public System {
public:
	CollisionSystem();

	static void queryTree(QuadBox box, std::unordered_set<Entity>& found);
	void update();

private:
	static QuadTree tree;
	std::vector<std::unique_ptr<ICollisionHandler>> handlers;

	/// <summary>
	/// Resets the collision tree and reinserts all entities
	/// </summary>
	/// <param name="boundary">The QuadBoundingBox to reset the tree with</param>
	void rebuildQuadtree(QuadBox boundary);

	/// <summary>
	/// Checks for a collision between two entites given their collision components
	/// </summary>
	/// <param name="eColl">Pointer to the collision component of the instigating entitiy</param>
	/// <param name="oColl">Pointer to the collision component of the receiving entity</param>
	/// <returns>True if the entities are colliding, false otherwise</returns>
	static bool checkForCollision(const Collision* eColl, const Collision* oColl);
	/// <summary>
	/// Performs all game logic related to collisions
	/// </summary>
	/// <param name="entity">The instigating entity</param>
	/// <param name="eColl">The instigating entity's collision component</param>
	/// <param name="eTrans">The instigating entity's transform component</param>
	/// <param name="other">The receiving entity</param>
	/// <param name="oColl">The receiving entity's collision component</param>
	void evaluateCollision(const Entity entity, Collision* eColl, Transform* eTrans, const Entity other, Collision* oColl);
};


class PushHandler : public ICollisionHandler {
public:
	bool handle(Entity a, Collision* aColl, Transform* aTrans,
				Entity b, Collision* bColl, Transform* bTrans) override;
};


class PortalTeleportHandler : public ICollisionHandler {
public:
	bool handle(Entity a, Collision* aColl, Transform* aTrans,
				Entity b, Collision* bColl, Transform* bTrans) override;
};


class GrappleHandler : public ICollisionHandler {
public:
	bool handle(Entity a, Collision* aColl, Transform* aTrans,
				Entity b, Collision* bColl, Transform* bTrans) override;
};


class PortalSpawningHandler : public ICollisionHandler {
public:
	bool handle(Entity a, Collision* aColl, Transform* aTrans,
				Entity b, Collision* bColl, Transform* bTrans) override;
};


class ProjHitHandler : public ICollisionHandler {
public:
	bool handle(Entity a, Collision* aColl, Transform* aTrans,
				Entity b, Collision* bColl, Transform* bTrans) override;
};


class RoomChangeHandler : public ICollisionHandler {
public:
	bool handle(Entity a, Collision* aColl, Transform* aTrans,
				Entity b, Collision* bColl, Transform* bTrans) override;
};