#include "Room.hpp"
#include <fstream>
#include <sstream>
#include <iostream>
#include <memory>
#include <cassert>

#include "Components/Player.hpp"
#include "Components/Sprite.hpp"
#include "Components/Transform.hpp"

#include "RoomTile.hpp"
#include "WindowManager.hpp"
#include "InputManager.hpp"


Camera Room::camera = Camera(300, 300, 0, 0);

int Room::roomX = 0;

int Room::roomY = 0;

int Room::roomWidth = 0;

int Room::roomHeight = 0;

bool Room::canScrollX = true;

bool Room::canScrollY = true;

std::unordered_map<Entity, Entity> Room::portalLinks;

Room::Room(int roomX, int roomY) {
	this->roomX = roomX;
	this->roomY = roomY;

	Game::ecs.assignComponent<Player>(Game::stack.peek(), player);

	// ----- Player ----- //
	Sprite* playerSprite = Game::ecs.assignComponent<Sprite>(Game::stack.peek(), player);
	playerSprite->spriteSheet = TextureManager::loadTexture(Game::renderer, "Assets/orbeeto.png");
	
	Transform* playerTrans = Game::ecs.assignComponent<Transform>(Game::stack.peek(), player);
	playerTrans->pos = Vector2(300, 300);
	
	Collision* playerColl = Game::ecs.assignComponent<Collision>(Game::stack.peek(), player);
	playerColl->hitWidth = 32;
	playerColl->hitHeight = 32;
	playerColl->hitPos = Vector2(300.0f, 300.0f);
	
	Game::ecs.assignComponent<Pushable_PTag>(Game::stack.peek(), player);
	Game::ecs.assignComponent<CanPush_PTag>(Game::stack.peek(), player);
	Game::ecs.assignComponent<Hurtable_PTag>(Game::stack.peek(), player);
	Game::ecs.assignComponent<CanTeleport_PTag>(Game::stack.peek(), player);

	Hp* playerHp = Game::ecs.assignComponent<Hp>(Game::stack.peek(), player);
	playerHp->hp = 25;
	playerHp->maxHp = 50;

	Defense* pDef = Game::ecs.assignComponent<Defense>(Game::stack.peek(), player);
	pDef->maxDef = 10;
	pDef->def = 10;

	// ----- Left Gun ----- //
	Sprite* lGunSprite = Game::ecs.assignComponent<Sprite>(Game::stack.peek(), leftGun);
	lGunSprite->layer = 1;
	lGunSprite->spriteSheet = TextureManager::loadTexture(Game::renderer, "Assets/orbeetoguns.png");

	Transform* lGunTrans = Game::ecs.assignComponent<Transform>(Game::stack.peek(), leftGun);
	lGunTrans->pos = Vector2(300.0f, 300.0f);

	PlayerGun* lGun = Game::ecs.assignComponent<PlayerGun>(Game::stack.peek(), leftGun);
	lGun->owner = player;

	// ----- Right Gun ----- //
	PlayerGun* rGun = Game::ecs.assignComponent<PlayerGun>(Game::stack.peek(), rightGun);
	rGun->owner = player;
	rGun->isLeft = false;

	Sprite* rGunSprite = Game::ecs.assignComponent<Sprite>(Game::stack.peek(), rightGun);
	rGunSprite->layer = 1;
	rGunSprite->index = 5;
	rGunSprite->spriteSheet = TextureManager::loadTexture(Game::renderer, "Assets/orbeetoguns.png");

	Game::ecs.assignComponent<Transform>(Game::stack.peek(), rightGun);

	// Player's HP Bar
	Entity playerHpBar = Game::ecs.createEntity(Game::stack.peek());

	EntityAI* phbMove = Game::ecs.assignComponent<EntityAI>(Game::stack.peek(), playerHpBar);
	phbMove->ai = AiType::follow_entity;

	auto* feAI = Game::ecs.assignComponent<FollowEntityAI>(Game::stack.peek(), playerHpBar);
	feAI->entityRef = player;
	feAI->distOffset = Vector2(0, 40);

	Transform* phbTrans = Game::ecs.assignComponent<Transform>(Game::stack.peek(), playerHpBar);
	phbTrans->pos = { 0, 0 };

	Sprite* phbSprite = Game::ecs.assignComponent<Sprite>(Game::stack.peek(), playerHpBar);
	phbSprite->tileWidth = 128;
	phbSprite->tileHeight = 16;
	phbSprite->srcRect.w = 128;
	phbSprite->srcRect.h = 16;
	phbSprite->destRect.w = 128;
	phbSprite->destRect.h = 16;
	phbSprite->ignoreScaling = true;
	phbSprite->spriteSheet = TextureManager::loadTexture(Game::renderer, "Assets/health_bar.png");

	StatBar* phbStatBar = Game::ecs.assignComponent<StatBar>(Game::stack.peek(), playerHpBar);
	phbStatBar->maxVal = &playerHp->maxHp;
	phbStatBar->val = &playerHp->hp;

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
	roomX = x;
	roomY = y;

	if (roomX == 0 && roomY == 0) {
		roomWidth = 1280;
		roomHeight = 720;
		canScrollX = true;
		canScrollY = true;
		//readRoomData(extractRoomTiles("RoomLayouts/newSerializeTest.dat"));

		RoomTile tile1 = RoomTile(0, 0, 4, 720 / 16, 0, 0, 2);
		Entity w1 = tile1.buildTile();

		RoomTile tile2 = RoomTile(1280 / 16 - 4, 8, 4, 4, 0, 0, 2);
		Entity w2 = tile2.buildTile();

		RoomTile border = RoomTile(4, 0, 76, 4, 0, 0, 0);
		Entity b1 = border.buildTile();

		/*RoomChange* rc = Game::ecs.assignComponent<RoomChange>(Game::stack.peek(), tile1Ent);
		rc->jumpTo = Vector2(0, 1);
		rc->playerSpawnPos = Vector2(300, 300);*/
	}
	else if (roomX == 0 && roomY == 1) {
		roomWidth = 640;
		roomHeight = 360;
		canScrollX = true;
		canScrollY = true;

		RoomTile tile1 = RoomTile(0, 0, 4, 360 / 16, 0, 0, 2);
		Entity w1 = tile1.buildTile();
	}
}

void Room::update() {
	Transform* pTransform = Game::ecs.getComponent<Transform>(Game::stack.peek(), player);
	if (pTransform) {
		Room::camera.cinematicFocus(player, canScrollX, canScrollY, roomWidth, roomHeight);
	}

	// Gamestate change test
	if (stateChanges != InputManager::keysReleased[SDLK_x] && InputManager::keysReleased[SDLK_x] % 2 != 0) {
		Game::stack.push(StateName::INVENTORY);
		stateChanges = InputManager::keysReleased[SDLK_x];
	}
	else if (stateChanges != InputManager::keysReleased[SDLK_x]) {
		Game::stack.pop();
		stateChanges = InputManager::keysReleased[SDLK_x];
	}

	// Zooming in and out
	if (zoomOutInputCopy < InputManager::keysReleased[SDLK_o]) {
		camera.setWidth(camera.getWidth() + Window::WIDTH / 2);
		camera.setHeight(camera.getWidth() / Window::getAspectRatio().first * Window::getAspectRatio().second);
		zoomOutInputCopy = InputManager::keysReleased[SDLK_o];
	}
	if (zoomInInputCopy < InputManager::keysReleased[SDLK_p]) {
		camera.setWidth(camera.getWidth() - Window::WIDTH / 2);
		camera.setHeight(camera.getWidth() / Window::getAspectRatio().first * Window::getAspectRatio().second);
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