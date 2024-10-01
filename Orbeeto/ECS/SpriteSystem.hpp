#pragma once
#include "SDL.h"
#include "System.hpp"


class SpriteSystem : public System {
public:
	void init(Coordinator* coord);
	void render(SDL_Renderer* renderer);
	void update();

private:
	Coordinator* coordinator;
};
