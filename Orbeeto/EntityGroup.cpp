#include "EntityGroup.hpp"
#include <algorithm>
#include <iostream>



EntityGroup::EntityGroup(std::string name) {
	this->name = name;
}

std::vector<Entity> EntityGroup::getEntities() const {
	return entities;
}

void EntityGroup::addEntity(const Entity entity) {
	auto it = std::find(entities.begin(), entities.end(), entity);
	if (it != entities.end()) {
		std::cout << "Entity " << entity << " is already present in " << name << std::endl;
		return;
	}
	entities.push_back(entity);
}

void EntityGroup::removeEntity(const Entity entity) {
	auto it = std::find(entities.begin(), entities.end(), entity);
	if (it != entities.end()) {
		entities.erase(it);
	}
}