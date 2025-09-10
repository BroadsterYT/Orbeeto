#include "Raycast.hpp"
#include "Room.hpp"
#include <iostream>
#include <unordered_set>


Raycast::Raycast(Vector2 origin, int width, double angle) {
	this->origin = origin;
	this->angle = angle;
	rotDir = Vector2(0, -width);
	rotDir.rotate(angle);

	this->width = width;
}

void Raycast::getAllIntersects() {
	rotDir = Vector2(0, -(width - getWidthAdj()));
	rotDir.rotate(angle);

	std::unordered_set<Entity> inter;  // Entities intersected
	for (int i = 0; i < 100; i++) {
		/*Entity e = Game::ecs.createEntity(Game::stack.peek());
		Game::ecs.assignComponent<Sprite>(Game::stack.peek(), e);
		Game::ecs.assignComponent<Transform>(Game::stack.peek(), e);

		Transform* eTrans = Game::ecs.getComponent<Transform>(Game::stack.peek(), e);
		eTrans->pos = Vector2(origin.x + rotDir.x * i, origin.y + rotDir.y * i);

		Sprite* eSprite = Game::ecs.getComponent<Sprite>(Game::stack.peek(), e);
		*eSprite = Sprite(0, 0, 16, 16);
		eSprite->spriteSheet = TextureManager::loadTexture(Game::renderer, "Assets/tile1.png");*/
		CollisionSystem::queryTree(QuadBox{ (float)(origin.x + rotDir.x * i + width / 2), (float)(origin.y + rotDir.y * i + width / 2), 16, 16}, inter);
	}
}

double Raycast::getWidthAdj() {
	return -(width * sqrt(2) - width) * abs(sin(2 * angle));
}