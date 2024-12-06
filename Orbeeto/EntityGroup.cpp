#include "EntityGroup.hpp"
#include <algorithm>


std::vector<uint32_t> EntityGroup::getEntities() const {
	return entities;
}

void EntityGroup::addEntity(const uint32_t entity) {
	entities.push_back(entity);
}

void EntityGroup::removeEntity(const uint32_t entity) {
	auto it = std::find(entities.begin(), entities.end(), entity);
	if (it != entities.end()) {
		entities.erase(it);
	}
}