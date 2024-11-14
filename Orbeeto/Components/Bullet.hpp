#pragma once
#include "Component.hpp"


struct Bullet : Component {
	int damage;
	uint32_t birthTime = SDL_GetTicks();
};