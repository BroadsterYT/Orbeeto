#pragma once
#include "Component.hpp"


enum class ParticleAI {
	AWAY_FROM_CENTER,  // Particle moves away from spawn position and slows
};


struct Particle : Component {
	ParticleAI type = ParticleAI::AWAY_FROM_CENTER;  // The particle ai to use
	float maxLifetime = 1.0f;
	float lifetime = 0.0f;


	void serialize(std::ofstream& out) override {
		uint32_t rawAi = static_cast<uint32_t>(type);
		SerialHelper::serialize(out, &rawAi);

		SerialHelper::serialize(out, &maxLifetime, &lifetime);
	}

	void deserialize(std::ifstream& in) override {
		uint32_t rawAi;
		SerialHelper::deserialize(in, &rawAi);
		type = static_cast<ParticleAI>(rawAi);

		SerialHelper::deserialize(in, &maxLifetime, &lifetime);
	}
};