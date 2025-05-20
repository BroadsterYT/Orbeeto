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

void Camera::cinematicFocus(Entity entity) {
	Transform* trans = Game::ecs.getComponent<Transform>(Game::stack.peek(), entity);
	Collision* coll = Game::ecs.getComponent<Collision>(Game::stack.peek(), entity);
	
	Vector2 cameraVec = { (double)camera.x, (double)camera.y };
	Vector2 targetVec = {
		std::floor(trans->pos.x - WindowManager::SCREENWIDTH / 2),
		std::floor(trans->pos.y - WindowManager::SCREENHEIGHT / 2)
	};

	if (lastTpCheck != coll->tpFlag) {
		tpToggle.setState(false);
		tpToggle.setWeight(0.0);
		tpToggle.setValue1(cameraVec);
		tpToggle.toggle();

		lastTpCheck = coll->tpFlag;
	}

	tpToggle.setValue2(targetVec);

	camera.x = tpToggle.getValue().x;
	camera.y = tpToggle.getValue().y;
}
