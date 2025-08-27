#pragma once
#include "Component.hpp"
#include <stdint.h>


enum Facing {
	SOUTH,
	EAST,
	NORTH,
	WEST
};

struct TeleportLink : public Component {
	Entity linkedTo = 0;
	int facing = Facing::SOUTH;


	void serialize(std::ofstream& out) override {
		SerialHelper::serialize(out, &linkedTo, &facing);
	}

	void deserialize(std::ifstream& in) override {
		SerialHelper::deserialize(in, &linkedTo, &facing);
	}
};