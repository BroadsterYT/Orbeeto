#include "Room.hpp"
#include <fstream>
#include <iostream>
#include <memory>
#include <cassert>

#include "../Components/Player.hpp"
#include "../Components/Sprite.hpp"
#include "../Components/Transform.hpp"


Camera Room::camera = Camera();

std::unordered_map<Entity, Entity> Room::portalLinks;

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
		.layer = 0,
		.tileWidth = 64,
		.tileHeight = 64,
		.spriteSheet = TextureManager::loadTexture(Game::renderer, "Assets/orbeeto.png")
	};
	
	Transform* playerTrans = Game::ecs.getComponent<Transform>(player);
	*playerTrans = Transform{ .pos = Vector2(300, 300) };
	
	Collision* playerColl = Game::ecs.getComponent<Collision>(player);
	*playerColl = Collision{
		.hitWidth = 32,
		.hitHeight = 32,
		.hitPos = Vector2(300.0f, 300.0f),
		.physicsTags = {"player", "pushable", "canPush", "hurtable"}
	};

	// ----- Left Gun ----- //
	Sprite* lGunSprite = Game::ecs.getComponent<Sprite>(leftGun);
	*lGunSprite = Sprite{
		.layer = 1,
		.tileWidth = 64,
		.tileHeight = 64,
		.spriteSheet = TextureManager::loadTexture(Game::renderer, "Assets/orbeetoguns.png")
	};

	Transform* lGunTrans = Game::ecs.getComponent<Transform>(leftGun);
	*lGunTrans = Transform{ .pos = Vector2(300.0f, 300.0f) };

	PlayerGun* lGun = Game::ecs.getComponent<PlayerGun>(leftGun);
	*lGun = PlayerGun{
		.owner = &player,
	};

	loadRoom(0, 0);
}

void Room::loadRoom(int x, int y) {
	if (roomX == 0 && roomY == 0) {
		readRoomData(vectorizeRoomDetails("Rooms/RoomLayouts/test.dat"), vectorizeRoomTiles("Rooms/RoomLayouts/test.dat"));
	}
}

void Room::update() {
	Transform* pTransform = Game::ecs.getComponent<Transform>(player);

	Room::camera.focus((int)pTransform->pos.x, (int)pTransform->pos.y);
}

void Room::newPortalLink(Entity& first, Entity& second) {
	portalLinks[first] = second;
}

void Room::removePortalLink(Entity& portal) {
	auto it = portalLinks.find(portal);
	if (it != portalLinks.end()) portalLinks.erase(it);
	else std::cout << "Link could not be found\n";
}

Entity Room::getPortalLink(Entity& portal) {
	return portalLinks[portal];
}

void Room::clearPortalLinks() {
	portalLinks.clear();
}

std::vector<int> Room::vectorizeRoomDetails(const std::string roomFilePath) {
	std::vector<int> roomDetails;

	std::ifstream roomFile(roomFilePath);

	int currentSpec;
	for (int i = 0; i < 4; i++) {
		roomFile >> currentSpec;
		roomDetails.push_back(currentSpec);
	}

	roomFile.close();
	return roomDetails;
}

std::vector<std::vector<int>> Room::vectorizeRoomTiles(const std::string roomFileName) {
	std::ifstream roomFile(roomFileName);
	assert(roomFile.is_open() && "Error opening room data file.");

	int roomTileWidth, roomTileHeight;
	roomFile >> roomTileWidth >> roomTileHeight;

	// We don't care about the scrolling values so we skip over them
	int temp;
	roomFile >> temp >> temp;

	// Taking each tile ID in the room data file and putting them into vectors
	std::vector<std::vector<int>> finalData;
	std::vector<int> tempData;

	int currentTile;
	for (int i = 0; i < roomTileWidth * roomTileHeight; i++) {
		roomFile >> currentTile;

		tempData.push_back(currentTile);

		if ((i + 1) % roomTileWidth == 0) {
			finalData.push_back(tempData);
			tempData.clear();
		}
	}

	roomFile.close();
	return finalData;
}

void Room::readRoomData(const std::vector<int> roomDetails, const std::vector<std::vector<int>> roomTiles) {
	canScrollX = roomDetails[2];
	canScrollY = roomDetails[3];

	for (int y = 0; y < roomTiles.size(); y++) {
		for (int x = 0; x < roomTiles[y].size(); x++) {
			buildRoomEntity(roomTiles[y][x], x, y);
		}
	}
}

void Room::buildRoomEntity(const int tileId, int tilePosX, int tilePosY) {
	const int tileSize = 64;

	if (tileId == 0) return;

	else if (tileId == 1) {
		Entity testWall = Game::ecs.createEntity();
		Game::ecs.assignComponent<Collision>(testWall);
		Game::ecs.assignComponent<Sprite>(testWall);
		Game::ecs.assignComponent<Transform>(testWall);

		// Building wall tile image
		// TODO: finalWallImage texture must be destroyed when switching rooms
		SDL_Texture* finalWallImage = SDL_CreateTexture(Game::renderer, SDL_PIXELFORMAT_RGBA8888, SDL_TEXTUREACCESS_TARGET, tileSize, tileSize);
		SDL_Texture* tileSheet = TextureManager::loadTexture(Game::renderer, "Assets/wall.png");

		SDL_SetTextureBlendMode(finalWallImage, SDL_BLENDMODE_BLEND);
		SDL_SetRenderTarget(Game::renderer, finalWallImage);

		const int tileStampSize = 32;  // The size of each little tile being stitched together to make the final tile (may not be the size of the tile in the tile sheet!)
		SDL_Rect finalSrcRect(0, 0, 16, 16);
		SDL_Rect finalDestRect(0, 0, tileStampSize, tileStampSize);

		// Blitting each little tile onto the final tile texture
		for (int y = 0; y < 2; y++) {
			for (int x = 0; x < 2; x++) {
				finalDestRect.x = x * tileStampSize;
				finalDestRect.y = y * tileStampSize;
				SDL_RenderCopy(Game::renderer, tileSheet, &finalSrcRect, &finalDestRect);
			}
		}
		SDL_DestroyTexture(tileSheet);
		SDL_SetRenderTarget(Game::renderer, NULL);

		// Assigning components
		Collision* wallColl = Game::ecs.getComponent<Collision>(testWall);
		*wallColl = Collision{
			.hitWidth = 64,
			.hitHeight = 64,
			.physicsTags = {"wall", "canPush", "canHoldPortal"}
		};

		Sprite* wallSprite = Game::ecs.getComponent<Sprite>(testWall);
		*wallSprite = Sprite{
			.tileWidth = tileSize,
			.tileHeight = tileSize,
			.spriteSheet = finalWallImage
		};

		Transform* wallTrans = Game::ecs.getComponent<Transform>(testWall);
		*wallTrans = Transform{
			.pos = Vector2(tileSize * tilePosX, tileSize * tilePosY)  // TODO: Verify this is correct
		};
	}
}