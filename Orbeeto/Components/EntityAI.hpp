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


	void serialize(std::ofstream& out) override {
		uint32_t rawAi = static_cast<uint32_t>(ai);
		out.write(reinterpret_cast<const char*>(&rawAi), sizeof(rawAi));
	}

	void deserialize(std::ifstream& in) override {
		uint32_t rawAi;
		in.read(reinterpret_cast<char*>(&rawAi), sizeof(rawAi));
		ai = static_cast<AiType>(rawAi);
	}
};


struct FollowEntityAI : public Component {
	Entity entityRef = 0;
	Vector2 distOffset = Vector2();


	void serialize(std::ofstream& out) override {
		SerialHelper::serialize(out, &entityRef, &distOffset.x, &distOffset.y);
	}

	void deserialize(std::ifstream& in) override {
		SerialHelper::deserialize(in, &entityRef, &distOffset.x, &distOffset.y);
	}
};

/*
  _______   _       _        _              _____
 |__   __| (_)     | |      | |       /\   |_   _|
	| |_ __ _ _ __ | | _____| |_     /  \    | |
	| | '__| | '_ \| |/ / _ | __|   / /\ \   | |
	| | |  | | | | |   |  __| |_   / ____ \ _| |_
	|_|_|  |_|_| |_|_|\_\___|\__| /_/    \_|_____|
*/

struct TwoPointShiftAI : Component {
	Entity toggleRef = 0;
	InterpToggle<Vector2> interp = InterpToggle<Vector2>(Math::cerp<Vector2>, Vector2(), Vector2(), 0.25f);
	bool lastToggleState = false;


	void serialize(std::ofstream& out) override {
		SerialHelper::serialize(out, &toggleRef,
			&interp.val1.x, &interp.val1.y,
			&interp.val2.x, &interp.val2.y,
			&interp.cycleTime, &interp.weight,
			&interp.lastWeight, &interp.lastToggle,
			&interp.active,
			&lastToggleState
			);
	}

	void deserialize(std::ifstream& in) override {
		SerialHelper::deserialize(in, &toggleRef,
			&interp.val1.x, &interp.val1.y,
			&interp.val2.x, &interp.val2.y,
			&interp.cycleTime, &interp.weight,
			&interp.lastWeight, &interp.lastToggle,
			&interp.active,
			&lastToggleState
			);
	}
};


struct TractorBeamAI : Component {
	Entity toggleRef = 0;
	bool lastToggleState = false;
	bool invertToggle = false;
	int width = 64;
	int height = 64;

	int direction = 0;
	float strength = 0.05f;


	void serialize(std::ofstream& out) override {
		SerialHelper::serialize(out, 
			&toggleRef, 
			&lastToggleState, 
			&invertToggle, 
			&width, 
			&height, 
			&direction,
			&strength);
	}

	void deserialize(std::ifstream& in) override {
		SerialHelper::deserialize(in, 
			&toggleRef, 
			&lastToggleState,
			&invertToggle, 
			&width, 
			&height, 
			&direction,
			&strength);
	}
};

/*
  ______                                       _____ 
 |  ____|                                /\   |_   _|
 | |__   _ __   ___ _ __ ___  _   _     /  \    | |  
 |  __| | '_ \ / _ \ '_ ` _ \| | | |   / /\ \   | |  
 | |____| | | |  __/ | | | | | |_| |  / ____ \ _| |_ 
 |______|_| |_|\___|_| |_| |_|\__, | /_/    \_\_____|
                               __/ |                 
                              |___/                  
*/

struct MyteAI : Component {



	void serialize(std::ofstream& out) override {

	}

	void deserialize(std::ifstream& in) override {

	}
};


struct TextTrembleAI : public Component {
	Vector2 center = Vector2();
	Vector2 randOffset = Vector2();
	float mag = 2.0f;


	void serialize(std::ofstream& out) override {
		SerialHelper::serialize(out, &center.x, &center.y, &randOffset.x, &randOffset.y, &mag);
	}

	void deserialize(std::ifstream& in) override {
		SerialHelper::deserialize(in, &center.x, &center.y, &randOffset.x, &randOffset.y, &mag);
	}
};


struct TextWaveAI : public Component {
	Vector2 center = Vector2();
	float mag = 5.0f;
	float timeElapsed = 0.0f;


	void serialize(std::ofstream& out) override {
		SerialHelper::serialize(out, &center.x, &center.y, &mag, &timeElapsed);
	}

	void deserialize(std::ifstream& in) override {
		SerialHelper::deserialize(in, &center.x, &center.y, &mag, &timeElapsed);
	}
};