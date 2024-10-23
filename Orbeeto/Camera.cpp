#include "Camera.hpp"
#include "Components/Transform.hpp"
#include "WindowManager.hpp"


Camera::Camera(int posX, int posY, int width, int height) {
	camera = SDL_Rect(posX, posY, width, height);
}

int Camera::getX() {
	return camera.x;
}

int Camera::getY() {
	return camera.y;
}

void Camera::focus(int posX, int posY) {
	camera.x = posX - WindowManager::SCREENWIDTH / 2;
	camera.y = posY - WindowManager::SCREENHEIGHT / 2;
}