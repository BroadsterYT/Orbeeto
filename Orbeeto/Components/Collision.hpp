#pragma once
#include "Component.hpp"
#include "../Vector2.hpp"
#include <cmath>
#include <iostream>
#include <SDL_stdinc.h>


struct Collision : Component {
	int hitWidth = 64;
	int hitHeight = 64;
	Vector2 hitPos = { 0, 0 };

	std::vector<std::string> physicsTags;
};