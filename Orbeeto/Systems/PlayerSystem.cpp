#include "PlayerSystem.hpp"
#include "../Game.hpp"
#include "../Components/Sprite.hpp"
#include "../Components/Collision.hpp"
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

		if (InputManager::mousePressed[SDL_BUTTON_LEFT]) {
			Entity bullet = coordinator->createEntity();

			coordinator->addComponent<AccelTransform>(bullet,
				AccelTransform{
					.pos = Vector2(accelTransform.pos.x + 100, accelTransform.pos.y)
				}
			);
			coordinator->addComponent<Collision>(bullet,
				Collision{
					16,
					16,
					Vector2(accelTransform.pos.x + 100, accelTransform.pos.y),
					false,
					false,
					true,
					false
				}
			);
			coordinator->addComponent<Sprite>(bullet,
				Sprite{
					.tileWidth = 32,
					.tileHeight = 32,
					.posX = 0,
					.posY = 0,
					.spriteSheet = TextureManager::loadTexture(Game::renderer, "Assets/bullets.png"),
				}
			);
		}

		accelTransform.accel = finalAccel;
		accelTransform.accelMovement();

		Vector2 roomPos(sprite.destRect.x + sprite.tileWidth / 2, sprite.destRect.y + sprite.tileHeight / 2);
		// Player's sprite rotates to cursor
		sprite.angle = -roomPos.getAngleToPoint(InputManager::mousePosX, InputManager::mousePosY);
	}
}