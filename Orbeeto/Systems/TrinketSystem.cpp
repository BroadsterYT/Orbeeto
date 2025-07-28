#include "TrinketSystem.hpp"
#include "CollisionSystem.hpp"


TrinketSystem::TrinketSystem() {}

void TrinketSystem::update() {
	for (auto& entity : Game::ecs.getSystemGroup<Transform, Trinket>(Game::stack.peek())) {
		Transform* trans = Game::ecs.getComponent<Transform>(Game::stack.peek(), entity);
		Trinket* trinket = Game::ecs.getComponent<Trinket>(Game::stack.peek(), entity);

		switch (trinket->type) {
		case TrinketType::BUTTON:
		{
			std::vector<Entity> onTop;
			CollisionSystem::queryTree(QuadBox{ (float)trans->pos.x, (float)trans->pos.y, 64, 64 }, onTop);

			if (onTop.size() > 0) {
				trinket->active = true;
			}
			else trinket->active = false;
		}
			break;
		}  // Switch end
	}
}