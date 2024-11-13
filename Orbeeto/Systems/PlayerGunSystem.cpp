#include "PlayerGunSystem.hpp"
#include "../InputManager.hpp"


PlayerGunSystem::PlayerGunSystem() : System() {}

void PlayerGunSystem::update() {
	for (Entity& entity : Game::ecs.getSystemGroup<PlayerGun, Sprite, Transform>()) {
		PlayerGun* gun = Game::ecs.getComponent<PlayerGun>(entity);
		Sprite* sprite = Game::ecs.getComponent<Sprite>(entity);
		Transform* transform = Game::ecs.getComponent<Transform>(entity);

		Transform* ownerTrans = Game::ecs.getComponent<Transform>(*gun->owner);

		transform->pos = ownerTrans->pos;

		Vector2 roomPos(sprite->destRect.x + sprite->tileWidth / 2, sprite->destRect.y + sprite->tileHeight / 2);
		sprite->angle = -roomPos.getAngleToPoint(InputManager::mousePosX, InputManager::mousePosY);
	}
}