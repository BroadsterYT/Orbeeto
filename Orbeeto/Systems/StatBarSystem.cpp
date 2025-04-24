#include "StatBarSystem.hpp"


StatBarSystem::StatBarSystem() {}

void StatBarSystem::update() {
	for (auto& entity : Game::ecs.getSystemGroup<StatBar, Transform, Sprite>(Game::stack.peek())) {
		Transform* trans = Game::ecs.getComponent<Transform>(Game::stack.peek(), entity);
		StatBar* sBar = Game::ecs.getComponent<StatBar>(Game::stack.peek(), entity);
		Sprite* sprite = Game::ecs.getComponent<Sprite>(Game::stack.peek(), entity);

		float ratio = (float)(*sBar->val - sBar->minVal) / (float)(*sBar->maxVal - sBar->minVal);
		sprite->index = (int)(16.0f * ratio);

		if (sBar->deleteAtZero) {
			if (*sBar->val <= 0) Game::ecs.destroyEntity(Game::stack.peek(), entity);
		}
	}
}