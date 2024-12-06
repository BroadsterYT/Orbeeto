#pragma once
#include <vector>


class EntityGroup {
private:
	std::vector<uint32_t> entities;

public:
	std::vector<uint32_t> getEntities() const;
	void addEntity(const uint32_t entity);
	void removeEntity(const uint32_t entity);
};