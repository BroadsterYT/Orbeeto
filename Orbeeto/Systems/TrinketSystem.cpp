#include "TrinketSystem.hpp"
#include "CollisionSystem.hpp"


TrinketSystem::TrinketSystem() {}

void TrinketSystem::update() {
	for (auto& entity : Game::ecs.getSystemGroup<Transform, Trinket>(Game::stack.peek())) {
		Transform* trans = Game::ecs.getComponent<Transform>(Game::stack.peek(), entity);
		Trinket* trinket = Game::ecs.getComponent<Trinket>(Game::stack.peek(), entity);

		switch (trinket->type) {
		case TrinketType::button: {
			std::unordered_set<Entity> onTop;
			CollisionSystem::queryTree(QuadBox{ (float)trans->pos.x - 32, (float)trans->pos.y - 32, 64, 64 }, onTop);

			bool playerCheck = false;
			for (auto& entity : onTop) {
				Player* p = Game::ecs.getComponent<Player>(Game::stack.peek(), entity);
				if (p) playerCheck = true;
			}

			if (playerCheck) {
				//std::cout << "ACTIVE!\n";
				trinket->active = true;
			}
			else {
				trinket->active = false;
				//std::cout << "inactive\n";
			}
			break;
		}
		}  // Switch end
	}
}