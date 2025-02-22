#include "PlayerSystem.hpp"
#include "../InputManager.hpp"


PlayerSystem::PlayerSystem() : System() {}

void PlayerSystem::update() {
	for (auto entity : Game::ecs.getSystemGroup<Player, Sprite, Transform>()) {
		Player* player = Game::ecs.getComponent<Player>(entity);
		Sprite* sprite = Game::ecs.getComponent<Sprite>(entity);
		Transform* transform = Game::ecs.getComponent<Transform>(entity);

		// Normal movement
		Vector2 finalAccel(0.0f, 0.0f);
		if (InputManager::keysPressed[SDLK_w]) finalAccel.y -= transform->accelConst;
		if (InputManager::keysPressed[SDLK_a]) finalAccel.x -= transform->accelConst;
		if (InputManager::keysPressed[SDLK_s]) finalAccel.y += transform->accelConst;
		if (InputManager::keysPressed[SDLK_d]) finalAccel.x += transform->accelConst;

		if (player->grappleRef != 0) {
			if (player->grappleState == GrappleState::RETURNING && player->moveToGrapple) {
				Grapple* grapple = Game::ecs.getComponent<Grapple>(player->grappleRef);
				Transform* gTrans = Game::ecs.getComponent<Transform>(player->grappleRef);
				double angle = transform->pos.getAngleToPoint(gTrans->pos);
				
				if (!player->cancelVelFlag) {
					std::cout << "Vel canceled! \n";
					transform->vel = { 0, 0 };
					player->cancelVelFlag = true;
				}

				std::cout << "Return angle: " << angle << std::endl;
				finalAccel.x += gTrans->accelConst * cos(-angle);
				finalAccel.y += gTrans->accelConst * sin(-angle);
			}
			else {
				player->cancelVelFlag = false;
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

	Entity grapple = Game::ecs.createEntity();
	player->grappleRef = grapple;

	Game::ecs.assignComponent<Sprite>(grapple);
	Game::ecs.assignComponent<Collision>(grapple);
	Game::ecs.assignComponent<Grapple>(grapple);
	Game::ecs.assignComponent<Transform>(grapple);

	Sprite* gSprite = Game::ecs.getComponent<Sprite>(grapple);
	*gSprite = Sprite{
		.tileWidth = 32,
		.tileHeight = 32,
		.angle = pSprite->angle,
		.srcRect = SDL_Rect(0, 64, 32, 32),
		.spriteSheet = TextureManager::loadTexture(Game::renderer, "Assets/bullets.png"),
	};

	Collision* gColl = Game::ecs.getComponent<Collision>(grapple);
	*gColl = Collision{
		.hitWidth = 32,
		.hitHeight = 32,
		.physicsTags = {"grapple"},
	};

	Grapple* gGrapple = Game::ecs.getComponent<Grapple>(grapple);
	*gGrapple = Grapple{
		.owner = pEntity
	};

	Transform* gTrans = Game::ecs.getComponent<Transform>(grapple);
	*gTrans = Transform{
		.pos = Vector2(pTrans->pos.x, pTrans->pos.y),
		.vel = Vector2(0, -2.0f),
		.accelConst = 0.15f,
	};
	gTrans->vel.rotate(pSprite->angle);
}

void PlayerSystem::firePortal(Entity pEntity, Player* player, Transform* pTrans, Sprite* pSprite) {
	Entity portalBullet = Game::ecs.createEntity();

	Game::ecs.assignComponent<Sprite>(portalBullet);
	Game::ecs.assignComponent<Collision>(portalBullet);
	Game::ecs.assignComponent<Transform>(portalBullet);
	Game::ecs.assignComponent<Bullet>(portalBullet);

	Sprite* pbSprite = Game::ecs.getComponent<Sprite>(portalBullet);
	*pbSprite = Sprite{
		.tileWidth = 32,
		.tileHeight = 32,
		.angle = pSprite->angle,
		.srcRect = SDL_Rect(0, 32, 32, 32),
		.spriteSheet = TextureManager::loadTexture(Game::renderer, "Assets/bullets.png"),
	};

	Collision* pbColl = Game::ecs.getComponent<Collision>(portalBullet);
	*pbColl = Collision{
		.hitWidth = 8,
		.hitHeight = 8,
		.physicsTags = {"portalBullet", "projectile"},
	};

	Transform* pbTrans = Game::ecs.getComponent<Transform>(portalBullet);
	*pbTrans = Transform{
		.pos = Vector2(pTrans->pos.x, pTrans->pos.y),
		.vel = Vector2(0, -2.0f),
	};
	pbTrans->vel.rotate(pSprite->angle);

	Bullet* pbBullet = Game::ecs.getComponent<Bullet>(portalBullet);
	*pbBullet = Bullet{
		.shotBy = pEntity,
	};
}