#pragma once
#include "System.hpp"


class PlayerGunSystem : public System {
public:
	PlayerGunSystem() : System() {}

	void update() {
		for (Entity& entity : Game::ecs.getSystemGroup<PlayerGun, Sprite, Transform>()) {
			// Gun components
			PlayerGun* gun = Game::ecs.getComponent<PlayerGun>(entity);
			Sprite* sprite = Game::ecs.getComponent<Sprite>(entity);
			Transform* transform = Game::ecs.getComponent<Transform>(entity);

			// Owner components
			Transform* ownerTrans = Game::ecs.getComponent<Transform>(*gun->owner);


			transform->pos = ownerTrans->pos;


			// Rotating to cursor
			Vector2 roomPos(sprite->destRect.x + sprite->tileWidth / 2, sprite->destRect.y + sprite->tileHeight / 2);
			double rotAngle = -roomPos.getAngleToPoint(InputManager::mousePosX, InputManager::mousePosY);
			sprite->angle = rotAngle;


			// Firing bullets
			if (gun->isLeft && InputManager::mousePressed[SDL_BUTTON_LEFT] && gun->cooldown >= gun->maxCooldown) {
				Entity bullet = Game::ecs.createEntity();

				Game::ecs.assignComponent<Sprite>(bullet);
				Game::ecs.assignComponent<Transform>(bullet);
				Game::ecs.assignComponent<Bullet>(bullet);


				Sprite* bSprite = Game::ecs.getComponent<Sprite>(bullet);
				*bSprite = Sprite{
					.tileWidth = 32,
					.tileHeight = 32,
					.spriteSheet = TextureManager::loadTexture(Game::renderer, "Assets/bullets.png")
				};


				// Placing bullet at offset of barrel
				int offsetX = 21;
				int offsetY = 30;
				double barrelOffsetX = -offsetX * cos(-rotAngle * M_PI / 180) - offsetY * sin(-rotAngle * M_PI / 180);
				double barrelOffsetY = offsetX * sin(-rotAngle * M_PI / 180) - offsetY * cos(-rotAngle * M_PI / 180);

				Transform* bTransform = Game::ecs.getComponent<Transform>(bullet);
				*bTransform = Transform{
					.pos = Vector2(ownerTrans->pos.x + barrelOffsetX, ownerTrans->pos.y + barrelOffsetY),
					.vel = Vector2(0, -2.0f)
				};
				bTransform->vel.rotate(rotAngle);
				bTransform->vel += ownerTrans->vel;


				Bullet* bBullet = Game::ecs.getComponent<Bullet>(bullet);
				*bBullet = Bullet{ .damage = 5 };


				gun->cooldown = 0;
			}

			gun->cooldown++;
		}
	}
};