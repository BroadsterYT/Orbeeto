#include "EntityAISystem.hpp"
#include <cassert>
#include <random>
#include <cmath>

#include "CollisionSystem.hpp"


EntityAISystem::EntityAISystem() {}

void EntityAISystem::update() {
	for (auto& entity : Game::ecs.getSystemGroup<Transform, EntityAI>(Game::stack.peek())) {
		EntityAI* mvmAI = Game::ecs.getComponent<EntityAI>(Game::stack.peek(), entity);
		Transform* trans = Game::ecs.getComponent<Transform>(Game::stack.peek(), entity);

		switch (mvmAI->ai) {
		case AiType::circle_accel:
			/*trans->accel.x = trans->accelConst * cos(TimeManip::getSDLTime() / 1000);
			trans->accel.y = trans->accelConst * sin(TimeManip::getSDLTime() / 1000);
			trans->accelMovement();*/
			break;

		case AiType::follow_entity: {
			auto* feAI = Game::ecs.getComponent<FollowEntityAI>(Game::stack.peek(), entity);
			assert(feAI && "Error: Entity must have FollowEntityAI component.");

			auto* eTrans = Game::ecs.getComponent<Transform>(Game::stack.peek(), feAI->entityRef);
			trans->pos = eTrans->pos + feAI->distOffset;

			break;
		}

		case AiType::two_point_shift: {
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

		case AiType::tractor_beam: {
			TractorBeamAI* tb = Game::ecs.getComponent<TractorBeamAI>(Game::stack.peek(), entity);
			assert(tb && "Entity must have TractorBeamAI component");
			assert(tb->toggleRef != 0 && "TractorBeamAI toggleRef cannot be 0");

			Trinket* trink = Game::ecs.getComponent<Trinket>(Game::stack.peek(), tb->toggleRef);
			if (trink->active || (!trink->active && tb->invertToggle)) {
				// Finding entities in beam
				std::unordered_set<Entity> inside;
				CollisionSystem::queryTree(QuadBox{ (float)(trans->pos.x - tb->width / 2), (float)(trans->pos.y - tb->height / 2), (float)tb->width, (float)tb->height }, inside);

				// TODO: Add filters for certain entities

				for (auto& e : inside) {
					Transform* eTrans = Game::ecs.getComponent<Transform>(Game::stack.peek(), e);
					
					switch (tb->direction) {
					case 0: {
						eTrans->accel.y += tb->strength;
						break;
					}
					case 1: {
						eTrans->accel.x += tb->strength;
						break;
					}
					case 2: {
						eTrans->accel.y -= tb->strength;
						break;
					}
					case 3: {
						eTrans->accel.x -= tb->strength;
						break;
					}
					default:
						break;
					}  // End switch
				}

			}

			break;
		}

		case AiType::kilomyte: {
			break;
		}

		case AiType::text_tremble: {
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

		case AiType::text_wave: {
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