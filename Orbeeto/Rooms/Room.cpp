#include "Room.hpp"
#include <fstream>
#include <sstream>
#include <iostream>
#include <memory>
#include <cassert>

#include "../Components/Player.hpp"
#include "../Components/Sprite.hpp"
#include "../Components/Transform.hpp"

#include "../WindowManager.hpp"
#include "../InputManager.hpp"


Camera Room::camera = Camera(300, 300, WindowManager::SCREENWIDTH, WindowManager::SCREENHEIGHT);

int Room::roomX = 0;

int Room::roomY = 0;

int Room::roomWidth = 0;

int Room::roomHeight = 0;

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

	Game::ecs.assignComponent<Sprite>(rightGun);
	Game::ecs.assignComponent<PlayerGun>(rightGun);
	Game::ecs.assignComponent<Transform>(rightGun);

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
	};
	playerColl->physicsTags.set(PTags::PLAYER);
	playerColl->physicsTags.set(PTags::PUSHABLE);
	playerColl->physicsTags.set(PTags::CAN_PUSH);
	playerColl->physicsTags.set(PTags::HURTABLE);
	playerColl->physicsTags.set(PTags::CAN_TELEPORT);

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
		.owner = player,
	};

	// ----- Right Gun ----- //
	PlayerGun* rGun = Game::ecs.getComponent<PlayerGun>(rightGun);
	*rGun = PlayerGun{
		.owner = player,
		.isLeft = false
	};

	Sprite* rGunSprite = Game::ecs.getComponent<Sprite>(rightGun);
	*rGunSprite = Sprite{
		.layer = 1,
		.tileWidth = 64,
		.tileHeight = 64,
		.index = 5,
		.spriteSheet = TextureManager::loadTexture(Game::renderer, "Assets/orbeetoguns.png"),
	};

	loadRoom(0, 0);
}

int Room::getRoomX() {
	return roomX;
}

int Room::getRoomY() {
	return roomY;
}

int Room::getRoomWidth() {
	return roomWidth;
}

int Room::getRoomHeight() {
	return roomHeight;
}

void Room::loadRoom(int x, int y) {
	
	
	if (roomX == 0 && roomY == 0) {
		roomWidth = 1280;
		roomHeight = 720;
		canScrollX = true;
		canScrollY = true;
		readRoomData(extractRoomTiles("Rooms/RoomLayouts/newSerializeTest.dat"));

		// ----- Test Enemy 1 ----- //
		Entity enemyTest = Game::ecs.createEntity();

		Game::ecs.assignComponent<Transform>(enemyTest);
		Game::ecs.assignComponent<Sprite>(enemyTest);
		Game::ecs.assignComponent<Collision>(enemyTest);
		Game::ecs.assignComponent<MovementAI>(enemyTest);

		Transform* e1Trans = Game::ecs.getComponent<Transform>(enemyTest);
		*e1Trans = Transform{
			.pos = { 200, 200 }
		};

		Sprite* e1Sprite = Game::ecs.getComponent<Sprite>(enemyTest);
		*e1Sprite = Sprite{
			.tileWidth = 64,
			.tileHeight = 64,
			.spriteSheet = TextureManager::loadTexture(Game::renderer, "Assets/orbeeto.png")
		};

		Collision* e1Coll = Game::ecs.getComponent<Collision>(enemyTest);
		*e1Coll = Collision{
			.hitWidth = 64,
			.hitHeight = 64,
		};
		e1Coll->physicsTags.set(PTags::ENEMY);
		e1Coll->physicsTags.set(PTags::PUSHABLE);

		MovementAI* e1AI = Game::ecs.getComponent<MovementAI>(enemyTest);
		*e1AI = MovementAI{
			.ai = M_AI::OCTOGRUNT
		};
	}
}

void Room::update() {
	Transform* pTransform = Game::ecs.getComponent<Transform>(player);
	Room::camera.cinematicFocus(pTransform->pos.x, pTransform->pos.y, pTransform->vel, pTransform->accelConst);

	// Zooming in and out
	if (zoomOutInputCopy < InputManager::keysReleased[SDLK_o]) {
		camera.setWidth(camera.getWidth() - 256);
		camera.setHeight(camera.getWidth() / WindowManager::A_RATIO.first * WindowManager::A_RATIO.second);
		zoomOutInputCopy = InputManager::keysReleased[SDLK_o];
	}
	if (zoomInInputCopy < InputManager::keysReleased[SDLK_p]) {
		camera.setWidth(camera.getWidth() + 256);
		camera.setHeight(camera.getWidth() / WindowManager::A_RATIO.first * WindowManager::A_RATIO.second);
		zoomInInputCopy = InputManager::keysReleased[SDLK_p];
	}
}

void Room::newPortalLink(Entity& first, Entity& second) {
	portalLinks[first] = second;
}

void Room::removePortalLink(Entity& portal) {
	auto it = portalLinks.find(portal);
	if (it != portalLinks.end()) portalLinks.erase(it);
	else std::cout << "Link could not be found\n";
}

Entity Room::getPortalLink(Entity portal) {
	return portalLinks[portal];
}

void Room::clearPortalLinks() {
	portalLinks.clear();
}

std::vector<std::vector<uint8_t>> Room::extractRoomTiles(const std::string roomFileName) {
	std::ifstream roomFile(roomFileName);
	assert(roomFile.is_open() && "Error opening room data file.");

	std::vector<std::vector<uint8_t>> output;
	if (roomFile.peek() == EOF) return output;

	std::vector<uint8_t> currentTile;
	std::string currentVal = "";

	char c;
	while (roomFile.get(c)) {
		if (c == ' ') {
			uint8_t tile = std::stoul(currentVal, nullptr, 16);
			currentTile.push_back(tile);
			currentVal = "";
		}
		else if (c == '\n') {
			output.push_back(currentTile);
			currentTile.clear();
			currentVal = "";
		}
		else {
			currentVal += c;
		}
	}
	// Including last tile of last row
	uint8_t tile = std::stoul(currentVal, nullptr, 16);
	currentTile.push_back(tile);

	// Including entire last row
	output.push_back(currentTile);

	roomFile.close();
	return output;
}

void Room::readRoomData(const std::vector<std::vector<uint8_t>> roomTiles) {
	if (roomTiles.size() == 0) return;

	int numTiles = roomTiles.size();
	for (int tile = 0; tile < numTiles; tile++) {
		buildRoomEntity(roomTiles[tile]);
	}
}

enum TileInfo {
	XPOS,
	YPOS,
	WIDTH,
	HEIGHT,
	PROPERTIES,
	TILESET,
	TILETYPE,
	STYLE,
	ADJ
};

enum TileProperties {
	SOLID,
	INVISIBLE,
};

void Room::buildRoomEntity(const std::vector<uint8_t>& tileInfo) {
	assert(tileInfo[TileInfo::WIDTH] >= 0 && tileInfo[TileInfo::HEIGHT] >= 0 && "Tile must have positive, non-zero dimensions.");
	Entity tile = Game::ecs.createEntity();

	// Turning properties value into a bitset for easy manip
	std::bitset<8> props = tileInfo[TileInfo::PROPERTIES];

	int tileSize = 16;  // The size of each individual tile image
	int finalWidth = tileSize * tileInfo[TileInfo::WIDTH];
	int finalHeight = tileSize * tileInfo[TileInfo::HEIGHT];
	SDL_Texture* tileSheet = TextureManager::loadTexture(Game::renderer, "Assets/wall.png");

	switch (tileInfo[TileInfo::TILESET]) {  // Selecting a tile sheet
	case 0x00:
		break;
	default:
		break;
	}

	SDL_Texture* finalImage = SDL_CreateTexture(Game::renderer, SDL_PIXELFORMAT_RGBA8888, SDL_TEXTUREACCESS_TARGET, tileSize * tileInfo[TileInfo::WIDTH], tileSize * tileInfo[TileInfo::HEIGHT]);
	SDL_SetTextureBlendMode(finalImage, SDL_BLENDMODE_BLEND);
	SDL_SetRenderTarget(Game::renderer, finalImage);

	SDL_Rect srcRect = { 0, 0, tileSize, tileSize };
	SDL_Rect destRect = { 0, 0, tileSize, tileSize };

	// Selecting a tile group within a sheet
	srcRect.y = tileSize * tileInfo[TileInfo::TILETYPE];

	int w = tileInfo[TileInfo::WIDTH];  // Width of tile in tile sizes
	int h = tileInfo[TileInfo::HEIGHT];  // Height of tile in tile sizes

	switch (tileInfo[TileInfo::STYLE]) {  // Creating the final tile's image
	case 0x00:  // Standard tiling, repeat first tile
		for (int y = 0; y < h; y++) {
			for (int x = 0; x < w; x++) {
				destRect.x = x * tileSize;
				destRect.y = y * tileSize;
				SDL_RenderCopy(Game::renderer, tileSheet, &srcRect, &destRect);
			}
		}
		break;

	case 0x01:  // Full bordering
		for (int y = 0; y < h; y++) {
			for (int x = 0; x < w; x++) {
				if (y == 0 && x == 0) {  // Northwest corner
					srcRect.x = tileSize * 7;
				}
				else if (y == 0 && x == w - 1) {  // Northeast corner
					srcRect.x = tileSize * 6;
				}
				else if (y == h - 1 && x == 0) {  // Southwest corner
					srcRect.x = tileSize * 8;
				}
				else if (y == h - 1 && x == w - 1) {  // Southeast corner
					srcRect.x = tileSize * 5;
				}
				else if (y == h - 1) {  // Southern border
					srcRect.x = tileSize * 1;
				}
				else if (x == w - 1) {  // Eastern border
					srcRect.x = tileSize * 2;
				}
				else if (y == 0) {  // Northern border
					srcRect.x = tileSize * 3;
				}
				else if (x == 0) {  // Western border
					srcRect.x = tileSize * 4;
				}

				destRect.x = x * tileSize;
				destRect.y = y * tileSize;
				SDL_RenderCopy(Game::renderer, tileSheet, &srcRect, &destRect);

				srcRect.x = 0;
			}
		}
		break;

	default:
		break;
	}
	SDL_SetRenderTarget(Game::renderer, NULL);
	SDL_DestroyTexture(tileSheet);

	// ----- Assigning Components ----- //

	Game::ecs.assignComponent<Transform>(tile);
	Transform* transform = Game::ecs.getComponent<Transform>(tile);
	*transform = {
		.pos = Vector2(tileSize * tileInfo[TileInfo::XPOS] + finalWidth / 2,
					   tileSize * tileInfo[TileInfo::YPOS] + finalHeight / 2),
	};
	std::cout << transform->pos.x << " " << transform->pos.y << std::endl;
		
	if (props.test(TileProperties::SOLID)) {
		Game::ecs.assignComponent<Collision>(tile);
		Collision* coll = Game::ecs.getComponent<Collision>(tile);
		*coll = Collision{
			.hitWidth = finalWidth,
			.hitHeight = finalHeight,
		};
		coll->physicsTags.set(PTags::WALL);
		coll->physicsTags.set(PTags::CAN_PUSH);
		coll->physicsTags.set(PTags::CAN_HOLD_PORTAL);
	}

	if (!props.test(TileProperties::INVISIBLE)) {
		Game::ecs.assignComponent<Sprite>(tile);
		Sprite* sprite = Game::ecs.getComponent<Sprite>(tile);
		*sprite = Sprite{
			.tileWidth = finalWidth,
			.tileHeight = finalHeight,
			.spriteSheet = finalImage,
		};
	}
}