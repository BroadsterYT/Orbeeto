#pragma once
#include "System.hpp"
#include <vector>


class SpriteSystem : public System {
public:
	SpriteSystem(SDL_Renderer* renderer);

	void render(SDL_Renderer* renderer);
};