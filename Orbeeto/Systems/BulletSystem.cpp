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
		case BulletType::STANDARD:  // Standard bullet movement
			transform->velMovement();
			sprite->angle = -transform->vel.getAngle() + 180.0;
			break;

		case BulletType::HOMING:  // Homing bullets
			{
			double closestDistance = std::numeric_limits<double>::max();

			// Getting the distances between this bullet and all possible targets
			if (TimeManip::getTimeDiff(bullet->lastHomingCheck) > 1000) {
				for (auto& target : Game::ecs.getSystemGroup<Transform, Collision, Sprite>()) {
					if (entity == target) continue;
					// TODO: Replace testing with actual implementation
					if (Game::ecs.getComponent<Player>(target) != nullptr) continue;  // Can't target players
					if (Game::ecs.getComponent<Bullet>(target) != nullptr) continue;  // Can't target other bullets
					if (Game::ecs.getComponent<Grapple>(target) != nullptr) continue;  // Can't target other bullets

					Transform* targetTrans = Game::ecs.getComponent<Transform>(target);
					double distance = transform->pos.getDistToPoint(targetTrans->pos);

					if (distance < closestDistance) {
						closestDistance = distance;
						bullet->closestTarget = target;
					}
				}
				bullet->lastHomingCheck = TimeManip::getTime();
			}

			if (bullet->closestTarget == 0) {
				transform->velMovement();
				break;
			}

			Transform* targetTrans = Game::ecs.getComponent<Transform>(bullet->closestTarget);

			// Rotating bullet toward target
			if (transform->pos.getDistToPoint(targetTrans->pos) < bullet->homingRange) {
				double angle = transform->pos.getAngleToPoint(targetTrans->pos);

				double difference = transform->vel.getAngle() - angle;
				transform->vel.rotate(difference - 180);
			}

			}  // End scope
			transform->velMovement();
			break;

		default:
			throw std::runtime_error("Error: Invalid bullet AI type.");
			break;
		}

		// Destroying bullet if its lifetime is too long
		if (TimeManip::getTimeDiff(bullet->birthTime) >= 5000) {
			//std::cout << "Bullet destroyed." << std::endl;

			Game::ecs.destroyEntity(entity);
		}
	}
}