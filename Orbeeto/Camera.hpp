#pragma once
#include "SDL.h"
#include "Game.hpp"


class Camera {
private:
	SDL_Rect camera;

public:
	Camera(int posX = 0, int posY = 0, int width = 0, int height = 0);

	int getX();
	int getY();

	void focus(int posX, int posY);
};