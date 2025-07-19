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
			// TODO: Complete at later date, need to remove to update MovementAI struct
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

		case M_AI::TEXT_WAVE:
		{
			trans->pos.y = mvmAI->vec1.y + mvmAI->mag * sin(10 * mvmAI->intervalTime);
			mvmAI->intervalTime += TimeManip::deltaTime;
		}
			break;

		default:
			break;
		}
	}
}