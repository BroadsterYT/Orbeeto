#pragma once
#include "Component.hpp"


enum class ParticleAI {
	AWAY_FROM_CENTER,  // Particle moves away from spawn position and slows
};


struct Particle : Component {
	ParticleAI type = ParticleAI::AWAY_FROM_CENTER;  // The particle ai to use
	float maxLifetime = 1.0f;
	float lifetime = 0.0f;
};