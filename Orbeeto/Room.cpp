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

std::unordered_map<Entity, Entity> Room::portalLinks;

Room::Room(int roomX, int roomY) {
	this->roomX = roomX;
	this->roomY = roomY;

	Game::ecs.assignComponent<Sprite>(Game::stack.peek(), player);
	Game::ecs.assignComponent<Player>(Game::stack.peek(), player);
	Game::ecs.assignComponent<Transform>(Game::stack.peek(), player);
	Game::ecs.assignComponent<Collision>(Game::stack.peek(), player);
	Game::ecs.assignComponent<Hp>(Game::stack.peek(), player);
	Game::ecs.assignComponent<Defense>(Game::stack.peek(), player);

	Game::ecs.assignComponent<Sprite>(Game::stack.peek(), leftGun);
	Game::ecs.assignComponent<PlayerGun>(Game::stack.peek(), leftGun);
	Game::ecs.assignComponent<Transform>(Game::stack.peek(), leftGun);

	Game::ecs.assignComponent<Sprite>(Game::stack.peek(), rightGun);
	Game::ecs.assignComponent<PlayerGun>(Game::stack.peek(), rightGun);
	Game::ecs.assignComponent<Transform>(Game::stack.peek(), rightGun);

	// ----- Player ----- //
	Sprite* playerSprite = Game::ecs.getComponent<Sprite>(Game::stack.peek(), player);
	playerSprite->spriteSheet = TextureManager::loadTexture(Game::renderer, "Assets/orbeeto.png");
	
	Transform* playerTrans = Game::ecs.getComponent<Transform>(Game::stack.peek(), player);
	playerTrans->pos = Vector2(300, 300);
	
	Collision* playerColl = Game::ecs.getComponent<Collision>(Game::stack.peek(), player);
	playerColl->hitWidth = 32;
	playerColl->hitHeight = 32;
	playerColl->hitPos = Vector2(300.0f, 300.0f);
	
	playerColl->physicsTags.set(PTags::PLAYER);
	playerColl->physicsTags.set(PTags::PUSHABLE);
	playerColl->physicsTags.set(PTags::CAN_PUSH);
	playerColl->physicsTags.set(PTags::HURTABLE);
	playerColl->physicsTags.set(PTags::CAN_TELEPORT);

	Hp* playerHp = Game::ecs.getComponent<Hp>(Game::stack.peek(), player);
	playerHp->hp = 25;
	playerHp->maxHp = 50;

	Defense* pDef = Game::ecs.getComponent<Defense>(Game::stack.peek(), player);
	pDef->maxDef = 10;
	pDef->def = 10;

	// ----- Left Gun ----- //
	Sprite* lGunSprite = Game::ecs.getComponent<Sprite>(Game::stack.peek(), leftGun);
	lGunSprite->layer = 1;
	lGunSprite->spriteSheet = TextureManager::loadTexture(Game::renderer, "Assets/orbeetoguns.png");

	Transform* lGunTrans = Game::ecs.getComponent<Transform>(Game::stack.peek(), leftGun);
	lGunTrans->pos = Vector2(300.0f, 300.0f);

	PlayerGun* lGun = Game::ecs.getComponent<PlayerGun>(Game::stack.peek(), leftGun);
	lGun->owner = player;

	// ----- Right Gun ----- //
	PlayerGun* rGun = Game::ecs.getComponent<PlayerGun>(Game::stack.peek(), rightGun);
	rGun->owner = player;
	rGun->isLeft = false;

	Sprite* rGunSprite = Game::ecs.getComponent<Sprite>(Game::stack.peek(), rightGun);
	rGunSprite->layer = 1;
	rGunSprite->index = 5;
	rGunSprite->spriteSheet = TextureManager::loadTexture(Game::renderer, "Assets/orbeetoguns.png");

	// Player's HP Bar
	Entity playerHpBar = Game::ecs.createEntity(Game::stack.peek());

	Game::ecs.assignComponent<StatBar>(Game::stack.peek(), playerHpBar);
	Game::ecs.assignComponent<Sprite>(Game::stack.peek(), playerHpBar);
	Game::ecs.assignComponent<Transform>(Game::stack.peek(), playerHpBar);
	Game::ecs.assignComponent<MovementAI>(Game::stack.peek(), playerHpBar);

	MovementAI* phbMove = Game::ecs.getComponent<MovementAI>(Game::stack.peek(), playerHpBar);
	phbMove->ai = M_AI::FOLLOW_ENTITY;
	phbMove->entityRef = player;
	phbMove->distance = { 0, 40 };

	Transform* phbTrans = Game::ecs.getComponent<Transform>(Game::stack.peek(), playerHpBar);
	phbTrans->pos = { 0, 0 };

	Sprite* phbSprite = Game::ecs.getComponent<Sprite>(Game::stack.peek(), playerHpBar);
	phbSprite->tileWidth = 128;
	phbSprite->tileHeight = 16;
	phbSprite->srcRect.w = 128;
	phbSprite->srcRect.h = 16;
	phbSprite->destRect.w = 128;
	phbSprite->destRect.h = 16;
	phbSprite->ignoreScaling = true;
	phbSprite->spriteSheet = TextureManager::loadTexture(Game::renderer, "Assets/health_bar.png");

	StatBar* phbStatBar = Game::ecs.getComponent<StatBar>(Game::stack.peek(), playerHpBar);
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
	if (roomX == 0 && roomY == 0) {
		roomWidth = 1280;
		roomHeight = 720;
		canScrollX = true;
		canScrollY = true;
		//readRoomData(extractRoomTiles("RoomLayouts/newSerializeTest.dat"));

		RoomTile tile1 = RoomTile(0, 0, 2, 8, 0, 0, 2);
		RoomTile tile2 = RoomTile(4, 0, 8, 2, 0, 0, 2);
		RoomTile tile3 = RoomTile(6, 4, 2, 8, 0, 0, 6);
		RoomTile tile4 = RoomTile(4, 0, 8, 2, 0, 0, 2);
		tile1.buildTile();
		tile2.buildTile();
		tile3.buildTile();

		// ----- Test Enemy 1 ----- //
		/*Entity enemyTest = Game::ecs.createEntity(Game::stack.peek());

		Game::ecs.assignComponent<Transform>(Game::stack.peek(), enemyTest);
		Game::ecs.assignComponent<Sprite>(Game::stack.peek(), enemyTest);
		Game::ecs.assignComponent<Collision>(Game::stack.peek(), enemyTest);
		Game::ecs.assignComponent<MovementAI>(Game::stack.peek(), enemyTest);

		Transform* e1Trans = Game::ecs.getComponent<Transform>(Game::stack.peek(), enemyTest);
		e1Trans->pos = { 200, 200 };

		Sprite* e1Sprite = Game::ecs.getComponent<Sprite>(Game::stack.peek(), enemyTest);
		*e1Sprite = Sprite();
		e1Sprite->spriteSheet = TextureManager::loadTexture(Game::renderer, "Assets/orbeeto.png");

		Collision* e1Coll = Game::ecs.getComponent<Collision>(Game::stack.peek(), enemyTest);

		e1Coll->physicsTags.set(PTags::ENEMY);
		e1Coll->physicsTags.set(PTags::PUSHABLE);

		MovementAI* e1AI = Game::ecs.getComponent<MovementAI>(Game::stack.peek(), enemyTest);
		e1AI->ai = M_AI::OCTOGRUNT;*/
	}
}

void Room::update() {
	Transform* pTransform = Game::ecs.getComponent<Transform>(Game::stack.peek(), player);
	if (pTransform != nullptr) {
		Room::camera.cinematicFocus(player);
	}

	// Zooming in and out
	if (zoomOutInputCopy < InputManager::keysReleased[SDLK_o]) {
		camera.setWidth(camera.getWidth() + Window::WIDTH / 2);
		camera.setHeight(camera.getWidth() / Window::A_RATIO.first * Window::A_RATIO.second);
		zoomOutInputCopy = InputManager::keysReleased[SDLK_o];
	}
	if (zoomInInputCopy < InputManager::keysReleased[SDLK_p]) {
		camera.setWidth(camera.getWidth() - Window::WIDTH / 2);
		camera.setHeight(camera.getWidth() / Window::A_RATIO.first * Window::A_RATIO.second);
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