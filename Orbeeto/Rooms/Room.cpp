#include "Room.hpp"
#include <iostream>
#include <memory>

#include "../Components/Player.hpp"
#include "../Components/Sprite.hpp"
#include "../Components/Transform.hpp"


Camera Room::camera = Camera();

Room::Room(int roomX, int roomY) {
	this->roomX = roomX;
	this->roomY = roomY;

	Entity test = Game::ecs.createEntity();
	Game::ecs.assignComponent<Sprite>(test);

	Game::ecs.assignComponent<Sprite>(player);
	Game::ecs.assignComponent<Transform>(player);

	Sprite* pullSprite = Game::ecs.getComponent<Sprite>(player);
	*pullSprite = Sprite{
		.tileWidth = 64,
		.tileHeight = 64,
		.posX = 0,
		.posY = 0,
		.spriteSheet = TextureManager::loadTexture(Game::renderer, "Assets/orbeeto.png")
	};
	
	Transform* pullTransform = Game::ecs.getComponent<Transform>(player);
	*pullTransform = Transform{ .pos = Vector2(300, 300) };

	Game::ecs.destroyEntity(test);

	std::cout << "Entities: " << std::endl;
	for (int i = 0; i < Game::ecs.entities.size(); i++) {
		std::cout << Game::ecs.entities[i].entity << std::endl;
	}

	Game::ecs.getSystemGroup<Sprite>();

	loadRoomEntities(0, 0);
}

void Room::loadRoomEntities(int x, int y) {
	if (roomX == 0 && roomY == 0) {

	}
}

void Room::recordRoomLayout() {

}

void Room::update() {
	Transform* pTransform = Game::ecs.getComponent<Transform>(player);
	Room::camera.focus((int)pTransform->pos.x, (int)pTransform->pos.y);
}