#include "Raycast.hpp"
#include <iostream>


Raycast::Raycast(Vector2 origin, double angle) {
	this->origin = origin;
	this->angle = angle;
	rotDir = Vector2(0, -16);
	rotDir.rotate(angle);
	callcount = 0;
}

void Raycast::getAllIntersects() {
	std::vector<Entity> inter;  // Entities intersected
	for (int x = 0; x < 100; x++) { // TODO: Calulate the number of checks to do based on closest stopping distance
		CollisionSystem::queryTree(QuadBox{ (float)(origin.x + rotDir.x * x), (float)(origin.y + rotDir.y * x), 16, 16}, inter);
		//SDL_SetRenderTarget(Game::renderer, NULL);
		//SDL_SetRenderDrawColor(Game::renderer, 255, 0, 0, 255);
		//SDL_Rect draw = { (int)(origin.x + rotDir.x), (int)(origin.y + rotDir.y), 16, 16 };
		//SDL_RenderFillRect(Game::renderer, &draw);
		//SDL_SetRenderDrawColor(Game::renderer, 0, 0, 0xFF, SDL_ALPHA_OPAQUE);
		//std::cout << "x: " << origin.x + rotDirCopy.x << " y: " << origin.y + rotDirCopy.y << std::endl;
		callcount++;
	}

	for (auto& ent : inter) {
		std::cout << callcount << " Entity " << ent << " present in raycast search." << std::endl;
	}
}