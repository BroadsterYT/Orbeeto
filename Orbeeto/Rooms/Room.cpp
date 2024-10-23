#include "Room.hpp"

#include "../Components/Transform.hpp"
#include "../Components/Collision.hpp"
#include "../Components/Defense.hpp"
#include "../Components/Hp.hpp"
#include "../Components/Player.hpp"
#include "../Components/PlayerGun.hpp"
#include "../Components/Sprite.hpp"
#include <iostream>


Camera Room::camera = Camera();

Room::Room(int roomX, int roomY) {
	this->roomX = roomX;
	this->roomY = roomY;

	// Creating a test player
	Game::coordinator.addComponent<Transform>(player,
		Transform{
			.pos = Vector2(300, 300)
		}
		);
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
	Game::coordinator.addComponent<Defense>(player, Defense{ 10, 10 });
	Game::coordinator.addComponent<Hp>(player, Hp{ 50, 50 });
	Game::coordinator.addComponent<Player>(player, Player{});
	Game::coordinator.addComponent<Sprite>(player,
		Sprite{
			.tileWidth = 64,
			.tileHeight = 64,
			.posX = 0,
			.posY = 0,
			.spriteSheet = TextureManager::loadTexture(Game::renderer, "Assets/orbeeto.png")
		}
		);
	

	// Player left gun test
	Game::coordinator.addComponent<Transform>(leftGun,
		Transform{.pos = Vector2(0, 0)}
		);
	Game::coordinator.addComponent<PlayerGun>(leftGun,
		PlayerGun{
			.owner = &player,
			.cooldown = 10.0f,
			.heatDissipation = 5.0f
		}
		);
	Game::coordinator.addComponent<Sprite>(leftGun,
		Sprite{
			.tileWidth = 64,
			.tileHeight = 64,
			.posX = 0,
			.posY = 0,
			.spriteSheet = TextureManager::loadTexture(Game::renderer, "Assets/orbeetoguns.png")
		}
		);

	loadRoomEntities(0, 0);
}

void Room::loadRoomEntities(int x, int y) {
	if (roomX == 0 && roomY == 0) {
		const Entity& wall1 = Game::coordinator.createEntity();

		Game::coordinator.addComponent<Transform>(wall1, Transform{.pos = Vector2(500, 500)});
		Game::coordinator.addComponent<Collision>(wall1,
			Collision{
				64,
				64,
				Vector2(500, 500),
				false,
				true,
			}
			);
		Game::coordinator.addComponent<Sprite>(wall1,
			Sprite{
				.tileWidth = 64,
				.tileHeight = 64,
				.posX = 0,
				.posY = 0,
				.spriteSheet = TextureManager::loadTexture(Game::renderer, "Assets/orbeeto.png")
			}
			);
	}
	
	else {

	}
}

void Room::recordRoomLayout() {

}

void Room::update() {
	Room::camera.focus(player);
}