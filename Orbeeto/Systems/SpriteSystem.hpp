#pragma once
#include "SDL.h"
#include "../ECS/Coordinator.hpp"
#include "../ECS/System.hpp"
#include "../Components/Sprite.hpp"


class SpriteSystem : public System {
private:
	Coordinator* coordinator;

public:
	void init(Coordinator* coord);
	void render(SDL_Renderer* renderer);
	void update();
};
