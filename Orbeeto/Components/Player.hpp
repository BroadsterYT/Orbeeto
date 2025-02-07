#pragma once
#include "Component.hpp"
#include <stdint.h>


enum GrappleState {
	INACTIVE = 0,
	SENT = 1,
	LATCHED = 2,
	RETURNING = 3
};

struct Player : Component {
	int grappleState = GrappleState::INACTIVE;
	
	int grappleInputCopy = 0; // A copy of the value of the number of middle mouse releases
	int portalInputCopy = 0; // A copy of the number of right mouse releases
};