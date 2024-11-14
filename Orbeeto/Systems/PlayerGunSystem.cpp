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

		// Firing bullets
		if (InputManager::mousePressed[SDL_BUTTON_LEFT]) {
			Entity bullet = Game::ecs.createEntity();

			Game::ecs.assignComponent<Sprite>(bullet);
			Game::ecs.assignComponent<Transform>(bullet);
			Game::ecs.assignComponent<Bullet>(bullet);
			//Game::ecs.assignComponent<Collision>(bullet);

			Sprite* bSprite = Game::ecs.getComponent<Sprite>(bullet);
			*bSprite = Sprite{
				.tileWidth = 32,
				.tileHeight = 32,
				.spriteSheet = TextureManager::loadTexture(Game::renderer, "Assets/bullets.png")
			};
			
			Transform* bTransform = Game::ecs.getComponent<Transform>(bullet);
			*bTransform = Transform{ 
				.pos = Vector2(ownerTrans->pos.x, ownerTrans->pos.y),
				.vel = Vector2(0, 2.0f)
			};

			Bullet* bBullet = Game::ecs.getComponent<Bullet>(bullet);
			*bBullet = Bullet{ .damage = 5 };

			/*Collision* bCollision = Game::ecs.getComponent<Collision>(bullet);
			*bCollision = Collision{
				.hitWidth = 8,
				.hitHeight = 8,
				.hitPos = Vector2(ownerTrans->pos.x, ownerTrans->pos.y),
				.isProj = true
			};*/
		}

		// Rotating to cursor
		Vector2 roomPos(sprite->destRect.x + sprite->tileWidth / 2, sprite->destRect.y + sprite->tileHeight / 2);
		sprite->angle = -roomPos.getAngleToPoint(InputManager::mousePosX, InputManager::mousePosY);
	}
}