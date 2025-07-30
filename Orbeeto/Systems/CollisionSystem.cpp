#include "CollisionSystem.hpp"
#include <algorithm>
#include "../Room.hpp"
#include "../WindowManager.hpp"


Quadtree CollisionSystem::tree = Quadtree(QuadBox{ 0, 0, 1280, 720 });

CollisionSystem::CollisionSystem() {
	handlers.emplace_back(std::make_unique<PushHandler>());
	handlers.emplace_back(std::make_unique<PortalTeleportHandler>());
	handlers.emplace_back(std::make_unique<GrappleHandler>());
	handlers.emplace_back(std::make_unique<PortalSpawningHandler>());
	handlers.emplace_back(std::make_unique<ProjHitHandler>());
}

void CollisionSystem::queryTree(QuadBox box, std::vector<Entity>& found) {
	tree.query(box, found);
}

void CollisionSystem::update() {
	float roomW = Room::getRoomWidth();
	float roomH = Room::getRoomHeight();

	rebuildQuadtree(QuadBox{ 0.0f, 0.0f, roomW, roomH });
	std::vector<Entity> found;

	int clipSize = 80;
	for (int y = 0; y <= roomH; y = y + clipSize) {
		for (int x = 0; x <= roomW; x = x + clipSize) {
			//std::cout << "Bound x: " << x << ", Bound y: " << y << std::endl;
			tree.query(QuadBox{ (float)x, (float)y, (float)clipSize, (float)clipSize }, found);
			//std::cout << "Bound posX: " << j << " Bound posY: " << i << " Found: " << found.size() << std::endl;

			for (Entity& entity : found) {
				Collision* collision = Game::ecs.getComponent<Collision>(Game::stack.peek(), entity);
				if (collision == nullptr) continue;
				Transform* transform = Game::ecs.getComponent<Transform>(Game::stack.peek(), entity);

				collision->hitPos = transform->pos;

				for (auto& other : found) {
					if (other == entity) continue;

					Collision* oCollide = Game::ecs.getComponent<Collision>(Game::stack.peek(), other);
					if (oCollide == nullptr) continue;

					if (checkForCollision(collision, oCollide)) {
						evaluateCollision(entity, collision, transform, other, oCollide);
					}
				}
			}
			found.clear();
		}
	}
}

void CollisionSystem::rebuildQuadtree(QuadBox boundary) {
	tree = Quadtree(boundary);
	for (Entity& entity : Game::ecs.getSystemGroup<Collision, Transform>(Game::stack.peek())) {
		//std::cout << tree.insert(entity) << std::endl;
		tree.insert(entity);
	}
}

bool CollisionSystem::checkForCollision(const Collision* eColl, const Collision* oColl) {
	double eHalfWidth = eColl->hitWidth / 2.0;
	double eHalfHeight = eColl->hitHeight / 2.0;
	double oHalfWidth = oColl->hitWidth / 2.0;
	double oHalfHeight = oColl->hitHeight / 2.0;

	if (eColl->hitPos.x + eHalfWidth >= oColl->hitPos.x - oHalfWidth
		&& eColl->hitPos.x - eHalfWidth <= oColl->hitPos.x + oHalfWidth
		&& eColl->hitPos.y + eHalfHeight >= oColl->hitPos.y - oHalfHeight
		&& eColl->hitPos.y - eHalfHeight <= oColl->hitPos.y + oHalfHeight) {
		return true;
	}
	return false;
}

void CollisionSystem::evaluateCollision(Entity& entity, Collision* eColl, Transform* eTrans, Entity& other, Collision* oColl) {
	Transform* oTrans = Game::ecs.getComponent<Transform>(Game::stack.peek(), other);
	
	for (auto& handler : handlers) {
		if (handler->handle(entity, eColl, eTrans, other, oColl, oTrans)) {
			return;
		}
	}
}

bool CollisionSystem::hasPhysicsTag(const Collision* coll, int tag) {
	return coll->physicsTags.test(tag);
}


int ICollisionHandler::intersection(const Collision* aColl, const Collision* bColl) {
	Vector2 dist(aColl->hitPos.x - bColl->hitPos.x, aColl->hitPos.y - bColl->hitPos.y);  // Euclidian distance between hitboxes
	Vector2 minDist((aColl->hitWidth + bColl->hitWidth) / 2, (aColl->hitHeight + bColl->hitHeight) / 2);

	Vector2 depth;
	depth.x = dist.x > 0 ? minDist.x - dist.x : -minDist.x - dist.x;
	depth.y = dist.y > 0 ? minDist.y - dist.y : -minDist.y - dist.y;

	if (depth.x != 0 && depth.y != 0) {
		if (abs(depth.x) < abs(depth.y)) {  // Collision along x-axis
			if (depth.x > 0) return 1;
			else return 3;
		}
		else {  // Collision along y-axis
			if (depth.y > 0) return 0;
			else return 2;
		}
	}

	return -1;
}


bool PushHandler::handle(Entity a, Collision* aColl, Transform* aTrans,
						 Entity b, Collision* bColl, Transform* bTrans) {
	if (aColl->physicsTags.test((int)PTags::PUSHABLE) && bColl->physicsTags.test((int)PTags::CAN_PUSH)) {
		int side = intersection(aColl, bColl);

		if (side == 0  // South
			&& (aTrans->vel.y < 0 || bTrans->vel.y > 0)
			&& aTrans->pos.y - aColl->hitHeight / 2 <= bTrans->pos.y + bColl->hitHeight / 2) {
			aTrans->vel.y = 0;
			aTrans->pos.y = bTrans->pos.y + bColl->hitHeight / 2 + aColl->hitHeight / 2;
		}
		if (side == 1  // East
			&& (aTrans->vel.x < 0 || bTrans->vel.x > 0)
			&& aTrans->pos.x - aColl->hitWidth / 2 <= bTrans->pos.x + bColl->hitWidth / 2) {
			aTrans->vel.x = 0;
			aTrans->pos.x = bTrans->pos.x + bColl->hitWidth / 2 + aColl->hitWidth / 2;
		}
		if (side == 2  // North
			&& (aTrans->vel.y > 0 || bTrans->vel.y < 0)
			&& aTrans->pos.y + aColl->hitHeight / 2 >= bTrans->pos.y - bColl->hitHeight / 2) {
			aTrans->vel.y = 0;
			aTrans->pos.y = bTrans->pos.y - bColl->hitHeight / 2 - aColl->hitHeight / 2;
		}
		if (side == 3  // West
			&& (aTrans->vel.x > 0 || bTrans->vel.x < 0)
			&& aTrans->pos.x + aColl->hitWidth / 2 >= bTrans->pos.x - bColl->hitWidth / 2) {
			aTrans->vel.x = 0;
			aTrans->pos.x = bTrans->pos.x - bColl->hitWidth / 2 - aColl->hitWidth / 2;
		}
		
		return true;
	}
	return false;
}


bool PortalTeleportHandler::handle(Entity a, Collision* aColl, Transform* aTrans,
								   Entity b, Collision* bColl, Transform* bTrans) {
	if (aColl->physicsTags.test((int)PTags::CAN_TELEPORT) && bColl->physicsTags.test((int)PTags::PORTAL)) {
		TeleportLink* firstLink = Game::ecs.getComponent<TeleportLink>(Game::stack.peek(), b);
		TeleportLink* secondLink = Game::ecs.getComponent<TeleportLink>(Game::stack.peek(), Room::getPortalLink(b));

		if (secondLink == nullptr) return false;

		Transform* outPortalTrans = Game::ecs.getComponent<Transform>(Game::stack.peek(), Room::getPortalLink(b));
		Collision* outPortalColl = Game::ecs.getComponent<Collision>(Game::stack.peek(), Room::getPortalLink(b));

		// Getting offset from center of portal
		float offset = 0.0;
		if (firstLink->facing == 0 || firstLink->facing == 2) {
			offset = bColl->hitPos.x - aColl->hitPos.x;
		}
		else {
			offset = bColl->hitPos.y - aColl->hitPos.y;
		}

		std::unordered_map<int, double> directionMap = {  // Defaults to first portal facing south
			{0, 180.0},
			{1, 90.0},
			{2, 0.0},
			{3, 270.0}
		};

		if (secondLink != nullptr) {
			// Placing entity at new location
			float width = (outPortalColl->hitWidth + aColl->hitWidth) / 2 + 1;  // Add 1 to each direction to prevent immediate re-entry
			float height = (outPortalColl->hitHeight + aColl->hitHeight) / 2 + 1;

			if (secondLink->facing == 0) {
				aTrans->pos = { outPortalTrans->pos.x + offset, outPortalTrans->pos.y + height };
			}
			else if (secondLink->facing == 1) {
				aTrans->pos = { outPortalTrans->pos.x + width, outPortalTrans->pos.y + offset };
			}
			else if (secondLink->facing == 2) {
				aTrans->pos = { outPortalTrans->pos.x + offset, outPortalTrans->pos.y - height };
			}
			else if (secondLink->facing == 3) {
				aTrans->pos = { outPortalTrans->pos.x - width, outPortalTrans->pos.y + offset };
			}

			// Rotating velocity
			if (firstLink->facing == 1) {
				directionMap.clear();
				directionMap = {
					{0, 270.0},
					{1, 180.0},
					{2, 90.0},
					{3, 0.0}
				};
			}
			else if (firstLink->facing == 2) {
				directionMap.clear();
				directionMap = {
					{0, 0.0},
					{1, 270.0},
					{2, 180.0},
					{3, 90.0}
				};
			}
			else if (firstLink->facing == 3) {
				directionMap.clear();
				directionMap = {
					{0, 90.0},
					{1, 0.0},
					{2, 270.0},
					{3, 180.0}
				};
			}

			aTrans->vel.rotate(directionMap[secondLink->facing]);
			if (aColl->tpFlag == false) {
				//std::cout << "Flipped true!\n";
				aColl->tpFlag = true;
			}
			else {
				//std::cout << "Flipped false!\n";
				aColl->tpFlag = false;
			}
		}
		return true;
	}
	return false;
}


bool GrappleHandler::handle(Entity a, Collision* aColl, Transform* aTrans,
							Entity b, Collision* bColl, Transform* bTrans) {
	if (aColl->physicsTags.test((int)PTags::GRAPPLE)) {
		Grapple* grapple = Game::ecs.getComponent<Grapple>(Game::stack.peek(), a);
		Player* player = Game::ecs.getComponent<Player>(Game::stack.peek(), grapple->owner);

		if (bColl->physicsTags.test((int)PTags::PLAYER) && player->grappleState == GrappleState::RETURNING) {
			Game::ecs.destroyEntity(Game::stack.peek(), a);
			player->grappleRef = 0;  // Remove grapple reference from player
			player->moveToGrapple = false;

			player->grappleState = GrappleState::INACTIVE;
			return true;
		}

		if (bColl->physicsTags.test((int)PTags::WALL) && player->grappleState == GrappleState::SENT) {
			player->grappleState = GrappleState::LATCHED;
			grapple->grappledTo = b;
			player->moveToGrapple = true;
		}
		return true;
	}
	return false;
}


bool PortalSpawningHandler::handle(Entity a, Collision* aColl, Transform* aTrans,
								   Entity b, Collision* bColl, Transform* bTrans) {
	if (aColl->physicsTags.test((int)PTags::PORTAL_BULLET) && bColl->physicsTags.test((int)PTags::CAN_HOLD_PORTAL)) {
		int side = intersection(aColl, bColl);  // The direction the spawned portal will face
		std::cout << side << std::endl;
		Entity portal = Game::ecs.createEntity(Game::stack.peek());

		Game::ecs.assignComponent<Sprite>(Game::stack.peek(), portal);
		Game::ecs.assignComponent<Transform>(Game::stack.peek(), portal);
		Game::ecs.assignComponent<Collision>(Game::stack.peek(), portal);
		Game::ecs.assignComponent<TeleportLink>(Game::stack.peek(), portal);

		Sprite* pSprite = Game::ecs.getComponent<Sprite>(Game::stack.peek(), portal);
		pSprite->spriteSheet = TextureManager::loadTexture(Game::renderer, "Assets/orbeeto.png");
		pSprite->layer = 20;

		Transform* pTrans = Game::ecs.getComponent<Transform>(Game::stack.peek(), portal);

		*pTrans = Transform();
		pTrans->pos = aTrans->pos;

		Collision* pColl = Game::ecs.getComponent<Collision>(Game::stack.peek(), portal);
		pColl->hitWidth = 64;
		pColl->hitHeight = 64;
		pColl->hitPos = aTrans->pos;

		pColl->physicsTags.set((int)PTags::PORTAL);

		TeleportLink* pTLink = Game::ecs.getComponent<TeleportLink>(Game::stack.peek(), portal);
		*pTLink = TeleportLink();
		pTLink->facing = side;

		Bullet* pBullet = Game::ecs.getComponent<Bullet>(Game::stack.peek(), a);
		Player* player = Game::ecs.getComponent<Player>(Game::stack.peek(), pBullet->shotBy);

		// Updating active player portals. If two are alredy active the oldest one will be replaced by the new one
		if (player->portals.first == 0) {  // No portals fired yet
			player->portals.first = portal;
		}
		else {
			TeleportLink* otherLink = Game::ecs.getComponent<TeleportLink>(Game::stack.peek(), player->portals.first);

			if (player->portals.second == 0) {  // Only 1 portal fired so far
				player->portals.second = portal;

				// Linking portals for player
				pTLink->linkedTo = player->portals.first;
				otherLink->linkedTo = player->portals.second;

				// Linking portals for room
				Room::newPortalLink(player->portals.first, player->portals.second);
				Room::newPortalLink(player->portals.second, player->portals.first);

				std::cout << "Linked " << player->portals.first << " to " << Room::getPortalLink(player->portals.first) << std::endl;
				std::cout << "Linked " << player->portals.second << " to " << Room::getPortalLink(player->portals.second) << std::endl;
			}
			else {  // Currently 2 portals active
				Room::removePortalLink(player->portals.first);
				Room::removePortalLink(player->portals.second);
				Game::ecs.destroyEntity(Game::stack.peek(), player->portals.first);

				player->portals.first = player->portals.second;
				player->portals.second = portal;

				// Linking portals for player
				pTLink->linkedTo = player->portals.first;
				otherLink->linkedTo = player->portals.second;

				// Linking portals for room
				Room::newPortalLink(player->portals.first, player->portals.second);
				Room::newPortalLink(player->portals.second, player->portals.first);

				std::cout << "Linked " << player->portals.first << " to " << Room::getPortalLink(player->portals.first) << std::endl;
				std::cout << "Linked " << player->portals.second << " to " << Room::getPortalLink(player->portals.second) << std::endl;
			}
		}
		Game::ecs.destroyEntity(Game::stack.peek(), a);
		return true;
	}
	return false;
}


bool ProjHitHandler::handle(Entity a, Collision* aColl, Transform* aTrans,
									Entity b, Collision* bColl, Transform* bTrans) {
	if (aColl->physicsTags.test((int)PTags::PROJECTILE) && bColl->physicsTags.test((int)PTags::WALL)) {
		Game::ecs.destroyEntity(Game::stack.peek(), a);
		return true;
	}
	else if (aColl->physicsTags.test((int)PTags::E_PROJECTILE) && bColl->physicsTags.test((int)PTags::PLAYER)) {
		Hp* hp = Game::ecs.getComponent<Hp>(Game::stack.peek(), b);
		Defense* def = Game::ecs.getComponent<Defense>(Game::stack.peek(), b);
		Bullet* bullet = Game::ecs.getComponent<Bullet>(Game::stack.peek(), b);

		int halving = 50;
		hp->hp -= std::floor(halving * bullet->damage / (halving + def->def));

		Game::ecs.destroyEntity(Game::stack.peek(), a);
		return true;
	}
	return false;
}