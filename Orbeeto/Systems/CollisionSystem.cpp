#include "CollisionSystem.hpp"
#include <algorithm>
#include "../Rooms/Room.hpp"


CollisionSystem::CollisionSystem() : tree(QuadBoundingBox{0, 0, 1280, 720}) {}

void CollisionSystem::update() {
	rebuildQuadtree(QuadBoundingBox{0, 0, 1280, 720});
	
	std::vector<Entity> found;

	// TODO:: Adjust to confine to current room
	/*for (int i = 0; i < 720; i = i + 250) {
		for (int j = 0; j < 1280; j = j + 250) {*/
			tree.query(QuadBoundingBox{ (float)0, (float)0, 1280, 720 }, found);
			//std::cout << "Bound posX: " << j << " Bound posY: " << i << " Found: " << found.size() << std::endl;

			for (Entity& entity : found) {
				Collision* collision = Game::ecs.getComponent<Collision>(entity);
				if (collision == nullptr) continue;
				Transform* transform = Game::ecs.getComponent<Transform>(entity);

				collision->hitPos = transform->pos;

				for (auto& other : found) {
					if (other == entity) continue;

					Collision* oCollide = Game::ecs.getComponent<Collision>(other);

					if (oCollide == nullptr) continue;

					if (checkForCollision(collision, oCollide)) {
						evaluateCollision(entity, collision, transform, other, oCollide);
					}
				}
			}
			found.clear();
	/*	}
	}*/

	/*for (Entity& entity : Game::ecs.getSystemGroup<Collision, Transform>()) {
		Collision* collision = Game::ecs.getComponent<Collision>(entity);
		Transform* transform = Game::ecs.getComponent<Transform>(entity);

		collision->hitPos = transform->pos;

		// Evaluating every entity in the system for a collision
		for (Entity& other : Game::ecs.getSystemGroup<Collision, Transform>()) {
			if (other == entity) continue;
			Collision* oCollide = Game::ecs.getComponent<Collision>(other);

			if (oCollide == nullptr) continue;

			if (checkForCollision(collision, oCollide)) {
				evaluateCollision(entity, collision, transform, other, oCollide);
			}
		}
	}*/
}

void CollisionSystem::rebuildQuadtree(QuadBoundingBox boundary) {
	tree = Quadtree(boundary);
	for (Entity& entity : Game::ecs.getSystemGroup<Collision, Transform>()) {
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

int CollisionSystem::intersection(const Collision* eColl, const Collision* oColl) {
	Vector2 dist(eColl->hitPos.x - oColl->hitPos.x, eColl->hitPos.y - oColl->hitPos.y);  // Euclidian distance between hitboxes
	Vector2 minDist((eColl->hitWidth + oColl->hitWidth) / 2, (eColl->hitHeight + oColl->hitHeight) / 2);

	Vector2 depth;
	depth.x = dist.x > 0 ? minDist.x - dist.x : -minDist.x - dist.x;
	depth.y = dist.y > 0 ? minDist.y - dist.y : -minDist.y - dist.y;

	if (depth.x != 0 && depth.y != 0) {
		if (abs(depth.x) < abs(depth.y)) {  // Collision along x-axis
			if (depth.x > 0) return Facing::EAST;
			else return Facing::WEST;
		}
		else {  // Collision along y-axis
			if (depth.y > 0) return Facing::SOUTH;
			else return Facing::NORTH;
		}
	}

	return -1;
}

void CollisionSystem::pushEntity(Collision* coll1, Transform* trans1, Collision* coll2, Transform* trans2) {
	int side = intersection(coll1, coll2);

	if (side == Facing::SOUTH  // South
		&& (trans1->vel.y < 0 || trans2->vel.y > 0)
		&& trans1->pos.y - coll1->hitHeight / 2 <= trans2->pos.y + coll2->hitHeight / 2) {
		trans1->vel.y = 0;
		trans1->pos.y = trans2->pos.y + coll2->hitHeight / 2 + coll1->hitHeight / 2;
	}
	if (side == Facing::EAST  // East
		&& (trans1->vel.x < 0 || trans2->vel.x > 0)
		&& trans1->pos.x - coll1->hitWidth / 2 <= trans2->pos.x + coll2->hitWidth / 2) {
		trans1->vel.x = 0;
		trans1->pos.x = trans2->pos.x + coll2->hitWidth / 2 + coll1->hitWidth / 2;
	}
	if (side == Facing::NORTH  // North
		&& (trans1->vel.y > 0 || trans2->vel.y < 0)
		&& trans1->pos.y + coll1->hitHeight / 2 >= trans2->pos.y - coll2->hitHeight / 2) {
		trans1->vel.y = 0;
		trans1->pos.y = trans2->pos.y - coll2->hitHeight / 2 - coll1->hitHeight / 2;
	}
	if (side == Facing::WEST  // West
		&& (trans1->vel.x > 0 || trans2->vel.x < 0)
		&& trans1->pos.x + coll1->hitWidth / 2 >= trans2->pos.x - coll2->hitWidth / 2) {
		trans1->vel.x = 0;
		trans1->pos.x = trans2->pos.x - coll2->hitWidth / 2 - coll1->hitWidth / 2;
	}
}

Vector2 CollisionSystem::intersectionDepth(const Collision* eColl, const Collision* oColl) {
	float distX = eColl->hitPos.x - oColl->hitPos.x;
	float minDistX = (eColl->hitWidth + oColl->hitWidth) / 2;
	float depthX = distX > 0 ? minDistX - distX : -minDistX - distX;

	float distY = eColl->hitPos.y - oColl->hitPos.y;
	float minDistY = (eColl->hitHeight + oColl->hitHeight) / 2;
	float depthY = distY > 0 ? minDistY - distY : -minDistY - distY;

	return { depthX, depthY }; // Return how much overlap exists on both axes
}

void CollisionSystem::resolveCollision(Collision* coll1, Transform* trans1, Collision* coll2, Transform* trans2) {
	Vector2 depth = intersectionDepth(coll1, coll2);

	if (abs(depth.x) < abs(depth.y)) {
		// Resolve X first if it's the smaller penetration
		trans1->pos.x += depth.x;
	}
	else {
		// Resolve Y first otherwise
		trans1->pos.y += depth.y;
	}
}

void CollisionSystem::evaluateCollision(Entity& entity, Collision* eColl, Transform* eTrans, Entity& other, Collision* oColl) {
	// Pushing entities that can be pushed
	if (hasPhysicsTag(eColl, "pushable") && hasPhysicsTag(oColl, "canPush")) {
		Transform* oTrans = Game::ecs.getComponent<Transform>(other);
		pushEntity(eColl, eTrans, oColl, oTrans);
	}

	// Portal teleportation
	if (hasPhysicsTag(eColl, "canTeleport") && hasPhysicsTag(oColl, "portal")) {
		TeleportLink* firstLink = Game::ecs.getComponent<TeleportLink>(other);
		TeleportLink* secondLink = Game::ecs.getComponent<TeleportLink>(Room::getPortalLink(other));
		
		if (secondLink == nullptr) return;

		Transform* outPortalTrans = Game::ecs.getComponent<Transform>(Room::getPortalLink(other));
		Collision* outPortalColl = Game::ecs.getComponent<Collision>(Room::getPortalLink(other));

		std::unordered_map<int, double> directionMap = {  // Defaults to first portal facing south
			{Facing::SOUTH, 180.0},
			{Facing::EAST, 90.0},
			{Facing::NORTH, 0.0},
			{Facing::WEST, 270.0}
		};

		if (secondLink != nullptr) {
			// Placing entity at new location
			float width = (outPortalColl->hitWidth + eColl->hitWidth) / 2 + 1;  // Add 1 to each direction to prevent immediate re-entry
			float height = (outPortalColl->hitHeight + eColl->hitHeight) / 2 + 1;

			if (secondLink->facing == Facing::SOUTH) {
				eTrans->pos = { outPortalTrans->pos.x, outPortalTrans->pos.y + height };
			}
			else if (secondLink->facing == Facing::EAST) {
				eTrans->pos = { outPortalTrans->pos.x + width, outPortalTrans->pos.y };
			}
			else if (secondLink->facing == Facing::NORTH) {
				eTrans->pos = { outPortalTrans->pos.x, outPortalTrans->pos.y - height };
			}
			else if (secondLink->facing == Facing::WEST) {
				eTrans->pos = { outPortalTrans->pos.x - width, outPortalTrans->pos.y };
			}

			// Rotating velocity
			if (firstLink->facing == Facing::EAST) {
				directionMap.clear();
				directionMap = {
					{Facing::SOUTH, 270.0},
					{Facing::EAST, 180.0},
					{Facing::NORTH, 90.0},
					{Facing::WEST, 0.0}
				};
			}
			else if (firstLink->facing == Facing::NORTH) {
				directionMap.clear();
				directionMap = {
					{Facing::SOUTH, 0.0},
					{Facing::EAST, 270.0},
					{Facing::NORTH, 180.0},
					{Facing::WEST, 90.0}
				};
			}
			else if (firstLink->facing == Facing::WEST) {
				directionMap.clear();
				directionMap = {
					{Facing::SOUTH, 90.0},
					{Facing::EAST, 0.0},
					{Facing::NORTH, 270.0},
					{Facing::WEST, 180.0}
				};
			}

			eTrans->vel.rotate(directionMap[secondLink->facing]);
		}
	}

	// Grappling hook collisions
	if (hasPhysicsTag(eColl, "grapple")) {
		Grapple* grapple = Game::ecs.getComponent<Grapple>(entity);
		Player* player = Game::ecs.getComponent<Player>(grapple->owner);

		if (hasPhysicsTag(oColl, "player") && player->grappleState == GrappleState::RETURNING) {
			Game::ecs.destroyEntity(entity);
			player->grappleRef = 0;  // Remove grapple reference from player
			player->moveToGrapple = false;

			player->grappleState = GrappleState::INACTIVE;
			return;
		}

		if (hasPhysicsTag(oColl, "wall") && player->grappleState == GrappleState::SENT) {
			player->grappleState = GrappleState::LATCHED;
			grapple->grappledTo = other;
			player->moveToGrapple = true;
		}
	}

	// Portal Spawning
	if (hasPhysicsTag(eColl, "portalBullet") && hasPhysicsTag(oColl, "canHoldPortal")) {
		int side = intersection(eColl, oColl);  // The direction the spawned portal will face
		std::cout << side << std::endl;
		Entity portal = Game::ecs.createEntity();

		Game::ecs.assignComponent<Sprite>(portal);
		Game::ecs.assignComponent<Transform>(portal);
		Game::ecs.assignComponent<Collision>(portal);
		Game::ecs.assignComponent<TeleportLink>(portal);

		Sprite* pSprite = Game::ecs.getComponent<Sprite>(portal);
		*pSprite = Sprite{
			.tileWidth = 64,
			.tileHeight = 64,
			.spriteSheet = TextureManager::loadTexture(Game::renderer, "Assets/orbeeto.png"),
		};

		// Need spawning bullet's position
		Transform* eTrans = Game::ecs.getComponent<Transform>(entity);

		Transform* pTrans = Game::ecs.getComponent<Transform>(portal);
		*pTrans = Transform{
			.pos = eTrans->pos,
		};

		Collision* pColl = Game::ecs.getComponent<Collision>(portal);
		*pColl = Collision{
			.hitWidth = 64,
			.hitHeight = 64,
			.hitPos = eTrans->pos,
			.physicsTags = {"portal"}
		};

		TeleportLink* pTLink = Game::ecs.getComponent<TeleportLink>(portal);
		*pTLink = TeleportLink{ .facing = side };

		Bullet* pBullet = Game::ecs.getComponent<Bullet>(entity);
		Player* player = Game::ecs.getComponent<Player>(pBullet->shotBy);

		// Updating active player portals. If two are alredy active the oldest one will be replaced by the new one
		if (player->portals.first == 0) {  // No portals fired yet
			player->portals.first = portal;
		}
		else {
			TeleportLink* otherLink = Game::ecs.getComponent<TeleportLink>(player->portals.first);

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
				Game::ecs.destroyEntity(player->portals.first);

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

		// AN ENTITY WITH THE PORTALBULLET PHYSICS TAG MUST ALSO HAVE PROJECTILE TAG!
	}

	// Projectile deaths
	if (hasPhysicsTag(eColl, "projectile") && hasPhysicsTag(oColl, "wall")) {  // Destroys bullet if it hits wall
		Game::ecs.destroyEntity(entity);
		return;
	}
}

bool CollisionSystem::hasPhysicsTag(const Collision* coll, std::string tag) {
	const auto it = std::find(coll->physicsTags.begin(), coll->physicsTags.end(), tag);
	if (it != coll->physicsTags.end()) return true;
	else return false;
}