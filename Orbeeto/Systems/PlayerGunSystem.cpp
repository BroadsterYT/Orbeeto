#include "PlayerGunSystem.hpp"


PlayerGunSystem::PlayerGunSystem() : System() {}

void PlayerGunSystem::update() {
	for (Entity& entity : Game::ecs.getSystemGroup<PlayerGun, Sprite, Transform>(Game::stack.peek())) {
		PlayerGun* gun = Game::ecs.getComponent<PlayerGun>(Game::stack.peek(), entity);
		Sprite* sprite = Game::ecs.getComponent<Sprite>(Game::stack.peek(), entity);
		Transform* transform = Game::ecs.getComponent<Transform>(Game::stack.peek(), entity);
		Transform* ownerTrans = Game::ecs.getComponent<Transform>(Game::stack.peek(), gun->owner);  // Transform component of player

		transform->pos = ownerTrans->pos;

		// Rotating gun to cursor
		Vector2 roomPos(sprite->destRect.x + sprite->tileWidth / 2, sprite->destRect.y + sprite->tileHeight / 2);
		double rotAngle = -roomPos.getAngleToPoint(InputManager::mousePosX, InputManager::mousePosY);
		sprite->angle = rotAngle;

		// Firing bullets
		if (InputManager::mousePressed[SDL_BUTTON_LEFT] && TimeManip::getTimeDiff(gun->lastShot) >= gun->cooldown) {
			fireBullet(ownerTrans, 0, rotAngle, gun->isLeft);
			gun->lastShot = TimeManip::getTime();
		}
	}
}

void PlayerGunSystem::fireBullet(Transform* ownerTrans, const int bulletId, const double rotAngle, const bool isLeft) {
	Entity bullet = Game::ecs.createEntity(Game::stack.peek());

	Game::ecs.assignComponent<Sprite>(Game::stack.peek(), bullet);
	Game::ecs.assignComponent<Transform>(Game::stack.peek(), bullet);
	Game::ecs.assignComponent<Bullet>(Game::stack.peek(), bullet);
	Game::ecs.assignComponent<Collision>(Game::stack.peek(), bullet);

	// ----- Sprite ----- //
	Sprite* bSprite = Game::ecs.getComponent<Sprite>(Game::stack.peek(), bullet);
	*bSprite = Sprite(0, 0, 32, 32);
	bSprite->angle = rotAngle;
	bSprite->spriteSheet = TextureManager::loadTexture(Game::renderer, "Assets/bullets.png");

	// ----- Transform ----- //
	Transform* bTransform = Game::ecs.getComponent<Transform>(Game::stack.peek(), bullet);

	// Placing bullet at offset of barrel
	int offsetX = 21;
	int offsetY = 30;
	double barrelOffsetX = -offsetX * cos(-rotAngle * M_PI / 180) - offsetY * sin(-rotAngle * M_PI / 180);
	double barrelOffsetY = offsetX * sin(-rotAngle * M_PI / 180) - offsetY * cos(-rotAngle * M_PI / 180);

	if (!isLeft) {
		barrelOffsetX = offsetX * cos(-rotAngle * M_PI / 180) - offsetY * sin(-rotAngle * M_PI / 180);
		barrelOffsetY = -offsetX * sin(-rotAngle * M_PI / 180) - offsetY * cos(-rotAngle * M_PI / 180);
	}

	*bTransform = Transform();
	bTransform->pos = Vector2(ownerTrans->pos.x + barrelOffsetX, ownerTrans->pos.y + barrelOffsetY);

	// ----- Bullet ----- //
	Bullet* bBullet = Game::ecs.getComponent<Bullet>(Game::stack.peek(), bullet);
	*bBullet = Bullet();
	bBullet->bulletAI = BulletType::STANDARD;

	// ----- Collision ----- //
	Collision* bColl = Game::ecs.getComponent<Collision>(Game::stack.peek(), bullet);
	*bColl = Collision();
	bColl->hitWidth = 8;
	bColl->hitHeight = 8;
	bColl->hitPos = Vector2(ownerTrans->pos.x + barrelOffsetX, ownerTrans->pos.y + barrelOffsetY);

	bColl->physicsTags.set(PTags::PROJECTILE);
	bColl->physicsTags.set(PTags::CAN_TELEPORT);

	switch (bulletId) {
	case BulletType::STANDARD: // Regular bullet
		bTransform->vel = Vector2(0.0f, -3.0f);
		bTransform->vel.rotate(rotAngle);
		bTransform->vel += ownerTrans->vel;
		break;

	default:
		bTransform->vel = Vector2(0.0f, -3.0f);
		bTransform->vel.rotate(rotAngle);
		//bTransform->vel += ownerTrans->vel;
		break;
	}
}