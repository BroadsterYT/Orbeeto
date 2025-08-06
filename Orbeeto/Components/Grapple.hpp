#pragma once
#include "Component.hpp"


struct Grapple : Component {
	uint32_t owner = 0;
	uint32_t grappledTo = 0;


	void serialize(std::ofstream& out) override {
		SerialHelper::serialize(out, &owner, &grappledTo);
	}

	void deserialize(std::ifstream& in) override {
		SerialHelper::deserialize(in, &owner, &grappledTo);
	}
};