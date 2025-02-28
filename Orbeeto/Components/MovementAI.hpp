#pragma once
#include "Component.hpp"
#include "../TimeManip.hpp"


enum M_AI {
	DEFAULT,  // Default behavior (nothing)
	CIRCLE_ACCEL,  // Uses acceleration to move entity in a circle
	
	GRUNT,  // Standard grunt enemy
	OCTOGRUNT,
};


struct MovementAI : public Component {
	int ai = M_AI::DEFAULT;

	// --- Misc --- //
	uint64_t intervalTime = 0;  // Standard interval timer. Can be used for anything
	double angle = 0.0;
};