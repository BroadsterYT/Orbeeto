#include "Camera.hpp"
#include "Components/Transform.hpp"
#include "WindowManager.hpp"

#include <algorithm>
#include <cmath>
#include "SDL_stdinc.h"
#include "Math.hpp"


Camera::Camera(int posX, int posY, int width, int height) {
	camera = SDL_Rect(posX, posY, width, height);
}

int Camera::getX() {
	return camera.x;
}

int Camera::getY() {
	return camera.y;
}

int Camera::getWidth() {
	return camera.w;
}

void Camera::setWidth(int newWidth) {
	camera.w = newWidth;
}

int Camera::getHeight() {
	return camera.h;
}

void Camera::setHeight(int newHeight) {
	camera.h = newHeight;
}

void Camera::printDetails() {
	std::cout << "Pos x: " << camera.x << std::endl;
	std::cout << "Pos y: " << camera.y << std::endl;
	std::cout << "width: " << camera.w << std::endl;
	std::cout << "height: " << camera.h << std::endl << std::endl;
}

void Camera::focus(int posX, int posY) {
	camera.x = posX - WindowManager::SCREENWIDTH / 2;
	camera.y = posY - WindowManager::SCREENHEIGHT / 2;
}

void Camera::cinematicFocus(int posX, int posY, double accelC) {
	// https://www.desmos.com/calculator/3y1viny0hg
	double tanFuncX = tan(M_PI / (2.0 * (double)WindowManager::SCREENWIDTH) * ((double)camera.x - (double)posX + (double)WindowManager::SCREENWIDTH) - M_PI / 4.0);
	double tanFuncY = tan(M_PI / (2.0 * (double)WindowManager::SCREENHEIGHT) * ((double)camera.y - (double)posY + (double)WindowManager::SCREENHEIGHT) - M_PI / 4.0);

	double mult = 6.0;
	double clampLimitX = accelC * 2;
	double clampLimitY = clampLimitX;

	double tempAccelX = std::clamp(-mult * pow(tanFuncX, 3.0), -clampLimitX, clampLimitX);
	double tempAccelY = std::clamp(-mult * pow(tanFuncY, 3.0), -clampLimitY, clampLimitY);

	// Prevents movement along tangent outside of first period if tp takes player grater than window borders
	if (-3.0 * (double)WindowManager::SCREENWIDTH / 2.0 + (double)posX > camera.x) {
		tempAccelX = clampLimitX;
	}
	else if ((double)WindowManager::SCREENWIDTH / 2.0 + (double)posX < camera.x) {
		tempAccelX = -clampLimitX;
	}

	if (-3.0 * (double)WindowManager::SCREENHEIGHT / 2.0 + (double)posY > camera.y) {
		tempAccelY = clampLimitY;
	}
	else if ((double)WindowManager::SCREENHEIGHT / 2.0 + (double)posY < camera.y) {
		tempAccelY = -clampLimitY;
	}

	accel.x = tempAccelX;
	accel.y = tempAccelY;

	accel.x += vel.x * fric;
	accel.y += vel.y * fric;
	vel += accel * TimeManip::getDeltaAdjuster();
	pos += vel * TimeManip::getDeltaAdjuster() + accel * accelConst;

	camera.x = pos.x;
	camera.y = pos.y;
}