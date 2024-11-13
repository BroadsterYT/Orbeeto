#include "PlayerSystem.hpp"
#include "../InputManager.hpp"

#include "../Components/Player.hpp"
#include "../Components/Sprite.hpp"
#include "../Components/Transform.hpp"


PlayerSystem::PlayerSystem() : System() {}

void PlayerSystem::update() {
	for (auto& entity : Game::ecs.getSystemGroup<Player, Sprite, Transform>()) {
		Sprite* sprite = Game::ecs.getComponent<Sprite>(entity);
		Transform* transform = Game::ecs.getComponent<Transform>(entity);

		Vector2 finalAccel(0.0f, 0.0f);
		if (InputManager::keysPressed[SDLK_w]) finalAccel.y -= transform->accelConst;
		if (InputManager::keysPressed[SDLK_a]) finalAccel.x -= transform->accelConst;
		if (InputManager::keysPressed[SDLK_s]) finalAccel.y += transform->accelConst;
		if (InputManager::keysPressed[SDLK_d]) finalAccel.x += transform->accelConst;

		transform->accel = finalAccel;
		transform->accelMovement();

		Vector2 roomPos(sprite->destRect.x + sprite->tileWidth / 2, sprite->destRect.y + sprite->tileHeight / 2);
		sprite->angle = -roomPos.getAngleToPoint(InputManager::mousePosX, InputManager::mousePosY);
	}
}