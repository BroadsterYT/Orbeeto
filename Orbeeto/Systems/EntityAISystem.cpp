#include "EntityAISystem.hpp"
#include <cassert>
#include <random>
#include <cmath>


EntityAISystem::EntityAISystem() {}

void EntityAISystem::update() {
	for (auto& entity : Game::ecs.getSystemGroup<Transform, EntityAI>(Game::stack.peek())) {
		EntityAI* mvmAI = Game::ecs.getComponent<EntityAI>(Game::stack.peek(), entity);
		Transform* trans = Game::ecs.getComponent<Transform>(Game::stack.peek(), entity);

		switch (mvmAI->ai) {
		case M_AI::circle_accel:
			/*trans->accel.x = trans->accelConst * cos(TimeManip::getSDLTime() / 1000);
			trans->accel.y = trans->accelConst * sin(TimeManip::getSDLTime() / 1000);
			trans->accelMovement();*/
			break;

		case M_AI::follow_entity: {
			auto* feAI = Game::ecs.getComponent<FollowEntityAI>(Game::stack.peek(), entity);
			assert(feAI && "Error: Entity must have FollowEntityAI component.");

			auto* eTrans = Game::ecs.getComponent<Transform>(Game::stack.peek(), feAI->entityRef);
			trans->pos = eTrans->pos + feAI->distOffset;

			break;
		}

		case M_AI::two_point_shift: {
			auto* tps = Game::ecs.getComponent<TwoPointShiftAI>(Game::stack.peek(), entity);
			assert(tps && "Error: Entity must have TwoPointShiftAI component.");
			assert(tps->toggleRef != 0 && "Error: toggleRef cannot be 0");
			
			Trinket* trink = Game::ecs.getComponent<Trinket>(Game::stack.peek(), tps->toggleRef);
			if (tps->lastToggleState != trink->active) {
				tps->interp.toggle();
				tps->lastToggleState = trink->active;
			}

			trans->pos = tps->interp.getValue();
			break;
		}

		case M_AI::kilomyte: {
			break;
		}

		case M_AI::text_tremble: {
			auto* tt = Game::ecs.getComponent<TextTrembleAI>(Game::stack.peek(), entity);
			assert(tt && "Error: Entity must have TextTrembleAI component.");

			tt->randOffset.x = 0;
			tt->randOffset.y = 0;

			std::uniform_real_distribution<float> randMag(0.0f, tt->mag);
			tt->randOffset.x = randMag(TimeManip::prng);
			tt->randOffset.y = randMag(TimeManip::prng);

			trans->pos = tt->center + tt->randOffset;

			break;
		}

		case M_AI::text_wave: {
			auto* tw = Game::ecs.getComponent<TextWaveAI>(Game::stack.peek(), entity);
			assert(tw && "Error: Entity must have TextWaveAI component.");

			trans->pos.y = tw->center.y + tw->mag * sin(10 * tw->timeElapsed);
			tw->timeElapsed += TimeManip::deltaTime;

			break;
		}

		default:
			break;
		}  // End switch
	}
}