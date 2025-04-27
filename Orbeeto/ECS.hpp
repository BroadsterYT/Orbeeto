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
#include "Components/Player.hpp"
#include "Components/PlayerGun.hpp"
#include "Components/Sprite.hpp"
#include "Components/StatBar.hpp"
#include "Components/TeleportLink.hpp"
#include "Components/Transform.hpp"


class ECS {
public:
	std::vector<EntityDesc> entities;  // All entities currently in existence
	std::vector<Entity> freeEntities;  // All entity values that are unused

	ECS() {
		// ----- Registering Components ----- //
		std::cout << "Bullet component registered. ID: " << getComponentId<Bullet>() << std::endl;
		std::cout << "Collision component registered. ID: " << getComponentId<Collision>() << std::endl;
		std::cout << "Defense component registered. ID: " << getComponentId<Defense>() << std::endl;
		std::cout << "Grapple component registered. ID: " << getComponentId<Grapple>() << std::endl;
		std::cout << "Hp component registered. ID: " << getComponentId<Hp>() << std::endl;
		std::cout << "MovementAI component registered. ID: " << getComponentId<MovementAI>() << std::endl;
		std::cout << "Player component registered. ID: " << getComponentId<Player>() << std::endl;
		std::cout << "PlayerGun component registered. ID: " << getComponentId<PlayerGun>() << std::endl;
		std::cout << "Sprite component registered. ID: " << getComponentId<Sprite>() << std::endl;
		std::cout << "StatBar component registered. ID: " << getComponentId<StatBar>() << std::endl;
		std::cout << "TeleportLink component registered. ID: " << getComponentId<TeleportLink>() << std::endl;
		std::cout << "Transform component registered. ID: " << getComponentId<Transform>() << std::endl;

		for (Entity i = 1; i < MAX_ENTITIES; i++) {
			freeEntities.push_back(i);
		}
	}

	template <class T>
	int getComponentId() {
		static int componentId = componentCounter++;
		return componentId;
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

		std::vector<Component*> tempComponents;
		tempComponents.assign(MAX_COMPONENTS, nullptr);
		//entities.push_back({ temp, ComponentMask(), tempComponents });
		state->addEntityDesc({ temp, ComponentMask(), tempComponents });

		return temp;
	}

	/// <summary>
	/// Destroys an entity from a given game state
	/// </summary>
	/// <param name="state">Pointer to the game state to search</param>
	/// <param name="entity">The entity to delete</param>
	void destroyEntity(StateBase* state, Entity& entity) {
		auto& entityDescs = state->getEntityDescs();

		for (auto it = entityDescs.begin(); it != entityDescs.end(); ++it) {
			if (it->entity == entity) {
				// Free sprite texture if it exists
				if (it->mask.test(getComponentId<Sprite>())) {
					Sprite* sprite = getComponent<Sprite>(state, entity);
					SDL_DestroyTexture(sprite->spriteSheet);
					sprite->spriteSheet = nullptr;
				}

				for (auto& comp : it->components) {
					delete comp;
					comp = nullptr;
				}

				entityDescs.erase(it);

				freeEntities.push_back(entity);
				return;
			}
		}
	}

	template<typename T>
	void assignComponent(StateBase* state, Entity& entity) {
		for (EntityDesc& edesc : state->getEntityDescs()) {
			if (edesc.entity == entity) {
				assert(!edesc.mask.test(getComponentId<T>()) && "Component already added to entity.");
				
				edesc.mask.set(getComponentId<T>());
				edesc.components[getComponentId<T>()] = new T();

				// std::cout << "Component for entity " << entity << " set successfully." << std::endl;
				return;
			}
		}

		std::cout << "Component could not be added to entity " << entity << " because the entity could not be found" << std::endl;
	}

	template<typename T>
	void removeComponent(StateBase* state, Entity& entity) {
		for (EntityDesc& edesc : state->getEntityDescs()) {
			if (edesc.entity == entity) {
				assert(edesc.mask.test(getComponentId<T>()) && "Trying to remove non-existent component");

				edesc.mask.reset(getComponentId<T>());
				delete edesc.components[getComponentId<T>()];
				edesc.components[getComponentId<T>()] = nullptr;

				// std::cout << "Removal of component from entity " << entity << " was successful." << std::endl;
				return;
			}
		}

		// std::cout << "Component for entity " << entity << " could not be removed because entity could not be found or does not exist." << std::endl;
	}

	template<typename T>
	T* getComponent(StateBase* state, Entity entity) {
		for (EntityDesc& edesc : state->getEntityDescs()) {
			if (edesc.entity == entity) {
				return static_cast<T*>(edesc.components[getComponentId<T>()]);
			}
		}

		return nullptr;
	}

	template<typename... ComponentTypes>
	std::vector<Entity> getSystemGroup(StateBase* state) {
		std::vector<Entity> output;
		ComponentMask maskRef;

		assert(sizeof...(ComponentTypes) > 0 && "A group must be bound by at least 1 component.");

		int componentIds[] = { getComponentId<ComponentTypes>() ... };
		for (int& id : componentIds) {
			maskRef.set(id);
		}

		// Finding entities that belong in system group
		for (EntityDesc& edesc : state->getEntityDescs()) {
			if ((maskRef & edesc.mask) != maskRef) continue;
			output.push_back(edesc.entity);
		}

		return output;
	}

private:
	int componentCounter = 0;
};