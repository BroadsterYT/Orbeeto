#include "GrappleSystem.hpp"
#include "../InputManager.hpp"
#include "../Math.hpp"


GrappleSystem::GrappleSystem() : System() {}

void GrappleSystem::update() {
	for (auto& entity : Game::ecs.getSystemGroup<Collision, Grapple, Sprite, Transform>(Game::stack.peek())) {
		Transform* transform = Game::ecs.getComponent<Transform>(Game::stack.peek(), entity);
		Grapple* grapple = Game::ecs.getComponent<Grapple>(Game::stack.peek(), entity);

		Player* player = Game::ecs.getComponent<Player>(Game::stack.peek(), grapple->owner);
		Transform* pTrans = Game::ecs.getComponent<Transform>(Game::stack.peek(), grapple->owner);

		switch (player->grappleState) {
		case GrappleState::SENT:
			if (player->grappleInputCopy < InputManager::mouseReleased[SDL_BUTTON_MIDDLE]) {
				player->grappleState = GrappleState::RETURNING;
				transform->vel = { 0, 0 };
				//grapple->lastReturn = TimeManip::getTime();
				//std::cout << grapple->lastReturn << std::endl;
				player->grappleInputCopy = InputManager::mouseReleased[SDL_BUTTON_MIDDLE];
			}

			transform->velMovement();
			break;

		case GrappleState::LATCHED:
			transform->accel = Vector2(0.0f, 0.0f);

			if (player->grappleInputCopy < InputManager::mouseReleased[SDL_BUTTON_MIDDLE]) {
				player->grappleState = GrappleState::RETURNING;
				player->grappleInputCopy = InputManager::mouseReleased[SDL_BUTTON_MIDDLE];
			}
			break;

		case GrappleState::RETURNING: 
			if (player->grappleInputCopy < InputManager::mouseReleased[SDL_BUTTON_MIDDLE]) {
				Game::ecs.destroyEntity(Game::stack.peek(), entity);
				player->grappleRef = 0;  // Remove grapple reference from player
				player->moveToGrapple = false;

				player->grappleState = GrappleState::INACTIVE;
				player->grappleInputCopy = InputManager::mouseReleased[SDL_BUTTON_MIDDLE];
				break;
			}

			if (grapple->grappledTo == 0) {
				double angle = Math::rad(transform->pos.getAngleToPoint(pTrans->pos));

				transform->accel.x = transform->accelConst * -sin(angle);
				transform->accel.y = transform->accelConst * -cos(angle);

				transform->accelMovement();
			}
			else {
				/*double angle = pTrans->pos.getAngleToPoint(transform->pos);
				pTrans->accel.x = transform->accelConst * cos(-angle);
				pTrans->accel.y = transform->accelConst * sin(-angle);
				pTrans->accelMovement();*/
			}
			break;
		}
	}
}