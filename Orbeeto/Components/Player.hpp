#pragma once
#include "Component.hpp"


enum GrappleState {
	INACTIVE = 0,
	SENT = 1,
	LATCHED = 2,
	RETURNING = 3
};

struct Player : Component {
	int grappleState = GrappleState::INACTIVE;
	int grappleInputCopy = 0; // A copy of the value if the number of middle mouse presses
};