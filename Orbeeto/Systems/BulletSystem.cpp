#include "BulletSystem.hpp"

BulletSystem::BulletSystem() : System() {}

void BulletSystem::update() {
	for (Entity& entity : Game::ecs.getSystemGroup<Bullet, Transform>()) {
		Bullet* bullet = Game::ecs.getComponent<Bullet>(entity);
		Transform* transform = Game::ecs.getComponent<Transform>(entity);

		transform->velMovement();

		// Destroying bullet if its lifetime is too long
		/*if (SDL_GetTicks() - bullet) {

		}*/
	}
}