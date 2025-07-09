#pragma once
#include "Component.hpp"
#include "../TimeManip.hpp"


enum class M_AI {
	DEFAULT,  // Default behavior (nothing)
	CIRCLE_ACCEL,  // Uses acceleration to move entity in a circle
	FOLLOW_ENTITY,  // Follows entity specified by entityRef from a distance specified in distance vector
	
	GRUNT,  // Standard grunt enemy
	OCTOGRUNT,

	// ----- Text Movements ----- //
	TEXT_TREMBLE,
};


struct MovementAI : public Component {
	M_AI ai = M_AI::DEFAULT;  // The AI for the entity to use, chosen from M_AI.

	// --- Misc --- //
	uint32_t entityRef = 0;  // General entity reference, can be used for anything
	uint64_t intervalTime = 0;  // Standard interval timer. Can be used for anything
	
	Vector2 vec1 = { 0, 0 };  // Can be used for anything
	Vector2 distance = { 0, 0 };  // Can be used for anything
	float mag = 1.0f; // Magnitude. Can be used for anything
	double angle = 0.0;
};