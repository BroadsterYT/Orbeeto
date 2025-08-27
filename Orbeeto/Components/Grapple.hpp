#pragma once
#include "Component.hpp"


struct Grapple : Component {
	uint32_t owner = 0;
	uint32_t grappledTo = 0;


	// Grappling hook will not be serialized or deserialized between rooms
};