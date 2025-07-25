#pragma once
#include <cassert>
#include <iostream>
#include "Entity.hpp"



class IComponentPool {
public:
	virtual ~IComponentPool() = default;
	virtual void addComponent(Entity entity) = 0;
	virtual void removeComponent(Entity entity) = 0;
	virtual bool hasComponent(Entity entity) = 0;
};


template<class T>
class ComponentPool : public IComponentPool {
public:
	/// <summary>
	/// Adds the component of the component pool to an entity
	/// </summary>
	/// <param name="entity">The entity to give the component to</param>
	void addComponent(Entity entity) override {
		assert(!hasComponent(entity) && "Error: Component cannot be added because entity already has it");

		packed.push_back(entity);
		sparse[entity] = packed.size() - 1;
		components.push_back(new T());
	}

	/// <summary>
	/// Removes the component of the component pool from an entity
	/// </summary>
	/// <param name="entity">The entity to remove the component from</param>
	void removeComponent(Entity entity) override {
		assert(hasComponent(entity) && "Error: Cannot remove component because entity hasn't had it assigned");

		T* toDelete = components[sparse[entity]];

		// Swapping last entity/comp in packed/components with one to delete
		if (packed.size() != 0 && packed.back() != entity) {
			Entity temp = packed.back();
			packed[packed.size() - 1] = entity;  // Moving entity to delete to back
			packed[sparse[entity]] = temp;  // Moving entity originally in back to entity delete old position

			T* compTemp = components[packed.size() - 1];
			components[sparse[entity]] = compTemp;
			components[packed.size() - 1] = toDelete;

			sparse[temp] = sparse[entity];
		}

		delete components[components.size() - 1];
		components.pop_back();
		packed.pop_back();
		sparse[entity] = -1;
	}

	/// <summary>
	/// Check for whether or not an entity has the component of the component pool
	/// </summary>
	/// <param name="entity">The entity to check for component ownership</param>
	/// <returns>True if entity has the component, false otherwise</returns>
	bool hasComponent(Entity entity) override {
		if (sparse[entity] != -1 && packed[sparse[entity]] == entity) return true;
		else return false;
	}

	/// <summary>
	/// Returns the component belonging to the entity, returns nullptr if one wasn't assigned
	/// </summary>
	/// <param name="entity"></param>
	/// <returns>Pointer to entity's component, returns nullptr if it doesn't exist</returns>
	T* getComponent(Entity entity) {
		if (!hasComponent(entity)) {
			return nullptr;
		}
		return components[sparse[entity]];
	}

	std::vector<Entity> getPacked() {
		return packed;
	}

	void printPool() {
		std::cout << "Sparse: \n";
		for (int i = 0; i < sparse.size(); i++) {
			std::cout << i << ": " << sparse[i] << std::endl;
		}
		std::cout << std::endl;

		std::cout << "Packed: \n";
		for (int i = 0; i < packed.size(); i++) {
			std::cout << i << ": " << packed[i] << std::endl;
		}
		std::cout << std::endl;

		std::cout << "Components: \n";
		for (int i = 0; i < components.size(); i++) {
			std::cout << i;
			if (components[i] != nullptr) std::cout << ": Exists\n";
			else if (components[i] == nullptr) std::cout << ": nullptr\n";
			else std::cout << ": Unknown state\n";
		}
		std::cout << std::endl << std::endl;
	}

private:
	std::vector<int> sparse = std::vector<int>(MAX_ENTITIES, -1);
	std::vector<Entity> packed;
	std::vector<T*> components;
};