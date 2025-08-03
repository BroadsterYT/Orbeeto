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
	M_AI ai = M_AI::default_ai;


	void serialize(std::ofstream& out) override {
		uint32_t rawAi = static_cast<uint32_t>(ai);
		out.write(reinterpret_cast<const char*>(&rawAi), sizeof(rawAi));
	}

	void deserialize(std::ifstream& in) override {
		uint32_t rawAi;
		in.read(reinterpret_cast<char*>(&rawAi), sizeof(rawAi));
		ai = static_cast<M_AI>(rawAi);
	}
};


struct FollowEntityAI : public Component {
	Entity entityRef = 0;
	Vector2 distOffset = Vector2();


	void serialize(std::ofstream& out) override {
		out.write(reinterpret_cast<const char*>(&entityRef), sizeof(entityRef));

		out.write(reinterpret_cast<const char*>(&distOffset.x), sizeof(distOffset.x));
		out.write(reinterpret_cast<const char*>(&distOffset.y), sizeof(distOffset.y));
	}

	void deserialize(std::ifstream& in) override {
		in.read(reinterpret_cast<char*>(&entityRef), sizeof(entityRef));

		in.read(reinterpret_cast<char*>(&distOffset.x), sizeof(distOffset.x));
		in.read(reinterpret_cast<char*>(&distOffset.y), sizeof(distOffset.y));
	}
};


struct TwoPointShiftAI : public Component {
	Entity toggleRef = 0;
	InterpToggle<Vector2> interp = InterpToggle<Vector2>(Math::cerp<Vector2>, Vector2(), Vector2(), 0.25f);
	bool lastToggleState = false;


	void serialize(std::ofstream& out) override {
		out.write(reinterpret_cast<const char*>(&toggleRef), sizeof(toggleRef));

		out.write(reinterpret_cast<const char*>(&interp.val1.x), sizeof(interp.val1.x));
		out.write(reinterpret_cast<const char*>(&interp.val1.y), sizeof(interp.val1.y));
		out.write(reinterpret_cast<const char*>(&interp.val2.x), sizeof(interp.val2.x));
		out.write(reinterpret_cast<const char*>(&interp.val2.y), sizeof(interp.val2.y));
		out.write(reinterpret_cast<const char*>(&interp.cycleTime), sizeof(interp.cycleTime));
		out.write(reinterpret_cast<const char*>(&interp.weight), sizeof(interp.weight));
		out.write(reinterpret_cast<const char*>(&interp.lastWeight), sizeof(interp.lastWeight));
		out.write(reinterpret_cast<const char*>(&interp.lastToggle), sizeof(interp.lastToggle));
		out.write(reinterpret_cast<const char*>(&interp.active), sizeof(interp.active));

		out.write(reinterpret_cast<const char*>(&lastToggleState), sizeof(lastToggleState));
	}

	void deserialize(std::ifstream& in) override {
		in.read(reinterpret_cast<char*>(&toggleRef), sizeof(toggleRef));

		in.read(reinterpret_cast<char*>(&interp.val1.x), sizeof(interp.val1.x));
		in.read(reinterpret_cast<char*>(&interp.val1.y), sizeof(interp.val1.y));
		in.read(reinterpret_cast<char*>(&interp.val2.x), sizeof(interp.val2.x));
		in.read(reinterpret_cast<char*>(&interp.val2.y), sizeof(interp.val2.y));
		in.read(reinterpret_cast<char*>(&interp.cycleTime), sizeof(interp.cycleTime));
		in.read(reinterpret_cast<char*>(&interp.weight), sizeof(interp.weight));
		in.read(reinterpret_cast<char*>(&interp.lastWeight), sizeof(interp.lastWeight));
		in.read(reinterpret_cast<char*>(&interp.lastToggle), sizeof(interp.lastToggle));
		in.read(reinterpret_cast<char*>(&interp.active), sizeof(interp.active));

		in.read(reinterpret_cast<char*>(&lastToggleState), sizeof(lastToggleState));
	}
};


struct TextTrembleAI : public Component {
	Vector2 center = Vector2();
	Vector2 randOffset = Vector2();
	float mag = 2.0f;


	void serialize(std::ofstream& out) override {
		out.write(reinterpret_cast<const char*>(&center.x), sizeof(center.x));
		out.write(reinterpret_cast<const char*>(&center.y), sizeof(center.y));
		out.write(reinterpret_cast<const char*>(&randOffset.x), sizeof(randOffset.x));
		out.write(reinterpret_cast<const char*>(&randOffset.y), sizeof(randOffset.y));
		out.write(reinterpret_cast<const char*>(&mag), sizeof(mag));
	}

	void deserialize(std::ifstream& in) override {
		in.read(reinterpret_cast<char*>(&center.x), sizeof(center.x));
		in.read(reinterpret_cast<char*>(&center.y), sizeof(center.y));
		in.read(reinterpret_cast<char*>(&randOffset.x), sizeof(randOffset.x));
		in.read(reinterpret_cast<char*>(&randOffset.y), sizeof(randOffset.y));
		in.read(reinterpret_cast<char*>(&mag), sizeof(mag));
	}
};


struct TextWaveAI : public Component {
	Vector2 center = Vector2();
	float mag = 5.0f;
	float timeElapsed = 0.0f;


	void serialize(std::ofstream& out) override {
		out.write(reinterpret_cast<const char*>(&center.x), sizeof(center.x));
		out.write(reinterpret_cast<const char*>(&center.y), sizeof(center.y));
		out.write(reinterpret_cast<const char*>(&mag), sizeof(mag));
		out.write(reinterpret_cast<const char*>(&timeElapsed), sizeof(timeElapsed));
	}

	void deserialize(std::ifstream& in) override {
		in.read(reinterpret_cast<char*>(&center.x), sizeof(center.x));
		in.read(reinterpret_cast<char*>(&center.y), sizeof(center.y));
		in.read(reinterpret_cast<char*>(&mag), sizeof(mag));
		in.read(reinterpret_cast<char*>(&timeElapsed), sizeof(timeElapsed));
	}
};