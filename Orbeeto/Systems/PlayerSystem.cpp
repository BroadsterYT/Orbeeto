#include "PlayerSystem.hpp"
#include "../Game.hpp"
#include "../Components/Sprite.hpp"
#include "../Components/Collision.hpp"
#include "../Components/Transform.hpp"
#include "../Components/Player.hpp"

#include "../InputManager.hpp"
#include <iostream>


void PlayerSystem::init(Coordinator* coord) {
	coordinator = coord;
}

void PlayerSystem::update() {
	for (const auto& entity : mEntities) {
		auto& accelTrans = coordinator->getComponent<Transform>(entity);
		auto& sprite = coordinator->getComponent<Sprite>(entity);
		auto& player = coordinator->getComponent<Player>(entity);

		// Interpreting key presses
		Vector2 finalAccel(0.0f, 0.0f);
		if (InputManager::keysPressed[SDLK_w]) {
			finalAccel.y -= accelTrans.accelConst;
		}
		if (InputManager::keysPressed[SDLK_a]) {
			finalAccel.x -= accelTrans.accelConst;
		}
		if (InputManager::keysPressed[SDLK_s]) {
			finalAccel.y += accelTrans.accelConst;
		}
		if (InputManager::keysPressed[SDLK_d]) {
			finalAccel.x += accelTrans.accelConst;
		}

		accelTrans.accel = finalAccel;
		accelTrans.accelMovement();

		Vector2 roomPos(sprite.destRect.x + sprite.tileWidth / 2, sprite.destRect.y + sprite.tileHeight / 2);
		// Player's sprite rotates to cursor
		sprite.angle = -roomPos.getAngleToPoint(InputManager::mousePosX, InputManager::mousePosY);
	}
}