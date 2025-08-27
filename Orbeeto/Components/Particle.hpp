#pragma once
#include "Component.hpp"


enum class ParticleAI {
	away_from_center,  // Particle moves away from spawn position and slows
};


struct Particle : Component {
	ParticleAI type = ParticleAI::away_from_center;  // The particle ai to use
	float maxLifetime = 1.0f;
	float lifetime = 0.0f;


	// Particles will not be serialized or deserialized between rooms
};