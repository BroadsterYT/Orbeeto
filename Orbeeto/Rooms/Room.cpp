#include "Room.hpp"

#include "../Components/AccelTransform.hpp"
#include "../Components/Collision.hpp"
#include "../Components/Defense.hpp"
#include "../Components/Hp.hpp"
#include "../Components/Player.hpp"
#include "../Components/Sprite.hpp"
#include <iostream>

Camera Room::camera = Camera();

Room::Room(int roomX, int roomY) {
	this->roomX = roomX;
	this->roomY = roomY;

	// Creating a test player
	Game::coordinator.addComponent<Sprite>(player,
		Sprite{
			.tileWidth = 64,
			.tileHeight = 64,
			.posX = 0,
			.posY = 0,
			.spriteSheet = TextureManager::loadTexture(Game::renderer, "Assets/orbeeto.png")
		}
	);
	Game::coordinator.addComponent<AccelTransform>(player,
		AccelTransform{
			.pos = Vector2(300, 300)
		}
	);
	Game::coordinator.addComponent<Player>(player, Player{});
	Game::coordinator.addComponent<Collision>(player,
		Collision{
			64,		// hitbox width
			64,		// hitbox height
			Vector2(300, 300),	// hitbox position
			true,
			true,
			false,
			true,
		}
	);
	Game::coordinator.addComponent<Hp>(player, Hp{ 50, 50 });
	Game::coordinator.addComponent<Defense>(player, Defense{ 10, 10 });


	// Wall
	Game::coordinator.addComponent<Sprite>(wall,
		Sprite{
			.tileWidth = 64,
			.tileHeight = 64,
			.posX = 0,
			.posY = 0,
			.spriteSheet = TextureManager::loadTexture(Game::renderer, "Assets/orbeeto.png")
		}
	);
	Game::coordinator.addComponent<AccelTransform>(wall,
		AccelTransform{
			.pos = Vector2(500, 500)
		}
	);
	Game::coordinator.addComponent<Collision>(wall,
		Collision{
			64,
			64,
			Vector2(500, 500),
			false,
		}
	);
}

void Room::loadRoomLayout(int x, int y) {

}

void Room::recordRoomLayout() {

}

void Room::update() {
	Room::camera.focus(player);
}