#pragma once
#include "System.hpp"
#include <vector>
#include "../WindowManager.hpp"


class SpriteSystem : public System {
public:
	SpriteSystem(SDL_Renderer* renderer);

	void render(SDL_Renderer* renderer);
};