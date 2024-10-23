#include "BulletSystem.hpp"
#include "../Components/Bullet.hpp"
#include "../Components/Sprite.hpp"
#include "../Components/Transform.hpp"
#include "SDL.h"


void BulletSystem::init(Coordinator* coord) {
	coordinator = coord;
}

void BulletSystem::update() {
	for (auto entity : mEntities) {
		std::cout << "Bullet " << entity << "is being evaluated" << std::endl;
		auto& bullet = coordinator->getComponent<Bullet>(entity);
		auto& transform = coordinator->getComponent<Transform>(entity);

		transform.velMovement();

		if (SDL_GetTicks() - bullet.birthTime > 1000) {
			coordinator->removeComponent<Sprite>(entity);
			kill.push_back(entity);
		}
	}
}

void BulletSystem::killAbandoned() {
	for (auto entity : kill) {
		//std::cout << "Destroying entity " << entity << std::endl;
		coordinator->destroyEntity(entity);
	}
	kill.clear();
}