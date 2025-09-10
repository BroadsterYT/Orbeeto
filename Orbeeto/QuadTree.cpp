#include "QuadTree.hpp"


QuadTree::QuadTree(const QuadBox& boundary) : boundary(boundary) {}

bool QuadTree::insert(const Entity entity) {
	if (!boundary.contains(entity)) return false;

	if (entities.size() < CAPACITY && !divided) {
		entities.push_back(entity);
		return true;
	}

	if (!divided) {
		subdivide();
	}

	bool inserted = false;
	if (northwest->boundary.contains(entity)) {
		northwest->insert(entity);
		inserted = true;
	}
	if (northeast->boundary.contains(entity)) {
		northeast->insert(entity);
		inserted = true;
	}
	if (southwest->boundary.contains(entity)) {
		southwest->insert(entity);
		inserted = true;
	}
	if (southeast->boundary.contains(entity)) {
		southeast->insert(entity);
		inserted = true;
	}

	// Keep in this quad if didn't correctly fit
	if (!inserted) {
		entities.push_back(entity);
	}
}

void QuadTree::query(const QuadBox range, std::unordered_set<Entity>& found) {
	if (!boundary.intersects(range)) {
		return;
	};

	for (const auto& entity : entities) {
		if (range.contains(entity)) found.insert(entity);
	}

	if (divided) {
		northwest->query(range, found);
		northeast->query(range, found);
		southwest->query(range, found);
		southeast->query(range, found);
	}
}

void QuadTree::subdivide() {
	float x = boundary.x;
	float y = boundary.y;
	float w = boundary.width / 2;
	float h = boundary.height / 2;

	northwest = std::make_unique<QuadTree>(QuadBox{ x, y, w, h });
	northeast = std::make_unique<QuadTree>(QuadBox{ x + w, y, w, h });
	southwest = std::make_unique<QuadTree>(QuadBox{ x, y + h, w, h });
	southeast = std::make_unique<QuadTree>(QuadBox{ x + w, y + h, w, h });
	divided = true;
}