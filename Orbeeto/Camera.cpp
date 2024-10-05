#include "Camera.hpp"
#include "Components/AccelTransform.hpp"
#include "WindowManager.hpp"


Camera::Camera(Coordinator* coord, int posX, int posY, int width, int height) {
	coordinator = coord;
	camera = SDL_Rect(posX, posY, width, height);
}

int Camera::getX() {
	return camera.x;
}

int Camera::getY() {
	return camera.y;
}

void Camera::focus(const Entity& ref) {
	auto& accelTransform = coordinator->getComponent<AccelTransform>(ref);

	camera.x = accelTransform.pos.x - WindowManager::SCREENWIDTH / 2;
	camera.y = accelTransform.pos.y - WindowManager::SCREENHEIGHT / 2;
}