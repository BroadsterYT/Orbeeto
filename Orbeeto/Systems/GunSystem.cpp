#include "GunSystem.hpp"
#include "../Game.hpp"
#include "../Components/AccelTransform.hpp"
#include "../Components/PlayerGun.hpp"
#include "../Components/Sprite.hpp"
#include "../InputManager.hpp"
#include <iostream>


void GunSystem::init(Coordinator* coord) {
	coordinator = coord;
}

void GunSystem::update() {
	for (const Entity& entity : mEntities) {
		auto& accelTrans = coordinator->getComponent<AccelTransform>(entity);
		auto& gun = coordinator->getComponent<PlayerGun>(entity);
		auto& sprite = coordinator->getComponent<Sprite>(entity);

		auto& playerTrans = coordinator->getComponent<AccelTransform>(*gun.owner);

		accelTrans.pos = playerTrans.pos;

		Vector2 roomPos(sprite.destRect.x + sprite.tileWidth / 2, sprite.destRect.y + sprite.tileHeight / 2);
		// Player's sprite rotates to cursor
		sprite.angle = -roomPos.getAngleToPoint(InputManager::mousePosX, InputManager::mousePosY);

		if (InputManager::mousePressed[SDL_BUTTON_LEFT]) {
			Entity bullet = coordinator->createEntity();
			std::cout << "Bullet ID: " << bullet << std::endl;

			coordinator->addComponent<AccelTransform>(bullet, AccelTransform{ .pos = Vector2(accelTrans.pos.x, accelTrans.pos.y) });
			coordinator->addComponent<Sprite>(bullet,
				Sprite{
					.tileWidth = 32,
					.tileHeight = 32,
					.posX = 0,
					.posY = 0,
					.spriteSheet = TextureManager::loadTexture(Game::renderer, "Assets/bullets.png")
				}
				);
		}
	}
}