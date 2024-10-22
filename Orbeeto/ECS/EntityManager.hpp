#pragma once
#include <array>
#include <queue>
#include <cassert>
#include "Types.hpp"


class EntityManager {
private:
	std::queue<Entity> mAvailableEntities{};
	std::array<Signature, MAX_ENTITIES> mSignatures{};
	uint32_t mLivingEntityCount{};

public:
	EntityManager() {
		for (Entity entity = 0; entity < MAX_ENTITIES; entity++) {
			mAvailableEntities.push(entity);
		}
	}
	
	Entity createEntity() {
		assert(mLivingEntityCount < MAX_ENTITIES && "Too many entities in existence.");

		Entity id = mAvailableEntities.front();
		mAvailableEntities.pop();
		++mLivingEntityCount;

		return id;
	}

	void destroyEntity(Entity entity) {
		assert(entity < MAX_ENTITIES && "Entity out of range.");

		// Invalidate the destroyed entity's signature
		mSignatures[entity].reset();

		// Put the destroyed ID at the back of the queue
		mAvailableEntities.push(entity);
		--mLivingEntityCount;
	}

	void setSignature(Entity entity, Signature signature) {
		assert(entity < MAX_ENTITIES && "Entity out of range.");

		// Put this entity's signature into the array of signatures
		mSignatures[entity] = signature;
	}

	Signature getSignature(Entity entity) {
		assert(entity < MAX_ENTITIES && "Entity out of range.");

		return mSignatures[entity];
	}
};