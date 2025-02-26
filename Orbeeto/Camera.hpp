#pragma once
#include "SDL.h"
#include "Game.hpp"
#include "Vector2.hpp"


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

	Vector2 pos = { 0.0, 0.0 };
	Vector2 vel = { 0.0, 0.0 };
	Vector2 accel = { 0.0, 0.0 };
	double accelConst = 0.07;
	double fric = -0.03;

	bool isShifting = false;
	uint64_t lastShiftStart = TimeManip::getTime();
	uint64_t lastShiftEnd = TimeManip::getTime();
	uint64_t maxShift = 2000;
	uint64_t shiftCooldown = 500;

	void focus(int posX, int posY);
	void cinematicFocus(int posX, int posY, const Vector2& entityVel, double entityAccelConst);

private:
	SDL_Rect camera;
};
