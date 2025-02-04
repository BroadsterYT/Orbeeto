#include "BulletSystem.hpp"


BulletSystem::BulletSystem() {}

void BulletSystem::update() {
	for (Entity& entity : Game::ecs.getSystemGroup<Bullet, Sprite, Transform>()) {
		Bullet* bullet = Game::ecs.getComponent<Bullet>(entity);
		Transform* transform = Game::ecs.getComponent<Transform>(entity);

		// ----- Bullet AI ----- //
		switch (bullet->bulletAI) {
		case 0:  // Standard bullet movement
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