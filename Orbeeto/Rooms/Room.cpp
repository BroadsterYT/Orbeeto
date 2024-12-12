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

	Game::ecs.assignComponent<Sprite>(player);
	Game::ecs.assignComponent<Player>(player);
	Game::ecs.assignComponent<Transform>(player);
	Game::ecs.assignComponent<Collision>(player);

	Game::ecs.assignComponent<Sprite>(leftGun);
	Game::ecs.assignComponent<PlayerGun>(leftGun);
	Game::ecs.assignComponent<Transform>(leftGun);

	// ----- Player ----- //
	Sprite* playerSprite = Game::ecs.getComponent<Sprite>(player);
	*playerSprite = Sprite{
		.tileWidth = 64,
		.tileHeight = 64,
		.spriteSheet = TextureManager::loadTexture(Game::renderer, "Assets/orbeeto.png")
	};
	
	Transform* playerTrans = Game::ecs.getComponent<Transform>(player);
	*playerTrans = Transform{ .pos = Vector2(300, 300) };
	
	Collision* playerColl = Game::ecs.getComponent<Collision>(player);
	*playerColl = Collision{
		.hitWidth = 64,
		.hitHeight = 64,
		.hitPos = Vector2(300.0f, 300.0f),
		.canHurt = true
	};

	// ----- Left Gun ----- //
	Sprite* lGunSprite = Game::ecs.getComponent<Sprite>(leftGun);
	*lGunSprite = Sprite{
		.tileWidth = 64,
		.tileHeight = 64,
		.spriteSheet = TextureManager::loadTexture(Game::renderer, "Assets/orbeetoguns.png")
	};

	Transform* lGunTrans = Game::ecs.getComponent<Transform>(leftGun);
	*lGunTrans = Transform{ .pos = Vector2(300.0f, 300.0f) };

	PlayerGun* lGun = Game::ecs.getComponent<PlayerGun>(leftGun);
	*lGun = PlayerGun{
		.owner = &player,
		.maxCooldown = 100,
		.cooldown = 100,
		.heatDissipation = 10.0f
	};

	loadRoomEntities(0, 0);
}

void Room::loadRoomEntities(int x, int y) {
	if (roomX == 0 && roomY == 0) {
		Entity wall = Game::ecs.createEntity();

		Game::ecs.assignComponent<Sprite>(wall);
		Game::ecs.assignComponent<Transform>(wall);
		Game::ecs.assignComponent<Collision>(wall);

		Sprite* wallSprite = Game::ecs.getComponent<Sprite>(wall);
		*wallSprite = Sprite{
			.tileWidth = 64,
			.tileHeight = 64,
			.spriteSheet = TextureManager::loadTexture(Game::renderer, "Assets/orbeeto.png")
		};
		Transform* wallTrans = Game::ecs.getComponent<Transform>(wall);
		*wallTrans = Transform{ .pos = Vector2(500.0f, 500.0f) };
		Collision* wallColl = Game::ecs.getComponent<Collision>(wall);
		*wallColl = Collision{
			.hitWidth = 64,
			.hitHeight = 64,
			.hitPos = Vector2(300.0f, 300.0f),
			.canHurt = false
		};
	}
}

void Room::recordRoomLayout() {}

void Room::update() {
	Transform* pTransform = Game::ecs.getComponent<Transform>(player);
	Room::camera.focus((int)pTransform->pos.x, (int)pTransform->pos.y);
}