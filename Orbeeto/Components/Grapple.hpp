#pragma once
#include "Component.hpp"


struct Grapple : Component {
	uint32_t owner;
	uint32_t grappledTo = 0;
};