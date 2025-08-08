#include "PlayerSystem.hpp"
#include "../InputManager.hpp"
#include "../Math.hpp"


PlayerSystem::PlayerSystem() : System() {}

void PlayerSystem::update() {
	for (auto entity : Game::ecs.getSystemGroup<Player, Sprite, Transform>(Game::stack.peek())) {
		Player* player = Game::ecs.getComponent<Player>(Game::stack.peek(), entity);
		Sprite* sprite = Game::ecs.getComponent<Sprite>(Game::stack.peek(), entity);
		Transform* transform = Game::ecs.getComponent<Transform>(Game::stack.peek(), entity);

		// Normal movement
		Vector2 finalAccel(0.0f, 0.0f);
		if (InputManager::keysPressed[SDLK_w]) finalAccel.y -= transform->accelConst;
		if (InputManager::keysPressed[SDLK_a]) finalAccel.x -= transform->accelConst;
		if (InputManager::keysPressed[SDLK_s]) finalAccel.y += transform->accelConst;
		if (InputManager::keysPressed[SDLK_d]) finalAccel.x += transform->accelConst;

		if (player->grappleRef != 0) {
			if (player->grappleState == GrappleState::RETURNING && player->moveToGrapple) {
				Grapple* grapple = Game::ecs.getComponent<Grapple>(Game::stack.peek(), player->grappleRef);
				Transform* gTrans = Game::ecs.getComponent<Transform>(Game::stack.peek(), player->grappleRef);
				
				double angle = Math::rad(transform->pos.getAngleToPoint(gTrans->pos));
				
				finalAccel.x += gTrans->accelConst * -sin(angle);
				finalAccel.y += gTrans->accelConst * -cos(angle);
			}
		}

		transform->accel = finalAccel;
		transform->accelMovement();

		// TODO: Add special rotational movement when grappled to wall

		Vector2 roomPos(sprite->destRect.x + sprite->tileWidth / 2, sprite->destRect.y + sprite->tileHeight / 2);
		sprite->angle = -roomPos.getAngleToPoint(InputManager::mousePosX, InputManager::mousePosY);

		// ----- Firing grappling hook ----- //
		if (player->grappleState == GrappleState::INACTIVE && player->grappleInputCopy < InputManager::mouseReleased[SDL_BUTTON_MIDDLE]) {
			fireGrapple(entity, player, transform, sprite);
			player->grappleInputCopy = InputManager::mouseReleased[SDL_BUTTON_MIDDLE];
		}

		// ----- Firing portal bullet ----- //
		if (player->portalInputCopy < InputManager::mouseReleased[SDL_BUTTON_RIGHT]) {
			firePortal(entity, player, transform, sprite);
			player->portalInputCopy = InputManager::mouseReleased[SDL_BUTTON_RIGHT];
		}
	}
}

void PlayerSystem::fireGrapple(const Entity& pEntity, Player* player, Transform* pTrans, Sprite* pSprite) {
	player->grappleState = GrappleState::SENT;

	Entity grapple = Game::ecs.createEntity(Game::stack.peek());
	player->grappleRef = grapple;

	Game::ecs.assignComponent<Sprite>(Game::stack.peek(), grapple);
	Game::ecs.assignComponent<Collision>(Game::stack.peek(), grapple);
	Game::ecs.assignComponent<Grapple>(Game::stack.peek(), grapple);
	Game::ecs.assignComponent<Transform>(Game::stack.peek(), grapple);

	Sprite* gSprite = Game::ecs.getComponent<Sprite>(Game::stack.peek(), grapple);
	*gSprite = Sprite();
	gSprite->tileWidth = 32;
	gSprite->tileHeight = 32;
	gSprite->angle = pSprite->angle;
	gSprite->srcRect = SDL_Rect(0, 64, 32, 32);
	gSprite->index = 16;
	gSprite->spriteSheet = TextureManager::loadTexture(Game::renderer, "Assets/bullets.png");

	Collision* gColl = Game::ecs.getComponent<Collision>(Game::stack.peek(), grapple);
	*gColl = Collision();
	gColl->hitWidth = 32;
	gColl->hitHeight = 32;

	Grapple* gGrapple = Game::ecs.getComponent<Grapple>(Game::stack.peek(), grapple);
	*gGrapple = Grapple();
	gGrapple->owner = pEntity;

	Transform* gTrans = Game::ecs.getComponent<Transform>(Game::stack.peek(), grapple);
	*gTrans = Transform();
	gTrans->pos = Vector2(pTrans->pos.x, pTrans->pos.y);
	gTrans->vel = Vector2(0, -2.0f);
	gTrans->accelConst = 0.15f;
	gTrans->vel.rotate(pSprite->angle);
}

void PlayerSystem::firePortal(Entity pEntity, Player* player, Transform* pTrans, Sprite* pSprite) {
	Entity portalBullet = Game::ecs.createEntity(Game::stack.peek());

	Game::ecs.assignComponent<Sprite>(Game::stack.peek(), portalBullet);
	Game::ecs.assignComponent<Collision>(Game::stack.peek(), portalBullet);
	Game::ecs.assignComponent<Transform>(Game::stack.peek(), portalBullet);
	Game::ecs.assignComponent<Bullet>(Game::stack.peek(), portalBullet);

	Sprite* pbSprite = Game::ecs.getComponent<Sprite>(Game::stack.peek(), portalBullet);
	*pbSprite = Sprite();
	pbSprite->tileWidth = 32;
	pbSprite->tileHeight = 32;
	pbSprite->angle = pSprite->angle;
	pbSprite->srcRect = SDL_Rect(0, 32, 32, 32);
	pbSprite->spriteSheet = TextureManager::loadTexture(Game::renderer, "Assets/bullets.png");

	Collision* pbColl = Game::ecs.getComponent<Collision>(Game::stack.peek(), portalBullet);
	*pbColl = Collision();
	pbColl->hitWidth = 8;
	pbColl->hitHeight = 8;

	Game::ecs.assignComponent<PortalBullet_PTag>(Game::stack.peek(), portalBullet);
	Game::ecs.assignComponent<Projectile_PTag>(Game::stack.peek(), portalBullet);

	Transform* pbTrans = Game::ecs.getComponent<Transform>(Game::stack.peek(), portalBullet);
	*pbTrans = Transform();
	pbTrans->pos = Vector2(pTrans->pos.x, pTrans->pos.y);
	pbTrans->vel = Vector2(0, -2.0f);
	pbTrans->vel.rotate(pSprite->angle);

	Bullet* pbBullet = Game::ecs.getComponent<Bullet>(Game::stack.peek(), portalBullet);
	*pbBullet = Bullet();
	pbBullet->shotBy = pEntity;
}