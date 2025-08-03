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
		uint32_t rawType = static_cast<uint32_t>(type);
		out.write(reinterpret_cast<const char*>(&rawType), sizeof(rawType));
		
		out.write(reinterpret_cast<const char*>(&maxLifetime), sizeof(maxLifetime));
		out.write(reinterpret_cast<const char*>(&lifetime), sizeof(lifetime));
	}

	void deserialize(std::ifstream& in) override {
		uint32_t rawType;
		in.read(reinterpret_cast<char*>(&rawType), sizeof(rawType));
		type = static_cast<ParticleAI>(rawType);

		in.read(reinterpret_cast<char*>(&maxLifetime), sizeof(maxLifetime));
		in.read(reinterpret_cast<char*>(&lifetime), sizeof(lifetime));
	}
};