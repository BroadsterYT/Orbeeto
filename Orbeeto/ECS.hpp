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
#include "Components/EntityAI.hpp"
#include "Components/Grapple.hpp"
#include "Components/Hp.hpp"
#include "Components/Particle.hpp"
#include "Components/ParticleEmitter.hpp"
#include "Components/Player.hpp"
#include "Components/PlayerGun.hpp"
#include "Components/RoomChange.hpp"
#include "Components/Sprite.hpp"
#include "Components/StatBar.hpp"
#include "Components/TeleportLink.hpp"
#include "Components/Transform.hpp"
#include "Components/TextRender.hpp"
#include "Components/Trinket.hpp"


class ECS {
public:
	ECS() {
		std::cout << "Bullet component registered. ID: " << getComponentId<Bullet>() << std::endl;
		
		std::cout << "Collision component registered. ID: " << getComponentId<Collision>() << std::endl;
		std::cout << "CanPush_PTag component registered. ID: " << getComponentId<CanPush_PTag>() << std::endl;
		std::cout << "Pushable_PTag component registered. ID: " << getComponentId<Pushable_PTag>() << std::endl;
		std::cout << "Wall_PTag component registered. ID: " << getComponentId<Wall_PTag>() << std::endl;
		std::cout << "PortalBullet_PTag component registered. ID: " << getComponentId<PortalBullet_PTag>() << std::endl;
		std::cout << "CanHoldPortal_PTag component registered. ID: " << getComponentId<CanHoldPortal_PTag>() << std::endl;
		std::cout << "CanTeleport_PTag component registered. ID: " << getComponentId<CanTeleport_PTag>() << std::endl;
		std::cout << "Projectile_PTag component registered. ID: " << getComponentId<Projectile_PTag>() << std::endl;
		std::cout << "Hurtable_PTag component registered. ID: " << getComponentId<Hurtable_PTag>() << std::endl;
		std::cout << "Enemy_PTag component registered. ID: " << getComponentId<Enemy_PTag>() << std::endl;
		
		std::cout << "Defense component registered. ID: " << getComponentId<Defense>() << std::endl;
		std::cout << "Grapple component registered. ID: " << getComponentId<Grapple>() << std::endl;
		std::cout << "Hp component registered. ID: " << getComponentId<Hp>() << std::endl;
		
		std::cout << "EntityAI component registered. ID: " << getComponentId<EntityAI>() << std::endl;
		std::cout << "FollowEntityAI component registered. ID: " << getComponentId<FollowEntityAI>() << std::endl;
		std::cout << "TextTrembleAI component registered. ID: " << getComponentId<TextTrembleAI>() << std::endl;
		std::cout << "TextWaveAI component registered. ID: " << getComponentId<TextWaveAI>() << std::endl;
		std::cout << "TractorBeamAI component registered. ID: " << getComponentId<TractorBeamAI>() << std::endl;
		std::cout << "TwoPointShiftAI component registered. ID: " << getComponentId<TwoPointShiftAI>() << std::endl;
		
		std::cout << "Particle component registered. ID: " << getComponentId<Particle>() << std::endl;
		std::cout << "ParticleEmitter component registered. ID: " << getComponentId<ParticleEmitter>() << std::endl;
		std::cout << "Player component registered. ID: " << getComponentId<Player>() << std::endl;
		std::cout << "PlayerGun component registered. ID: " << getComponentId<PlayerGun>() << std::endl;
		std::cout << "RoomChange component registered. ID: " << getComponentId<RoomChange>() << std::endl;
		std::cout << "Sprite component registered. ID: " << getComponentId<Sprite>() << std::endl;
		std::cout << "StatBar component registered. ID: " << getComponentId<StatBar>() << std::endl;
		std::cout << "TeleportLink component registered. ID: " << getComponentId<TeleportLink>() << std::endl;
		std::cout << "Transform component registered. ID: " << getComponentId<Transform>() << std::endl;
		std::cout << "TextRender component registered. ID: " << getComponentId<TextRender>() << std::endl;
		
		std::cout << "Trinket component registered. ID: " << getComponentId<Trinket>() << std::endl;
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
		Entity temp = state->getNextFree();

		std::vector<Component*> tempComponents;
		tempComponents.assign(MAX_COMPONENTS, nullptr);
		state->addEntityDesc({ temp, ComponentMask(), tempComponents });

		return temp;
	}

	/// <summary>
	/// Destroys an entity from a given game state
	/// </summary>
	/// <param name="state">Pointer to the game state to search</param>
	/// <param name="entity">The entity to delete</param>
	void destroyEntity(StateBase* state, Entity& entity) {
		if (!state->getEntityDescs().contains(entity)) return;
		auto& edesc = state->getEntityDescs().at(entity);

		if (edesc.mask.test(getComponentId<Sprite>())) {
			TextureManager::cleanupTextures();  // TODO: Find solution that isn't O(n)
		}

		for (auto& comp : edesc.components) {
			delete comp;
			comp = nullptr;
		}

		state->getEntityDescs().erase(entity);
		state->returnFreeEntity(entity);
	}

	template<typename T>
	T* assignComponent(StateBase* state, Entity& entity) {
		auto& edesc = state->getEntityDescs().at(entity);
		assert(!edesc.mask.test(getComponentId<T>()) && "Component already added to entity.");

		edesc.mask.set(getComponentId<T>());
		edesc.components[getComponentId<T>()] = new T();
		return static_cast<T*>(edesc.components[getComponentId<T>()]);
		// std::cout << "Component for entity " << entity << " set successfully." << std::endl;
	}

	template<typename T>
	void removeComponent(StateBase* state, Entity& entity) {
		auto& edesc = state->getEntityDescs().at(entity);
		assert(edesc.mask.test(getComponentId<T>()) && "Trying to remove non-existent component");

		edesc.mask.reset(getComponentId<T>());
		delete edesc.components[getComponentId<T>()];
		edesc.components[getComponentId<T>()] = nullptr;
		// std::cout << "Removal of component from entity " << entity << " was successful." << std::endl;
	}

	template<typename T>
	T* getComponent(StateBase* state, Entity entity) {
		if (!state->getEntityDescs().contains(entity)) return nullptr;
		auto& edesc = state->getEntityDescs().at(entity);

		if (!edesc.components[getComponentId<T>()]) {
			return nullptr;
		}
		return static_cast<T*>(edesc.components[getComponentId<T>()]);
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
		for (auto& [entity, edesc] : state->getEntityDescs()) {
			if ((maskRef & edesc.mask) != maskRef) continue;
			output.push_back(edesc.entity);
		}

		return output;
	}

	// ---------- Serialization and Deserialization Batching ---------- //

	void serializeState(StateBase* state, std::string filePath) {
		std::ofstream out(filePath, std::ios::binary);
		ComponentMask inclusionMask;
		ComponentMask emptyMask;

		//inclusionMask.set(getComponentId<Trinket>());
		inclusionMask.set(getComponentId<Enemy_PTag>());
		
		for (auto& [entity, edesc] : state->getEntityDescs()) {
			if ((edesc.mask & inclusionMask) == emptyMask) continue;

			out << entity;
			for (uint32_t i = 0; i < edesc.components.size(); ++i) {
				if (!edesc.components[i]) continue;
				out << i;
				edesc.components[i]->serialize(out);
			}
			out << std::endl;
		}
		out.close();
	}

	void deserializeState(StateBase* state, std::string filePath) {
		std::ifstream in(filePath, std::ios::binary);
		std::unordered_map<Entity, Entity> entityRefMap;  // Key is serialized entity ID, value is new entity ID

		while (true) {
			int eofCheck = in.peek();
			if (eofCheck == EOF) {
				break;
			}

			Entity oldEntity;
			SerialHelper::deserialize(in, &oldEntity);
			Entity newEntity = state->getNextFree();
			entityRefMap.insert({ oldEntity, newEntity });

			bool relevantDataSerialized = false;  // If the entity was serialized without any important components, it can be deleted
			while (true) {
				int eolCheck = in.peek();
				if (eolCheck == '\n') {
					char absorb;
					in.get(absorb);
					break;
				}

				uint32_t newComp;
				SerialHelper::deserialize(in, &newComp);
				deserializeComponent(state, in, newEntity, newComp, relevantDataSerialized);
				
				if (!relevantDataSerialized) {
					destroyEntity(state, newEntity);
					entityRefMap.erase(oldEntity);
				}
			}
		}
		in.close();
	}

private:
	int componentCounter = 0;

	/// <summary>
	/// Creates a new component for an entity and assigns it deserialized values
	/// </summary>
	/// <param name="state">The game state to perform this operation in</param>
	/// <param name="in">The input file stream to deserialize component data from</param>
	/// <param name="entity">The entity receiving the deserialized component</param>
	/// <param name="compId">The ID of the component being assigned to the entity</param>
	/// <param name="relevant">Reference to relevance bool, used to determine if the entity contains any critical serialized components</param>
	void deserializeComponent(StateBase* state, std::ifstream& in, Entity& entity, uint32_t compId, bool& relevant) {
		if (compId == getComponentId<Transform>()) {
			assignComponent<Transform>(state, entity);
			Transform* trans = getComponent<Transform>(state, entity);
			trans->deserialize(in);
		}
	}
};