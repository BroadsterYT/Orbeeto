#pragma once
#include <cassert>
#include <vector>
#include <bitset>
#include <iostream>
#include <algorithm>

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
#include "Components/TeleportLink.hpp"
#include "Components/Transform.hpp"


using Entity = uint32_t;

const uint32_t MAX_ENTITIES = 2000;
const uint32_t MAX_COMPONENTS = 32;
using ComponentMask = std::bitset<MAX_COMPONENTS>;


struct EntityDesc {
	Entity entity;
	ComponentMask mask;
	std::vector<Component*> components;
};


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

	Entity createEntity() {
		assert(freeEntities.size() > 0 && "An entity overflow has occurred.");
		Entity temp = freeEntities[0];
		freeEntities.erase(freeEntities.begin());

		std::vector<Component*> tempComponents;
		tempComponents.assign(MAX_COMPONENTS, nullptr);
		entities.push_back({ temp, ComponentMask(), tempComponents });

		return temp;
	}

	void destroyEntity(Entity& entity) {
		int count = 0;
		for (EntityDesc& edesc : entities) {
			if (edesc.entity == entity) {
				// Freeing memory taken up by spritesheet if the entity has a sprite
				if (edesc.mask.test(getComponentId<Sprite>())) {
					std::cout << "Sprite sheet for entity " << entity << " is being destroyed.\n";
					Sprite* sprite = getComponent<Sprite>(entity);
					SDL_DestroyTexture(sprite->spriteSheet);
					sprite->spriteSheet = nullptr;
				}

				for (auto& comp : edesc.components) {
					delete comp;
					comp = nullptr;  // Only need to free component memory because of manual memory allocation
				}
				
				entities.erase(entities.begin() + count);
				// std::cout << "Entity " << entity << " was successfully destroyed." << std::endl;
				freeEntities.push_back(entity);
				return;
			}
			count++;
		}

		// std::cout << "Entity " << entity << " could not be destroyed because it was not found or does not exist." << std::endl;
	}

	template<typename T>
	void assignComponent(Entity& entity) {
		for (EntityDesc& edesc : entities) {
			if (edesc.entity == entity) {
				assert(!edesc.mask.test(getComponentId<T>()) && "Component already added to entity.");
				
				edesc.mask.set(getComponentId<T>());
				edesc.components[getComponentId<T>()] = new T;

				// std::cout << "Component for entity " << entity << " set successfully." << std::endl;
				return;
			}
		}

		std::cout << "Component could not be added to entity " << entity << " because the entity could not be found" << std::endl;
	}

	template<typename T>
	void removeComponent(Entity& entity) {
		for (EntityDesc& edesc : entities) {
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
	T* getComponent(Entity entity) {
		for (EntityDesc& edesc : entities) {
			if (edesc.entity == entity) {
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
			output.push_back(edesc.entity);
		}

		return output;
	}

private:
	int componentCounter = 0;
};