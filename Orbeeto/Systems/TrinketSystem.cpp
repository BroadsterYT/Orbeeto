#include "TrinketSystem.hpp"


TrinketSystem::TrinketSystem() {}

void TrinketSystem::update() {
	for (auto& entity : Game::ecs.getSystemGroup<Transform, Trinket>(Game::stack.peek())) {
		Transform* trans = Game::ecs.getComponent<Transform>(Game::stack.peek(), entity);
	}
}