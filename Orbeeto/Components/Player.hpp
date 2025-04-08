#pragma once
#include "Component.hpp"
#include <stdint.h>


enum GrappleState {
	INACTIVE,
	SENT,
	LATCHED,
	RETURNING
};

struct Player : Component {
	int grappleState = GrappleState::INACTIVE;
	uint32_t grappleRef = 0; // The ID of the active grappling hook. Is 0 when no grappling hook is deployed
	bool moveToGrapple = false;
	
	int grappleInputCopy = 0; // A copy of the value of the number of middle mouse releases
	int portalInputCopy = 0; // A copy of the number of right mouse releases

	std::pair<uint32_t, uint32_t> portals = { 0, 0 };
};