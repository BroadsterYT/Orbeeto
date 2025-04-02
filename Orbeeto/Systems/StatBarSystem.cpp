#include "StatBarSystem.hpp"


StatBarSystem::StatBarSystem() {}

void StatBarSystem::update() {
	for (auto& entity : Game::ecs.getSystemGroup<StatBar, Transform, Sprite>()) {
		Transform* trans = Game::ecs.getComponent<Transform>(entity);
		StatBar* sBar = Game::ecs.getComponent<StatBar>(entity);
		Sprite* sprite = Game::ecs.getComponent<Sprite>(entity);

		float ratio = (float)(*sBar->val - sBar->minVal) / (float)(*sBar->maxVal - sBar->minVal);
		sprite->index = (int)(16.0f * ratio);

		if (sBar->deleteAtZero) {
			if (*sBar->val <= 0) Game::ecs.destroyEntity(entity);
		}
	}
}