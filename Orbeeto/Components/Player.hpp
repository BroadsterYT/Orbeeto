#pragma once
#include "Component.hpp"
#include <stdint.h>


enum class GrappleState {
	INACTIVE,
	SENT,
	LATCHED,
	RETURNING
};

struct Player : Component {
	GrappleState grappleState = GrappleState::INACTIVE;
	Entity grappleRef = 0; // The ID of the active grappling hook.
	bool moveToGrapple = false;
	
	int grappleInputCopy = 0; // A copy of the value of the number of middle mouse releases
	int portalInputCopy = 0; // A copy of the number of right mouse releases

	std::pair<uint32_t, uint32_t> portals = { 0, 0 };


	void serialize(std::ofstream& out) override {

	}

	void deserialize(std::ifstream& in) override {

	}
};