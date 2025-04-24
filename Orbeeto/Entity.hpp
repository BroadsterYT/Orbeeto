#pragma once

#include <vector>
#include <bitset>
#include "Components/Component.hpp"


using Entity = uint32_t;

const uint32_t MAX_ENTITIES = 2000;
const uint32_t MAX_COMPONENTS = 16;
using ComponentMask = std::bitset<MAX_COMPONENTS>;


struct EntityDesc {
	Entity entity;
	ComponentMask mask;
	std::vector<Component*> components;

	bool operator==(const EntityDesc other) {
		return entity == other.entity;
	}
};
