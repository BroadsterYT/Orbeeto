#pragma once
#include "System.hpp"


class BulletSystem : public System {
public:
	BulletSystem() {}

	void update() {
		for (Entity& entity : Game::ecs.getSystemGroup<Bullet, Sprite, Transform>()) {
			Bullet* bullet = Game::ecs.getComponent<Bullet>(entity);
			Transform* transform = Game::ecs.getComponent<Transform>(entity);

			// Bullet AI
			if (bullet->bulletAI == 0) {
				transform->velMovement();
			}
			else {
				throw std::runtime_error("Invalid Bullet AI type");
			}

			// Destroying bullet if its lifetime is too long
			if (SDL_GetTicks() - bullet->birthTime >= 5000) {
				std::cout << "Bullet destroyed." << std::endl;

				Game::ecs.destroyEntity(entity);
			}
		}
	}
};