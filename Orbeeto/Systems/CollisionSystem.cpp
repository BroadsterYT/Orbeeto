#include "CollisionSystem.hpp"
#include <algorithm>
#include "../Rooms/Room.hpp"


CollisionSystem::CollisionSystem() {}

void CollisionSystem::update() {
	for (Entity& entity : Game::ecs.getSystemGroup<Collision, Transform>()) {
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
	}
}

bool CollisionSystem::checkForCollision(const Collision* eColl, const Collision* oColl) {
	if (eColl->hitPos.x + eColl->hitWidth / 2 >= oColl->hitPos.x - oColl->hitWidth / 2
		&& eColl->hitPos.x - eColl->hitWidth / 2 <= oColl->hitPos.x + oColl->hitWidth / 2
		&& eColl->hitPos.y + eColl->hitHeight / 2 >= oColl->hitPos.y - oColl->hitHeight / 2
		&& eColl->hitPos.y - eColl->hitHeight / 2 <= oColl->hitPos.y + oColl->hitHeight / 2) {
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

void CollisionSystem::pushEntity(Collision* coll1, Transform* trans1, Collision* coll2, Transform* trans2) {
	int side = intersection(coll1, coll2);

	if (side == 0  // South
		&& (trans1->vel.y < 0 || trans2->vel.y > 0)
		&& trans1->pos.y - coll1->hitHeight / 2 <= trans2->pos.y + coll2->hitHeight / 2) {
		trans1->vel.y = 0;
		trans1->pos.y = trans2->pos.y + coll2->hitHeight / 2 + coll1->hitHeight / 2;
	}
	if (side == 1  // East
		&& (trans1->vel.x < 0 || trans2->vel.x > 0)
		&& trans1->pos.x - coll1->hitWidth / 2 <= trans2->pos.x + coll2->hitWidth / 2) {
		trans1->vel.x = 0;
		trans1->pos.x = trans2->pos.x + coll2->hitWidth / 2 + coll1->hitWidth / 2;
	}
	if (side == 2  // North
		&& (trans1->vel.y > 0 || trans2->vel.y < 0)
		&& trans1->pos.y + coll1->hitHeight / 2 >= trans2->pos.y - coll2->hitHeight / 2) {
		trans1->vel.y = 0;
		trans1->pos.y = trans2->pos.y - coll2->hitHeight / 2 - coll1->hitHeight / 2;
	}
	if (side == 3  // West
		&& (trans1->vel.x > 0 || trans2->vel.x < 0)
		&& trans1->pos.x + coll1->hitWidth / 2 >= trans2->pos.x - coll2->hitWidth / 2) {
		trans1->vel.x = 0;
		trans1->pos.x = trans2->pos.x - coll2->hitWidth / 2 - coll1->hitWidth / 2;
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
	}

	// Grappling hook collisions
	if (hasPhysicsTag(eColl, "grapple")) {
		Grapple* grapple = Game::ecs.getComponent<Grapple>(entity);
		Player* player = Game::ecs.getComponent<Player>(grapple->owner);

		if (hasPhysicsTag(oColl, "player") && player->grappleState == GrappleState::RETURNING) {
			Game::ecs.destroyEntity(entity);
			player->grappleState = GrappleState::INACTIVE;
			return;
		}

		if (hasPhysicsTag(oColl, "wall") && player->grappleState == GrappleState::SENT) {
			player->grappleState = GrappleState::LATCHED;
			grapple->grappledTo = &other;
		}
	}

	// Portal Spawning
	if (hasPhysicsTag(eColl, "portalBullet") && hasPhysicsTag(oColl, "canHoldPortal")) {
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
		*pTLink = TeleportLink{};

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