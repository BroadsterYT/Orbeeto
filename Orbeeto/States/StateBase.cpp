#include "StateBase.hpp"


StateBase::StateBase(StateName name, bool allowUpdateBelow) {
	this->name = name;
	this->allowUpdateBelow = allowUpdateBelow;
}

StateName StateBase::getName() {
	return name;
}
