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
};