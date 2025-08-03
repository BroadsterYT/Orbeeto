#pragma once
#include "../SerialHelper.hpp"


struct Component {
	virtual ~Component() {};

	virtual void serialize(std::ofstream& out) {};
	virtual void deserialize(std::ifstream& in) {};
};