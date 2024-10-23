#pragma once
#include "../ECS.hpp"
#include "../InputManager.hpp"

#include "../Components/Player.hpp"
#include "../Components/Sprite.hpp"
#include "../Components/Transform.hpp"


void PlayerSystem(Scene& scene) {
	for (EntityID entity : SceneView<Sprite, Transform, Player>(scene)) {
		Player* player = scene.get<Player>(entity);
		Sprite* sprite = scene.get<Sprite>(entity);
		Transform* transform = scene.get<Transform>(entity);

		Vector2 finalAccel{ 0.0f, 0.0f };
		if (InputManager::keysPressed[SDLK_w]) {
			finalAccel.y -= transform->accelConst;
		}
		if (InputManager::keysPressed[SDLK_a]) {
			finalAccel.x -= transform->accelConst;
		}
		if (InputManager::keysPressed[SDLK_s]) {
			finalAccel.y += transform->accelConst;
		}
		if (InputManager::keysPressed[SDLK_d]) {
			finalAccel.x += transform->accelConst;
		}

		// Rotate player to cursor
		Vector2 roomPos(sprite->destRect.x + sprite->tileWidth / 2, sprite->destRect.y + sprite->tileHeight / 2);
		sprite->angle = -roomPos.getAngleToPoint(InputManager::mousePosX, InputManager::mousePosY);

		transform->accel = finalAccel;
		transform->accelMovement();
	}
}