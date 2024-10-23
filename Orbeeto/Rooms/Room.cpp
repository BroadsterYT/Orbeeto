#include "Room.hpp"
#include <iostream>

#include "../Components/Player.hpp"
#include "../Components/Sprite.hpp"
#include "../Components/Transform.hpp"


Camera Room::camera = Camera();

Room::Room(int roomX, int roomY) {
	this->roomX = roomX;
	this->roomY = roomY;

	Sprite* pSprite = Game::scene.assign<Sprite>(player);
	*pSprite = Sprite{
		.tileWidth = 64,
		.tileHeight = 64,
		.posX = 0,
		.posY = 0,
		.spriteSheet = TextureManager::loadTexture(Game::renderer, "Assets/orbeeto.png")
	};
	Transform* pTransform = Game::scene.assign<Transform>(player);
	*pTransform = Transform{
		.pos = Vector2{ 300.0f, 300.0f },
	};
	Player* pPlayer = Game::scene.assign<Player>(player);
	*pPlayer = Player{};

	loadRoomEntities(0, 0);
}

void Room::loadRoomEntities(int x, int y) {
}

void Room::recordRoomLayout() {

}

void Room::update() {
	Transform* pTransform = Game::scene.assign<Transform>(player);
	Room::camera.focus((int)pTransform->pos.x, (int)pTransform->pos.y);
}