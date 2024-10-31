#pragma once
#include "../ECS.hpp"
#include "../InputManager.hpp"

#include "../Components/Player.hpp"
#include "../Components/Sprite.hpp"
#include "../Components/Transform.hpp"


void PlayerSystem(ECS& ecs) {
	for (auto& entity : ecs.getSystemGroup<Player, Sprite, Transform>()) {
		Sprite* sprite = ecs.getComponent<Sprite>(entity);
		Transform* transform = ecs.getComponent<Transform>(entity);

		Vector2 finalAccel(0.0f, 0.0f);
		if (InputManager::keysPressed[SDLK_w]) finalAccel.y -= transform->accelConst;
		if (InputManager::keysPressed[SDLK_a]) finalAccel.x -= transform->accelConst;
		if (InputManager::keysPressed[SDLK_s]) finalAccel.y += transform->accelConst;
		if (InputManager::keysPressed[SDLK_d]) finalAccel.x += transform->accelConst;

		transform->accel = finalAccel;
		transform->accelMovement();

		//ecs.destroyEntity(entity);
	}
}