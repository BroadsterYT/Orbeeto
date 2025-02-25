#include "BulletSystem.hpp"
#include "../InputManager.hpp"
#include <limits>


BulletSystem::BulletSystem() {}

void BulletSystem::update() {
	for (Entity& entity : Game::ecs.getSystemGroup<Bullet, Sprite, Transform>()) {
		Bullet* bullet = Game::ecs.getComponent<Bullet>(entity);
		Transform* transform = Game::ecs.getComponent<Transform>(entity);
		Sprite* sprite = Game::ecs.getComponent<Sprite>(entity);

		// ----- Bullet AI ----- //
		switch (bullet->bulletAI) {
		case 0:  // Standard bullet movement
			transform->velMovement();
			sprite->angle = -transform->vel.getAngle() + 180.0;
			break;

		case 1:  // Homing bullets
			{
			double closestDistance = std::numeric_limits<double>::max();

			if (!bullet->homingCheck) {
				// Getting the distances between this bullet and all possible targets
				for (auto& target : Game::ecs.getSystemGroup<Transform, Collision, Sprite>()) {
					if (entity == target) continue;
					if (Game::ecs.getComponent<Player>(target) != nullptr) continue;  // Can't target players
					if (Game::ecs.getComponent<Bullet>(target) != nullptr) continue;  // Can't target other bullets

					Transform* targetTrans = Game::ecs.getComponent<Transform>(target);
					double distance = transform->pos.getDistToPoint(targetTrans->pos);

					if (distance < closestDistance) {
						closestDistance = distance;
						bullet->closestTarget = target;
					}

					bullet->homingCheck = true;
				}
			}

			if (bullet->closestTarget == 0) break;

			// Rotating bullet toward target
			Transform* targetTrans = Game::ecs.getComponent<Transform>(bullet->closestTarget);
			double angle = transform->pos.getAngleToPoint(targetTrans->pos);

			std::cout << transform->vel.getAngle() << std::endl;
			double difference = transform->vel.getAngle() - angle;
			transform->vel.rotate(difference - 180);

			}  // End scope
			transform->velMovement();
			break;

		default:
			throw std::runtime_error("Error: Invalid bullet AI type.");
			break;
		}

		// Destroying bullet if its lifetime is too long
		if (SDL_GetTicks() - bullet->birthTime >= 5000) {
			std::cout << "Bullet destroyed." << std::endl;

			Game::ecs.destroyEntity(entity);
		}
	}
}