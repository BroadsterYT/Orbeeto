#pragma once
#include "Component.hpp"
#include "../TimeManip.hpp"
#include "../InterpToggle.hpp"


enum class M_AI {
	default_ai,  // Default behavior (nothing)
	circle_accel,  // Uses acceleration to move entity in a circle
	follow_entity,  // Follows entity specified by entityRef from a distance specified in distance vector

	// ----- Trinkets ----- //
	two_point_shift,  // Moves back and forth between two points when the trigger entity toggles
	
	// ----- Enemies ----- //
	myte,
	kilomyte,

	// ----- Text Movements ----- //
	text_tremble,
	text_wave,
};


struct EntityAI : public Component {
	M_AI ai = M_AI::default_ai;  // The AI for the entity to use, chosen from M_AI.

	// --- Misc --- //
	Entity entityRef = 0;  // General entity reference, can be used for anything
};


struct FollowEntityAI : public Component {
	Entity entityRef = 0;
	Vector2 distOffset = Vector2();
};


struct TwoPointShiftAI : public Component {
	Entity toggleRef = 0;
	InterpToggle<Vector2> interp = InterpToggle<Vector2>(Math::cerp<Vector2>, Vector2(), Vector2(), 0.25f);
	bool lastToggleState = false;
};


struct TextTrembleAI : public Component {
	Vector2 center = Vector2();
	Vector2 randOffset = Vector2();
	float mag = 2.0f;
};


struct TextWaveAI : public Component {
	Vector2 center = Vector2();
	float mag = 5.0f;
	float timeElapsed = 0.0f;
};