#pragma once
#include <unordered_set>
#include "Game.hpp"


#pragma warning(push)
#pragma warning(disable : 4244)


struct QuadBox {
	float x, y, width, height;

	/// <summary>
	/// Determines if an entity lies within the bounds of this bounding box
	/// </summary>
	/// <param name="entity">The entity to check for. Will return false if entity does not have Transform and Collision components</param>
	/// <returns>True if the entity is found within range, false otherwise</returns>
	bool contains(const Entity& entity) const {
		Transform* trans = Game::ecs.getComponent<Transform>(Game::stack.peek(), entity);
		Collision* coll = Game::ecs.getComponent<Collision>(Game::stack.peek(), entity);
		if (!trans || !coll) return false;

		float south = trans->pos.y + coll->hitHeight / 2.0f;
		float east = trans->pos.x + coll->hitWidth / 2.0f;
		float north = trans->pos.y - coll->hitHeight / 2.0f;
		float west = trans->pos.x - coll->hitWidth / 2.0f;

		return !(east < x || west > x + width || south < y || north > y + height);
	}

	/// <summary>
	/// Determines if the given bounding box intersects with this one
	/// </summary>
	/// <param name="range">The bounding box to compare against this one</param>
	/// <returns>True if the boxes are intersecting, false otherwise</returns>
	bool intersects(const QuadBox& range) {
		return !(range.x > x + width || range.x + range.width < x ||
			range.y > y + height || range.y + range.height < y);
	}
};


class QuadTree {
public:
	QuadTree(const QuadBox& boundary);
	~QuadTree() = default;

	// Prevent copying
	QuadTree(const QuadTree&) = delete;
	QuadTree& operator=(const QuadTree&) = delete;

	// Allow moving
	QuadTree(QuadTree&&) = default;
	QuadTree& operator=(QuadTree&&) = default;

	QuadBox boundary;

	/// <summary>
	/// Inserts an entity into the QuadTree
	/// </summary>
	/// <param name="entity">The entity to insert</param>
	/// <returns>True if insertion is successful, false otherwise</returns>
	bool insert(const Entity entity);

	/// <summary>
	/// Retrieves the entities within a specified snippet of the QuadTree
	/// </summary>
	/// <param name="range">The bounds to search for entities within</param>
	/// <param name="found">The unordered_set to insert the found entities into</param>
	void query(const QuadBox range, std::unordered_set<Entity>& found);

private:
	static constexpr int CAPACITY = 4;
	std::vector<Entity> entities;
	bool divided = false;

	std::unique_ptr<QuadTree> northwest = nullptr;
	std::unique_ptr<QuadTree> northeast = nullptr;
	std::unique_ptr<QuadTree> southwest = nullptr;
	std::unique_ptr<QuadTree> southeast = nullptr;

	void subdivide();
};


#pragma warning(pop)