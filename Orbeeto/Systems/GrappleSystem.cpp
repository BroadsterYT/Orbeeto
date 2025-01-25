#include "GrappleSystem.hpp"
#include "../InputManager.hpp"
#include <cmath>


GrappleSystem::GrappleSystem() : System() {}

void GrappleSystem::update() {
	for (auto& entity : Game::ecs.getSystemGroup<Collision, Grapple, Sprite, Transform>()) {
		Transform* transform = Game::ecs.getComponent<Transform>(entity);
		Grapple* grapple = Game::ecs.getComponent<Grapple>(entity);

		Player* player = Game::ecs.getComponent<Player>(grapple->owner);
		Transform* pTrans = Game::ecs.getComponent<Transform>(grapple->owner);

		switch (player->grappleState) {
		case GrappleState::SENT:
			std::cout << transform->vel.x << " " << transform->vel.y << std::endl;

			if (!InputManager::mousePressed[SDL_BUTTON_MIDDLE]) {
				player->grappleState = GrappleState::RETURNING;
			}

			transform->velMovement();
			break;

		case GrappleState::LATCHED:
			transform->accel = Vector2(0.0f, 0.0f);
			if (!InputManager::mousePressed[SDL_BUTTON_MIDDLE]) {
				player->grappleState = GrappleState::RETURNING;
			}

			break;

		case GrappleState::RETURNING: 
			if (grapple->grappledTo == nullptr) {
				double angle = transform->pos.getAngleToPoint(pTrans->pos);
				transform->accel.x = transform->accelConst * cos(-angle);
				transform->accel.y = transform->accelConst * sin(-angle);
				transform->accelMovement();
			}
			else {
				double angle = pTrans->pos.getAngleToPoint(transform->pos);
				pTrans->accel.x = transform->accelConst * cos(-angle);
				pTrans->accel.y = transform->accelConst * sin(-angle);
				pTrans->accelMovement();
			}
			break;
		}
	}
}