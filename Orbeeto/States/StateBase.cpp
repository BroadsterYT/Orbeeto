#include "StateBase.hpp"
#include <iostream>
#include <algorithm>
#include <cassert>


StateBase::StateBase(bool allowUpdateBelow) {
	this->allowUpdateBelow = allowUpdateBelow;
}

std::vector<EntityDesc>& StateBase::getEntityDescs() {
	return entityDescs;
}

void StateBase::addEntityDesc(EntityDesc edesc) {
	entityDescs.push_back(edesc);
}

bool StateBase::hasPool(int componentId) {
	return pools.contains(componentId);
}

void StateBase::addPool(int componentId, IComponentPool* pool) {
	assert(!hasPool(componentId) && "Error: Cannot add pool because it already exists.");

	pools[componentId] = pool;
	std::cout << "Pool with ID " << componentId << " added to pools.\n";
}
