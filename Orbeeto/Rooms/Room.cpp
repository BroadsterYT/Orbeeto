#include "Room.hpp"

#include "../Components/AccelTransform.hpp"
#include "../Components/Collision.hpp"
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
			Game::renderer,
			"assets/orbeeto.png",
			64,
			64,
			0,
			0
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
			Vector2(300, 300)	// hitbox position
		}
	);

	// Wall
	Game::coordinator.addComponent<Sprite>(wall,
		Sprite{
			Game::renderer,
			"assets/orbeeto.png",
			64,
			64,
			0,
			0
		}
	);
	Game::coordinator.addComponent<AccelTransform>(wall,
		AccelTransform{
			.pos = Vector2(500, 500)
		}
	);
	Game::coordinator.addComponent<Collision>(wall,
		Collision{
			64,		// hitbox width
			64,		// hitbox height
			Vector2(500, 500)	// hitbox position
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