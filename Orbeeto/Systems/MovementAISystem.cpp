#include "MovementAISystem.hpp"
#include <random>
#include <cmath>


MovementAISystem::MovementAISystem() {}

void MovementAISystem::update() {
	for (auto& entity : Game::ecs.getSystemGroup<Transform, MovementAI>(Game::stack.peek())) {
		MovementAI* mvmAI = Game::ecs.getComponent<MovementAI>(Game::stack.peek(), entity);
		Transform* trans = Game::ecs.getComponent<Transform>(Game::stack.peek(), entity);

		switch (mvmAI->ai) {
		case M_AI::CIRCLE_ACCEL:
			trans->accel.x = trans->accelConst * cos(TimeManip::getSDLTime() / 1000);
			trans->accel.y = trans->accelConst * sin(TimeManip::getSDLTime() / 1000);
			trans->accelMovement();
			break;

		case M_AI::FOLLOW_ENTITY:
		{
			if (mvmAI->entityRef != 0) {
				Transform* eTrans = Game::ecs.getComponent<Transform>(Game::stack.peek(), mvmAI->entityRef);
				trans->pos = eTrans->pos + mvmAI->distance;
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
					Entity bullet = Game::ecs.createEntity(Game::stack.peek());

					Game::ecs.assignComponent<Transform>(Game::stack.peek(), bullet);
					Game::ecs.assignComponent<Collision>(Game::stack.peek(), bullet);
					Game::ecs.assignComponent<Sprite>(Game::stack.peek(), bullet);
					Game::ecs.assignComponent<Bullet>(Game::stack.peek(), bullet);

					Transform* bTrans = Game::ecs.getComponent<Transform>(Game::stack.peek(), bullet);
					bTrans->pos = { trans->pos.x + posAdjust.x, trans->pos.y + posAdjust.y };
					bTrans->vel = bulletVel;

					Collision* bColl = Game::ecs.getComponent<Collision>(Game::stack.peek(), bullet);
					bColl->hitWidth = 8;
					bColl->hitHeight = 8;

					bColl->physicsTags.set(PTags::PROJECTILE);
					bColl->physicsTags.set(PTags::E_PROJECTILE);
					bColl->physicsTags.set(PTags::CAN_TELEPORT);

					Sprite* bSprite = Game::ecs.getComponent<Sprite>(Game::stack.peek(), bullet);
					bSprite->tileWidth = 32;
					bSprite->tileHeight = 32;
					bSprite->index = 3;
					bSprite->spriteSheet = TextureManager::loadTexture(Game::renderer, "Assets/bullets.png");

					Bullet* bBullet = Game::ecs.getComponent<Bullet>(Game::stack.peek(), bullet);
					bBullet->bulletAI = BulletType::STANDARD;
					bBullet->damage = 7;

					angle += 45.0;
					posAdjust.rotate(angle);
					bulletVel.rotate(angle);
				}

				mvmAI->intervalTime = TimeManip::getTime();
			}
		}
			break;

		case M_AI::TEXT_TREMBLE:
		{
			mvmAI->distance.x = 0;  // Using distance as the random difference of position
			mvmAI->distance.y = 0;

			std::uniform_real_distribution<float> randMag(0.0f, mvmAI->mag);
			mvmAI->distance.x = randMag(TimeManip::prng);
			mvmAI->distance.y = randMag(TimeManip::prng);

			trans->pos = mvmAI->vec1 + mvmAI->distance;  
		}
			break;

		default:
			break;
		}
	}
}