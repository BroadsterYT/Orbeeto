#pragma once
#include "System.hpp"


class SpriteSystem : public System {
public:
	SpriteSystem();

	void render(SDL_Renderer* renderer);
	void update();
};