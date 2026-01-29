#pragma once
#include "Component.hpp"
#include "../TimeManip.hpp"
#include "../InterpToggle.hpp"


enum class AiType {
	default_ai,  // Default behavior (nothing)
	circle_accel,  // Uses acceleration to move entity in a circle
	follow_entity,  // Follows entity specified by entityRef from a distance specified in distance vector

	// ----- Trinkets ----- //
	two_point_shift,  // Moves back and forth between two points when the trigger entity toggles
	tractor_beam,
	
	// ----- Enemies ----- //
	myte,
	kilomyte,

	// ----- Text Movements ----- //
	text_tremble,
	text_wave,
};


struct EntityAI : public Component {
	AiType ai = AiType::default_ai;
};


struct FollowEntityAI : public Component {
	Entity entityRef = 0;
	Vector2 distOffset = Vector2();
};

struct TwoPointShiftAI : Component {
	Entity toggleRef = 0;
	InterpToggle<Vector2> interp = InterpToggle<Vector2>(Math::cerp<Vector2>, Vector2(), Vector2(), 0.25f);
	bool lastToggleState = false;
};


struct TractorBeamAI : Component {
	Entity toggleRef = 0;
	bool lastToggleState = false;
	bool invertToggle = false;
	int width = 64;
	int height = 64;

	int direction = 0;
	float strength = 0.05f;
};


struct MyteAI : Component {
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