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

const uint32_t MAX_ENTITIES = 2000;
const uint32_t MAX_COMPONENTS = 10;
using ComponentMask = std::bitset<MAX_COMPONENTS>;

struct EntityDesc {
	Entity entity;
	ComponentMask mask;
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
		std::cout << "Sprite component registered. ID: " << getComponentId<Sprite>() << std::endl;
		std::cout << "Sprite component registered. ID: " << getComponentId<Transform>() << std::endl;
		std::cout << "Player component registered. ID: " << getComponentId<Player>() << std::endl;

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
		Entity temp = freeEntities[0];
		freeEntities.erase(freeEntities.begin());

		// Preparing the vector of component pointers for the new entity
		std::vector<Component*> tempComponents;
		for (int i = 0; i < MAX_COMPONENTS; i++) {
			tempComponents.push_back(nullptr);
		}
		entities.push_back({ temp, ComponentMask(), tempComponents });

		std::cout << "Entity " << temp << " was successfully created." << std::endl;
		return temp;
	}

	void destroyEntity(Entity& entity) {
		int count = 0;
		for (EntityDesc& edesc : entities) {
			if (edesc.entity == entity) {
				for (Component* comp : edesc.components) {
					delete comp;
					comp = nullptr;
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
				assert(!edesc.mask.test(getComponentId<T>()) && "Component already added to entity");
				edesc.mask.set(getComponentId<T>());
				edesc.components[getComponentId<T>()] = new T;
				
				std::cout << "Component for entity " << entity << " set successfully." << std::endl;
				std::cout << "Entity bitmask: " << edesc.mask.to_string() << std::endl;
				return;
			}
		}

		std::cout << "Component could not be added to entity " << entity << " because the entity could not be found" << std::endl;
	}

	template<typename T>
	void removeComponent(Entity& entity) {
		for (EntityDesc& edesc : entities) {
			if (edesc.entity == entity) {
				delete edesc.components[getComponentId<T>()];
				edesc.components[getComponentId<T>()] = nullptr;
				std::cout << "Removal of component from entity " << entity << " was successful." << std::endl;
				return;
			}
		}

		std::cout << "Component for entity " << entity << " could not be removed because entity could not be found or does not exist." << std::endl;
	}

	template<typename T>
	T* getComponent(Entity& entity) {
		for (EntityDesc& edesc : entities) {
			if (entity == edesc.entity) {
				return static_cast<T*>(edesc.components[getComponentId<T>()]);
			}
		}
		return nullptr;
	}

	template<typename... ComponentTypes>
	std::vector<Entity> getSystemGroup() {
		std::vector<Entity> output;
		ComponentMask maskRef;

		assert(sizeof...(ComponentTypes) > 0 && "A group must be bound by at least 1 component.");

		int componentIds[] = { getComponentId<ComponentTypes>() ... };
		for (int& id : componentIds) {
			maskRef.set(id);
		}

		// Finding entities that belong in system group
		for (EntityDesc& edesc : entities) {
			if ((maskRef & edesc.mask) != maskRef) continue;
			//std::cout << "Entity " << edesc.entity << " belongs in this group" << std::endl;
			output.push_back(edesc.entity);
		}

		return output;
	}
};