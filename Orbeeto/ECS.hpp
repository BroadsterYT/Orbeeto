#pragma once
#include <cassert>
#include <vector>
#include <bitset>
#include <iostream>

#include "Components/Bullet.hpp"
#include "Components/Collision.hpp"
#include "Components/Component.hpp"
#include "Components/Defense.hpp"
#include "Components/Hp.hpp"
#include "Components/Player.hpp"
#include "Components/PlayerGun.hpp"
#include "Components/Sprite.hpp"
#include "Components/Transform.hpp"


using Entity = uint32_t;

const uint32_t MAX_ENTITIES = 1000;
const uint32_t MAX_COMPONENTS = 12;
using ComponentMask = std::bitset<MAX_COMPONENTS>;


struct EntityDesc {
	Entity entity;
	std::vector<int> sparse;  // The sparse vector that maps to the packed vector
	std::vector<int> packed; // The packed vector that maps to the component vector
	std::vector<Component*> components;
};


class ECS {
private:
	int componentCounter = 0;

public:
	std::vector<EntityDesc> entities;  // All entities currently in existence
	std::vector<Entity> freeEntities;  // All entity values that are unused

	ECS() {
		// ----- Registering Components ----- //
		std::cout << "Bullet component registered. ID: " << getComponentId<Bullet>() << std::endl;
		std::cout << "Collision component registered. ID: " << getComponentId<Collision>() << std::endl;
		std::cout << "Defense component registered. ID: " << getComponentId<Defense>() << std::endl;
		std::cout << "Hp component registered. ID: " << getComponentId<Hp>() << std::endl;
		std::cout << "Player component registered. ID: " << getComponentId<Player>() << std::endl;
		std::cout << "PlayerGun component registered. ID: " << getComponentId<PlayerGun>() << std::endl;
		std::cout << "Sprite component registered. ID: " << getComponentId<Sprite>() << std::endl;
		std::cout << "Transform component registered. ID: " << getComponentId<Transform>() << std::endl;

		for (Entity i = 0; i < MAX_ENTITIES; i++) {
			freeEntities.push_back(i);
		}
	}

	template <class T>
	int getComponentId() {
		static int componentId = componentCounter++;
		return componentId;
	}

	Entity createEntity() {
		assert(freeEntities.size() > 0 && "An entity overflow has occurred.");
		Entity temp = freeEntities[0];
		freeEntities.erase(freeEntities.begin());

		EntityDesc tempDesc;
		tempDesc.entity = temp;
		tempDesc.sparse.assign(MAX_COMPONENTS, -1);
		entities.push_back(tempDesc);

		return temp;
	}

	void destroyEntity(Entity& entity) {
		int count = 0;
		for (EntityDesc& edesc : entities) {
			if (edesc.entity == entity) {
				for (auto& comp : edesc.components) {
					delete comp;
					comp = nullptr;  // Only need to free component memory because of manual memory allocation
				}
				
				entities.erase(entities.begin() + count);
				std::cout << "Entity " << entity << " was successfully destroyed." << std::endl;
				freeEntities.push_back(entity);
				return;
			}
			count++;
		}

		std::cout << "Entity " << entity << " could not be destroyed because it was not found or does not exist." << std::endl;
	}

	template<typename T>
	void assignComponent(Entity& entity) {
		for (EntityDesc& edesc : entities) {
			if (edesc.entity == entity) {
				std::cout << edesc.sparse[getComponentId<T>()] << std::endl;
				assert(edesc.sparse[getComponentId<T>()] == -1 && "Component already added to entity.");
				
				edesc.sparse[getComponentId<T>()] = edesc.packed.size();
				edesc.packed.push_back(getComponentId<T>());
				
				edesc.components.push_back(nullptr);
				edesc.components[edesc.components.size() - 1] = new T;

				std::cout << "Component for entity " << entity << " set successfully." << std::endl;
				return;
			}
		}

		std::cout << "Component could not be added to entity " << entity << " because the entity could not be found" << std::endl;
	}

	template<typename T>
	void removeComponent(Entity& entity) {
		for (EntityDesc& edesc : entities) {
			if (edesc.entity == entity) {
				assert(edesc.sparse[getComponentId<T>()] != -1 && "Trying to remove non-existent component");

				int packedDelIndex = edesc.sparse[getComponentId<T>()]; // The index of the packed vector being deleted
				delete edesc.components[packedDelIndex];
				edesc.components.erase(edesc.components.begin() + packedDelIndex);
				edesc.sparse[getComponentId<T>()] = -1;

				// If last component was deleted, sparse vector does not need remapped
				if (packedDelIndex > edesc.components.size()) {
					std::cout << "Removal of component from entity " << entity << " was successful." << std::endl;
					return;
				}

				// Remapping packed vector to sparse
				for (int i = packedDelIndex; i < edesc.packed.size(); i++) {
					edesc.sparse[edesc.packed[i]] -= 1;
				}

				std::cout << "Removal of component from entity " << entity << " was successful." << std::endl;
				return;
			}
		}

		std::cout << "Component for entity " << entity << " could not be removed because entity could not be found or does not exist." << std::endl;
	}

	template<typename T>
	T* getComponent(Entity& entity) {
		for (EntityDesc& edesc : entities) {
			if (edesc.entity == entity) {
				return static_cast<T*>(edesc.components[edesc.sparse[getComponentId<T>()]]);
			}
		}

		return nullptr;
	}

	template<typename... ComponentTypes>
	std::vector<Entity> getSystemGroup() {
		////Uint32 timer = SDL_GetTicks();
		//std::vector<Entity> output;
		//ComponentMask maskRef;

		//assert(sizeof...(ComponentTypes) > 0 && "A group must be bound by at least 1 component.");

		//int componentIds[] = { getComponentId<ComponentTypes>() ... };
		//for (int& id : componentIds) {
		//	maskRef.set(id);
		//}

		//// Finding entities that belong in system group
		//for (EntityDesc& edesc : entities) {
		//	if ((maskRef & edesc.mask) != maskRef) continue;
		//	output.push_back(edesc.entity);
		//}

		////std::cout << "Time to complete: " << SDL_GetTicks() - timer << std::endl;
		//return output;
		std::vector<Entity> output;
		std::bitset<MAX_COMPONENTS> refMask;

		assert(sizeof...(ComponentTypes) > 0 && "A group must be bound by at least 1 component.");

		int refComponentIds[] = { getComponentId<ComponentTypes>() ... };
		for (int& id : refComponentIds) {
			refMask.set(id);
		}

		for (EntityDesc& edesc : entities) {
			std::bitset<MAX_COMPONENTS> entityMask;
			
			for (int i = 0; i < MAX_COMPONENTS; i++) {
				if (edesc.sparse[i] >= 0) {
					entityMask.set(i);
				}
				else {
					entityMask.reset(i);
				}
			}

			if ((refMask & entityMask) != refMask) continue;
			output.push_back(edesc.entity);
		}

		return output;
	}
};