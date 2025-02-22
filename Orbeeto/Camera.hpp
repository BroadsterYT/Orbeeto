#pragma once
#include "SDL.h"
#include "Game.hpp"


class Camera {
public:
	Camera(int posX = 0, int posY = 0, int width = 0, int height = 0);

	int getX();
	int getY();
	
	int getWidth();
	void setWidth(int newWidth);
	int getHeight();
	void setHeight(int newHeight);

	void printDetails();

	void focus(int posX, int posY);

private:
	SDL_Rect camera;
};