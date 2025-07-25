#pragma once
#ifdef _DEBUG
#ifndef _DBG_NEW

#include <crtdbg.h>

inline void* __operator_new(size_t __n) {
	return ::operator new(__n, _NORMAL_BLOCK, __FILE__, __LINE__);
}
inline void* _cdecl operator new(size_t __n, const char* __fname, int __line) {
	return ::operator new(__n, _NORMAL_BLOCK, __fname, __line);
}
inline void _cdecl operator delete(void* __p, const char*, int) {
	::operator delete(__p);
}

#define _DBG_NEW new(__FILE__,__LINE__)
#define new _DBG_NEW


#endif // _DBG_NEW
#else

#define __operator_new(__n) operator new(__n)

#endif

#include <cassert>
#include <vector>
#include <bitset>
#include <iostream>
#include <algorithm>

#include "Entity.hpp"
#include "States/StateBase.hpp"
#include "Components/Bullet.hpp"
#include "Components/Collision.hpp"
#include "Components/Component.hpp"
#include "Components/Defense.hpp"
#include "Components/Grapple.hpp"
#include "Components/Hp.hpp"
#include "Components/MovementAI.hpp"
#include "Components/Particle.hpp"
#include "Components/ParticleEmitter.hpp"
#include "Components/Player.hpp"
#include "Components/PlayerGun.hpp"
#include "Components/Sprite.hpp"
#include "Components/StatBar.hpp"
#include "Components/TeleportLink.hpp"
#include "Components/Transform.hpp"
#include "Components/TextRender.hpp"
#include "Components/Trinket.hpp"


class ECS {
public:
	std::vector<Entity> freeEntities;  // All entity values that are unused

	ECS() {
		// ----- Registering Components ----- //
		std::cout << "Bullet component registered. ID: " << getComponentId<Bullet>() << std::endl;
		std::cout << "Collision component registered. ID: " << getComponentId<Collision>() << std::endl;
		std::cout << "Defense component registered. ID: " << getComponentId<Defense>() << std::endl;
		std::cout << "Grapple component registered. ID: " << getComponentId<Grapple>() << std::endl;
		std::cout << "Hp component registered. ID: " << getComponentId<Hp>() << std::endl;
		std::cout << "MovementAI component registered. ID: " << getComponentId<MovementAI>() << std::endl;
		std::cout << "Particle component registered. ID: " << getComponentId<Particle>() << std::endl;
		std::cout << "ParticleEmitter component registered. ID: " << getComponentId<ParticleEmitter>() << std::endl;
		std::cout << "Player component registered. ID: " << getComponentId<Player>() << std::endl;
		std::cout << "PlayerGun component registered. ID: " << getComponentId<PlayerGun>() << std::endl;
		std::cout << "Sprite component registered. ID: " << getComponentId<Sprite>() << std::endl;
		std::cout << "StatBar component registered. ID: " << getComponentId<StatBar>() << std::endl;
		std::cout << "TeleportLink component registered. ID: " << getComponentId<TeleportLink>() << std::endl;
		std::cout << "Transform component registered. ID: " << getComponentId<Transform>() << std::endl;
		std::cout << "TextRender component registered. ID: " << getComponentId<TextRender>() << std::endl;
		std::cout << "Trinket component registered. ID: " << getComponentId<Trinket>() << std::endl;

		for (Entity i = 1; i < MAX_ENTITIES; i++) {
			freeEntities.push_back(i);
		}
	}

	template <class T>
	int getComponentId() {
		static int componentId = componentCounter++;
		return componentId;
	}

	template<class T>
	ComponentPool<T>* getPool(StateBase* state) {
		if (!state->hasPool(getComponentId<T>())) {
			IComponentPool* newPool = new ComponentPool<T>();
			state->addPool(getComponentId<T>(), newPool);
		}
		IComponentPool* basePtr = state->getPool(getComponentId<T>());
		return static_cast<ComponentPool<T>*>(basePtr);
	}

	/// <summary>
	/// Creates a new entity in the given game state
	/// </summary>
	/// <param name="state">Pointer to the game state to create the entity within</param>
	/// <returns>The created entity</returns>
	Entity createEntity(StateBase* state) {
		assert(freeEntities.size() > 0 && "An entity overflow has occurred.");
		Entity temp = freeEntities[0];
		freeEntities.erase(freeEntities.begin());

		//std::vector<Component*> tempComponents;
		//tempComponents.assign(MAX_COMPONENTS, nullptr);
		//state->addEntityDesc({ temp, ComponentMask(), tempComponents });

		return temp;
	}

	/// <summary>
	/// Destroys an entity from a given game state
	/// </summary>
	/// <param name="state">Pointer to the game state to search</param>
	/// <param name="entity">The entity to delete</param>
	void destroyEntity(StateBase* state, Entity& entity) {
		for (auto& pool : state->getPools()) {
			if (pool.second->hasComponent(entity)) {
				pool.second->removeComponent(entity);
			}
		}
		freeEntities.push_back(entity);
	}

	template<typename T>
	void assignComponent(StateBase* state, Entity& entity) {
		if (!state->hasPool(getComponentId<T>())) {
			IComponentPool* newPool = new ComponentPool<T>();
			state->addPool(getComponentId<T>(), newPool);
		}

		getPool<T>(state)->addComponent(entity);
	}

	template<typename T>
	void removeComponent(StateBase* state, Entity& entity) {
		getPool<T>(state)->removeComponent(entity);
	}

	template<typename T>
	T* getComponent(StateBase* state, Entity entity) {
		return getPool<T>(state)->getComponent(entity);
	}

	template<typename First, typename... Rest>
	std::vector<Entity> getSystemGroup(StateBase* state) {
		std::vector<Entity> output;
		for (auto& entity : getPool<First>(state)->getPacked()) {
			if ((getPool<Rest>(state)->hasComponent(entity) && ...)) {
				output.push_back(entity);
			}
		}

		return output;
	}

private:
	int componentCounter = 0;
};