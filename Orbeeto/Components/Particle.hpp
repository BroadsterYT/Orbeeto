#pragma once
#include "Component.hpp"


struct Particle : Component {
	float maxLifetime = 1.0f;
	float lifetime = 0.0f;
};