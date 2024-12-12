#pragma once
#include <vector>
#include <string>


using Entity = uint32_t;

class EntityGroup {
private:
	std::string name;
	std::vector<Entity> entities;

public:
	EntityGroup(std::string name);

	std::vector<Entity> getEntities() const;
	void addEntity(const Entity entity);
	void removeEntity(const Entity entity);
};