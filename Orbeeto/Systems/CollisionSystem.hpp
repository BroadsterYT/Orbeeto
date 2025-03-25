#pragma once
#include "System.hpp"


struct QuadBoundingBox {
	float x, y, width, height;

	/// <summary>
	/// Determines if a specified entity is within the bounding box
	/// </summary>
	/// <param name="entity">The entity to search for</param>
	/// <returns>True if the box contains the entity, false otherwise</returns>
	bool contains(const Entity& entity) const {
		Transform* transform = Game::ecs.getComponent<Transform>(entity);
		Collision* coll = Game::ecs.getComponent<Collision>(entity);
		if (transform == nullptr) return false;
		if (coll == nullptr) return false;

		// Need to get position from transform and not hitPos because floating precision is needed
		return (transform->pos.x + coll->hitWidth / 2 >= x && transform->pos.x - coll->hitWidth / 2 <= x + width &&
				transform->pos.y + coll->hitHeight / 2 >= y && transform->pos.y - coll->hitHeight / 2 <= y + height);
	}

	/// <summary>
	/// Determines if the given bounding box intersects with this one
	/// </summary>
	/// <param name="range">The bounding box to compare against this one</param>
	/// <returns>True if the boxes are intersecting, false otherwise</returns>
	bool intersects(const QuadBoundingBox& range) {
		return !(range.x > x + width || range.x + range.width < x ||
			range.y > y + height || range.y + range.height < y);
	}
};


class Quadtree {
public:
	Quadtree(const QuadBoundingBox& boundary) : boundary(boundary) {}

	~Quadtree() {
		delete northwest;
		delete northeast;
		delete southwest;
		delete southeast;
	}

	QuadBoundingBox boundary;

	/// <summary>
	/// Inserts an entity into the QuadTree
	/// </summary>
	/// <param name="entity">The entity to insert</param>
	/// <returns>True if insertion is successful, false otherwise</returns>
	bool insert(const Entity entity) {
		if (!boundary.contains(entity)) return false;

		if (entities.size() < CAPACITY) {
			entities.push_back(entity);
			return true;
		}

		// Too many entities, must subdivide
		if (!divided) subdivide();

		if (northwest->insert(entity) || northeast->insert(entity) || southwest->insert(entity) || southeast->insert(entity)) {
			return true;
		}

		return false;
	}

	/// <summary>
	/// Retrieves the entities within a specified snippet of the QuadTree
	/// </summary>
	/// <param name="range">The QuadBoundingBox to search for entities within</param>
	/// <param name="found">The vector to insert the found entities into</param>
	void query(const QuadBoundingBox range, std::vector<Entity>& found) {
		if (!boundary.intersects(range)) {
			return;
		};

		for (const auto& entity : entities) {
			if (range.contains(entity)) found.push_back(entity);
		}

		if (divided) {
			northwest->query(range, found);
			northeast->query(range, found);
			southwest->query(range, found);
			southeast->query(range, found);
		}
	}

private:
	static constexpr int CAPACITY = 4;
	std::vector<Entity> entities;
	bool divided = false;

	Quadtree* northwest = nullptr;
	Quadtree* northeast = nullptr;
	Quadtree* southwest = nullptr;
	Quadtree* southeast = nullptr;

	void subdivide() {
		float x = boundary.x;
		float y = boundary.y;
		float w = boundary.width / 2;
		float h = boundary.height / 2;

		northwest = new Quadtree(QuadBoundingBox{ x, y, w, h });
		northeast = new Quadtree(QuadBoundingBox{ x + w, y, w, h });
		southwest = new Quadtree(QuadBoundingBox{ x, y + h, w, h });
		southeast = new Quadtree(QuadBoundingBox{ x + w, y + h, w, h });
		divided = true;
	}
};


class CollisionSystem : public System {
public:
	CollisionSystem();

	void update();

private:
	Quadtree tree;
	/// <summary>
	/// Resets the collision tree and reinserts all entities
	/// </summary>
	/// <param name="boundary">The QuadBoundingBox to reset the tree with</param>
	void rebuildQuadtree(QuadBoundingBox boundary);

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

	void pushEntity(Collision* coll1, Transform* trans1, Collision* coll2, Transform* trans2);

	/// <summary>
	/// Performs all game logic related to collisions
	/// </summary>
	/// <param name="entity">The instigating entity</param>
	/// <param name="eColl">The instigating entity's collision component</param>
	/// <param name="eTrans">The instigating entity's transform component</param>
	/// <param name="other">The receiving entity</param>
	/// <param name="oColl">The receiving entity's collision component</param>
	void evaluateCollision(Entity& entity, Collision* eColl, Transform* eTrans, Entity& other, Collision* oColl);
	bool hasPhysicsTag(const Collision* coll, int tag);
};