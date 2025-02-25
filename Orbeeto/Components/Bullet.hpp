#pragma once
#include "Component.hpp"
#include "SDL.h"
#include "../TimeManip.hpp"


struct Bullet : Component {
	int damage = 5;
	uint32_t birthTime = SDL_GetTicks();
	int bulletAI = 0;

	uint32_t shotBy = 0;

	// ----- Misc ----- //
	bool homingCheck = false;
	uint32_t closestTarget = 0;
};