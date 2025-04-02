#include "MovementAISystem.hpp"

#include <cmath>


MovementAISystem::MovementAISystem() {}

void MovementAISystem::update() {
	for (auto& entity : Game::ecs.getSystemGroup<Transform, MovementAI>()) {
		MovementAI* mvmAI = Game::ecs.getComponent<MovementAI>(entity);
		Transform* transform = Game::ecs.getComponent<Transform>(entity);

		switch (mvmAI->ai) {
		case M_AI::CIRCLE_ACCEL:
			transform->accel.x = transform->accelConst * cos((double)TimeManip::getTime() / 1000);
			transform->accel.y = transform->accelConst * sin((double)TimeManip::getTime() / 1000);
			transform->accelMovement();
			break;

		case M_AI::FOLLOW_ENTITY:
		{
			if (mvmAI->entityRef != 0) {
				Transform* eTrans = Game::ecs.getComponent<Transform>(mvmAI->entityRef);
				transform->pos = eTrans->pos + mvmAI->distance;
			}
		}
			break;

		case M_AI::OCTOGRUNT:
		{
			if (TimeManip::getTimeDiff(mvmAI->intervalTime) >= 100) {
				double angle = 0.0 + mvmAI->angle;
				Vector2 posAdjust = { 0.0, -32.0 };
				Vector2 bulletVel = { 0.0, -4.0 };

				// Fire 8 bullets
				for (int i = 0; i < 8; i++) {
					Entity bullet = Game::ecs.createEntity();

					Game::ecs.assignComponent<Transform>(bullet);
					Game::ecs.assignComponent<Collision>(bullet);
					Game::ecs.assignComponent<Sprite>(bullet);
					Game::ecs.assignComponent<Bullet>(bullet);

					Transform* bTrans = Game::ecs.getComponent<Transform>(bullet);
					*bTrans = Transform{
						.pos = { transform->pos.x + posAdjust.x, transform->pos.y + posAdjust.y },\
						.vel = bulletVel
					};

					Collision* bColl = Game::ecs.getComponent<Collision>(bullet);
					*bColl = Collision{
						.hitWidth = 8,
						.hitHeight = 8,
					};
					bColl->physicsTags.set(PTags::PROJECTILE);
					bColl->physicsTags.set(PTags::CAN_TELEPORT);

					Sprite* bSprite = Game::ecs.getComponent<Sprite>(bullet);
					*bSprite = Sprite{
						.tileWidth = 32,
						.tileHeight = 32,
						.index = 3,
						.spriteSheet = TextureManager::loadTexture(Game::renderer, "Assets/bullets.png")
					};

					Bullet* bBullet = Game::ecs.getComponent<Bullet>(bullet);
					*bBullet = Bullet{
						.bulletAI = BulletType::STANDARD,
						.damage = 7,
					};

					angle += 45.0;
					posAdjust.rotate(angle);
					bulletVel.rotate(angle);
				}

				mvmAI->intervalTime = TimeManip::getTime();
			}
		}
			break;

		default:
			break;
		}
	}
}