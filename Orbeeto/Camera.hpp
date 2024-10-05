#pragma once
#include "SDL.h"
#include "ECS/Coordinator.hpp"
#include "Game.hpp"


class Camera {
private:
	SDL_Rect camera;
	Coordinator* coordinator;

public:
	Camera(Coordinator* coord = &Game::coordinator, int posX = 0, int posY = 0, int width = 0, int height = 0);

	int getX();
	int getY();

	void focus(const Entity& ref);
};