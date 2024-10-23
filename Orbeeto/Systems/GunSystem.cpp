#include "GunSystem.hpp"
#include "../Game.hpp"
#include "../Components/Bullet.hpp"
#include "../Components/Transform.hpp"
#include "../Components/PlayerGun.hpp"
#include "../Components/Sprite.hpp"
#include "../InputManager.hpp"
#include <iostream>


void GunSystem::init(Coordinator* coord) {
	coordinator = coord;
}

void GunSystem::update() {
	for (const Entity& entity : mEntities) {
		auto& transform = coordinator->getComponent<Transform>(entity);
		auto& gun = coordinator->getComponent<PlayerGun>(entity);
		auto& sprite = coordinator->getComponent<Sprite>(entity);

		auto& playerTrans = coordinator->getComponent<Transform>(*gun.owner);

		transform.pos = playerTrans.pos;

		Vector2 roomPos(sprite.destRect.x + sprite.tileWidth / 2, sprite.destRect.y + sprite.tileHeight / 2);
		// Player's sprite rotates to cursor
		sprite.angle = -roomPos.getAngleToPoint(InputManager::mousePosX, InputManager::mousePosY);

		if (InputManager::mousePressed[SDL_BUTTON_LEFT] && !fired) {
			Entity bullet = coordinator->createEntity();
			//std::cout << "Bullet ID: " << bullet << std::endl;

			coordinator->addComponent<Transform>(bullet, Transform{ .pos = Vector2(transform.pos.x, transform.pos.y), .vel = Vector2{ 0.0f, -3.0f } });
			coordinator->addComponent<Sprite>(bullet,
				Sprite{
					.tileWidth = 32,
					.tileHeight = 32,
					.posX = 0,
					.posY = 0,
					.angle = sprite.angle,
					.spriteSheet = TextureManager::loadTexture(Game::renderer, "Assets/bullets.png")
				});
			coordinator->addComponent<Bullet>(bullet,
				Bullet{
					.birthTime = SDL_GetTicks(),
					.damage = 1
				});

			// Setting velocity
			auto& bulletTrans = coordinator->getComponent<Transform>(bullet);
			bulletTrans.vel.rotate(sprite.angle);
			fired = true;
		}
	}
}