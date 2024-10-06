#include "PlayerSystem.hpp"
#include "../Components/Sprite.hpp"
#include "../Components/AccelTransform.hpp"
#include "../Components/Player.hpp"

#include "../InputManager.hpp"
#include <iostream>


void PlayerSystem::init(Coordinator* coord) {
	coordinator = coord;
}

void PlayerSystem::update() {
	for (const auto& entity : mEntities) {
		auto& sprite = coordinator->getComponent<Sprite>(entity);
		auto& accelTransform = coordinator->getComponent<AccelTransform>(entity);
		auto& player = coordinator->getComponent<Player>(entity);

		// Interpreting key presses
		Vector2 finalAccel(0.0f, 0.0f);
		if (InputManager::keysPressed[SDLK_w]) {
			finalAccel.y -= accelTransform.accelConst;
		}
		if (InputManager::keysPressed[SDLK_a]) {
			finalAccel.x -= accelTransform.accelConst;
		}
		if (InputManager::keysPressed[SDLK_s]) {
			finalAccel.y += accelTransform.accelConst;
		}
		if (InputManager::keysPressed[SDLK_d]) {
			finalAccel.x += accelTransform.accelConst;
		}

		accelTransform.accel = finalAccel;
		accelTransform.accelMovement();

		Vector2 roomPos(sprite.destRect.x + sprite.tileWidth / 2, sprite.destRect.y + sprite.tileHeight / 2);
		// Player's sprite rotates to cursor
		sprite.angle = -roomPos.getAngleToPoint(InputManager::mousePosX, InputManager::mousePosY);
	}
}