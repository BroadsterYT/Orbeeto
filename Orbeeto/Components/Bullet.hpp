#pragma once
#include "Component.hpp"
#include "SDL.h"


struct Bullet : Component {
	int damage;
	uint32_t birthTime = SDL_GetTicks();
	int bulletAI = 0;
};