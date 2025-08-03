#include "StateBase.hpp"
#include <algorithm>
#include <cassert>
#include <iostream>


StateBase::StateBase(bool allowUpdateBelow) {
	this->allowUpdateBelow = allowUpdateBelow;

	for (Entity i = 1; i < MAX_ENTITIES; ++i) {
		freeEntities.push_back(i);
	}
}

std::vector<EntityDesc>& StateBase::getEntityDescs() {
	return entityDescs;
}

void StateBase::addEntityDesc(EntityDesc edesc) {
	entityDescs.push_back(edesc);
}

Entity StateBase::getNextFree() {
	assert(freeEntities.size() > 0 && "Error: An entity overflow has occurred");
	Entity temp = freeEntities[0];
	freeEntities.erase(freeEntities.begin());
	return temp;
}

void StateBase::returnFreeEntity(const Entity entity) {
	freeEntities.push_back(entity);
}