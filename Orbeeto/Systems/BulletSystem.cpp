#include "BulletSystem.hpp"
#include "CollisionSystem.hpp"
#include "../InputManager.hpp"
#include <limits>


BulletSystem::BulletSystem() {}

void BulletSystem::update() {
	for (Entity& entity : Game::ecs.getSystemGroup<Bullet, Sprite, Transform, Collision>(Game::stack.peek())) {
		Bullet* bullet = Game::ecs.getComponent<Bullet>(Game::stack.peek(), entity);
		Transform* transform = Game::ecs.getComponent<Transform>(Game::stack.peek(), entity);
		Sprite* sprite = Game::ecs.getComponent<Sprite>(Game::stack.peek(), entity);
		Collision* coll = Game::ecs.getComponent<Collision>(Game::stack.peek(), entity);

		// ----- Bullet AI ----- //
		switch (bullet->bulletAI) {
		case BulletType::STANDARD:  // Standard bullet movement
			transform->velMovement();
			sprite->angle = -transform->vel.getAngle() + 180.0;
			break;

		case BulletType::HOMING: {
			double closestDistance = std::numeric_limits<double>::max();

			// Getting the distances between this bullet and all possible targets
			if (TimeManip::getTimeDiff(bullet->lastHomingCheck) > 1) {
				std::unordered_set<Entity> found;
				CollisionSystem::queryTree(QuadBox{ (float)(transform->pos.x - 32), (float)(transform->pos.y - 32), 64, 64 }, found);

				for (auto& target : found) {
					if (entity == target) continue;
					// TODO: Replace testing with actual implementation
					if (Game::ecs.getComponent<Player>(Game::stack.peek(), target) != nullptr) continue;  // Can't target players
					if (Game::ecs.getComponent<Bullet>(Game::stack.peek(), target) != nullptr) continue;  // Can't target other bullets
					if (Game::ecs.getComponent<Grapple>(Game::stack.peek(), target) != nullptr) continue;  // Can't target grappling hook

					Transform* targetTrans = Game::ecs.getComponent<Transform>(Game::stack.peek(), target);
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

			Transform* targetTrans = Game::ecs.getComponent<Transform>(Game::stack.peek(), bullet->closestTarget);

			// Rotating bullet toward target
			if (transform->pos.getDistToPoint(targetTrans->pos) < bullet->homingRange) {
				double angle = transform->pos.getAngleToPoint(targetTrans->pos);

				double difference = transform->vel.getAngle() - angle;
				transform->vel.rotate(difference - 180);
			}

			transform->velMovement();
			break;
		}  // End scope

		default:
			throw std::runtime_error("Error: Invalid bullet AI type.");
			break;
		}

		if (bullet->lifeTime >= 5.0f) {
			Game::ecs.destroyEntity(Game::stack.peek(), entity);
			continue;
		}
		bullet->lifeTime += TimeManip::deltaTime;
	}
}