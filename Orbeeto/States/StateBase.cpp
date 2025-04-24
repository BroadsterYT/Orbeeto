#include "StateBase.hpp"
#include <iostream>
#include <algorithm>


StateBase::StateBase(bool allowUpdateBelow) {
	this->allowUpdateBelow = allowUpdateBelow;
}

std::vector<EntityDesc>& StateBase::getEntityDescs() {
	return entityDescs;
}

void StateBase::addEntityDesc(EntityDesc edesc) {
	entityDescs.push_back(edesc);
}
