#include "PlayerGunSystem.hpp"


PlayerGunSystem::PlayerGunSystem() : System() {}

void PlayerGunSystem::update() {
	for (Entity& entity : Game::ecs.getSystemGroup<PlayerGun, Sprite, Transform>()) {
		PlayerGun* gun = Game::ecs.getComponent<PlayerGun>(entity);
		Sprite* sprite = Game::ecs.getComponent<Sprite>(entity);
		Transform* transform = Game::ecs.getComponent<Transform>(entity);
		Transform* ownerTrans = Game::ecs.getComponent<Transform>(*gun->owner);  // Transform component of player

		transform->pos = ownerTrans->pos;

		// Rotating gun to cursor
		Vector2 roomPos(sprite->destRect.x + sprite->tileWidth / 2, sprite->destRect.y + sprite->tileHeight / 2);
		double rotAngle = -roomPos.getAngleToPoint(InputManager::mousePosX, InputManager::mousePosY);
		sprite->angle = rotAngle;

		// Firing bullets
		if (InputManager::mousePressed[SDL_BUTTON_LEFT] && gun->cooldown >= gun->maxCooldown) {
			fireBullet(ownerTrans, 0, rotAngle);
			gun->cooldown = 0;
		}
		gun->cooldown++;
		if (gun->cooldown > gun->maxCooldown) gun->cooldown = gun->maxCooldown;
	}
}

void PlayerGunSystem::fireBullet(Transform* ownerTrans, const int bulletId, const double rotAngle) {
	Entity bullet = Game::ecs.createEntity();

	Game::ecs.assignComponent<Sprite>(bullet);
	Game::ecs.assignComponent<Transform>(bullet);
	Game::ecs.assignComponent<Bullet>(bullet);
	Game::ecs.assignComponent<Collision>(bullet);

	// ----- Sprite ----- //
	Sprite* bSprite = Game::ecs.getComponent<Sprite>(bullet);
	*bSprite = Sprite{
		.tileWidth = 32,
		.tileHeight = 32,
		.angle = rotAngle,
		.spriteSheet = TextureManager::loadTexture(Game::renderer, "Assets/bullets.png"),
	};

	// ----- Transform ----- //
	Transform* bTransform = Game::ecs.getComponent<Transform>(bullet);

	// Placing bullet at offset of barrel
	int offsetX = 21;
	int offsetY = 30;
	double barrelOffsetX = -offsetX * cos(-rotAngle * M_PI / 180) - offsetY * sin(-rotAngle * M_PI / 180);
	double barrelOffsetY = offsetX * sin(-rotAngle * M_PI / 180) - offsetY * cos(-rotAngle * M_PI / 180);

	*bTransform = Transform{
		.pos = Vector2(ownerTrans->pos.x + barrelOffsetX, ownerTrans->pos.y + barrelOffsetY)
	};

	// ----- Bullet ----- //
	Bullet* bBullet = Game::ecs.getComponent<Bullet>(bullet);

	// ----- Collision ----- //
	Collision* bColl = Game::ecs.getComponent<Collision>(bullet);
	*bColl = Collision{
		.hitWidth = 8,
		.hitHeight = 8,
		.hitPos = Vector2(ownerTrans->pos.x + barrelOffsetX, ownerTrans->pos.y + barrelOffsetY),
		.physicsTags = {"projectile"}
	};

	switch (bulletId) {
	case 0:
		bTransform->vel = Vector2(0.0f, -2.0f);
		bTransform->vel.rotate(rotAngle);
		//bTransform->vel += ownerTrans->vel;
		break;

	default:
		bTransform->vel = Vector2(0.0f, -2.0f);
		bTransform->vel.rotate(rotAngle);
		//bTransform->vel += ownerTrans->vel;
		break;
	}
}