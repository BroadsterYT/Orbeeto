#pragma once
#include <bitset>
#include <vector>
#include <iostream>


extern int s_componentCounter;

template<class T>
int GetId() {  // This is for components!
	static int s_componentId = s_componentCounter++;
	return s_componentId;
}


const int MAX_ENTITIES = 4000;
const int MAX_COMPONENTS = 64;
typedef std::bitset<MAX_COMPONENTS> ComponentMask;

typedef unsigned long long EntityID;
typedef unsigned int EntityVersion;
typedef unsigned int EntityIndex;

inline EntityID CreateEntityId(EntityIndex index, EntityVersion version) {
	// Shift the index up 32 bits, and put the version in the bottom
	return ((EntityID)index << 32) | ((EntityID)version);
}

inline EntityIndex GetEntityIndex(EntityID id) {
	// Shift down 32 bits so we lose the version and get the index
	return id >> 32;
}

inline EntityVersion GetEntityVersion(EntityID id) {
	// Cast to a 32 bit int to get our version number (losing the top 32 bits)
	return (EntityVersion)id;
}

inline bool IsEntityValid(EntityID id) {
	return (id >> 32) != EntityIndex(-1);
}

#define INVALID_ENTITY CreateEntityId(EntityIndex(-1), 0)


struct ComponentPool {
	ComponentPool(size_t elementsize) {
		// Allocate enough memory to hold MAX_ENTITIES, each with elementsize
		elementSize = elementsize;
		pData = new char[elementSize * MAX_ENTITIES];
	}

	~ComponentPool() {
		delete[] pData;
	}

	inline void* get(size_t index) {
		// Looking up the component at the desired index
		return pData + index * elementSize;
	}

	char* pData{ nullptr };
	size_t elementSize{ 0 };
};


struct Scene {
	// All the info we need about each entity
	struct EntityDesc {
		EntityID id;
		ComponentMask mask;
	};
	std::vector<EntityDesc> entities;
	std::vector<EntityIndex> freeEntities;

	EntityID newEntity() {
		if (!freeEntities.empty()) {
			EntityIndex newIndex = freeEntities.back();
			freeEntities.pop_back();
			EntityID newID = CreateEntityId(newIndex, GetEntityVersion(entities[newIndex].id));
		}

		entities.push_back({ CreateEntityId(EntityIndex(entities.size()), 0), ComponentMask()});
		return entities.back().id;
	}

	/*template<typename T>
	void assign(EntityID id) {
		if (entities[GetEntityIndex(id)].id != id) {
			std::cout << "Error: Entity has already been deleted." << std::endl;
			return;
		}

		int componentId = GetId<T>();
		entities[GetEntityIndex(id)].mask.set(componentId);
	}*/

	template<typename T>
	void remove(EntityID id) {
		if (entities[GetEntityIndex(id)].id != id) {
			std::cout << "Error: Entity has already been deleted." << std::endl;
			return;
		}

		int componentId = GetId<T>();
		entities[GetEntityIndex(id)].mask.reset(componentId);
	}

	void destroyEntity(EntityID id) {
		EntityID newID = CreateEntityId(EntityIndex(-1), GetEntityVersion(id) + 1);
		entities[GetEntityIndex(id)].id = newID;
		entities[GetEntityIndex(id)].mask.reset();
		freeEntities.push_back(GetEntityIndex(id));
	}

	
	// ----- Component Pools ----- // 

	std::vector<ComponentPool*> componentPools;

	template <typename T>
	T* assign(EntityID id) {
		int componentId = GetId<T>();

		if (componentPools.size() <= componentId) {  // Not enough component pool
			componentPools.resize(componentId + 1, nullptr);
		}
		if (componentPools[componentId] == nullptr) {  // New component, make a new pool
			componentPools[componentId] = new ComponentPool(sizeof(T));
		}

		// Looks up the component in the pool, and initializes it with placement new
		T* pComponent = new (componentPools[componentId]->get(id)) T();

		// Set the bit for this component to true and return the created component
		entities[GetEntityIndex(id)].mask.set(componentId);
		return pComponent;
	}

	template<typename T>
	T* get(EntityID id) {
		if (entities[GetEntityIndex(id)].id != id) {
			std::cout << "Error: Entity has already been deleted." << std::endl;
			return nullptr;
		}

		int componentId = GetId<T>();
		if (!entities[GetEntityIndex(id)].mask.test(componentId)) {
			return nullptr;
		}

		T* pComponent = static_cast<T*>(componentPools[componentId]->get(id));
		return pComponent;
	}
};


template<typename...ComponentTypes>
struct SceneView {
	SceneView(Scene& scene) : pScene(&scene) {
		if (sizeof...(ComponentTypes) == 0) {
			all = true;
		}
		else {
			// Unpack the template parameters into an initializer list
			int componentIds[] = { 0, GetId<ComponentTypes>() ... };
			for (int i = 1; i < (sizeof...(ComponentTypes) + 1); i++) {
				componentMask.set(componentIds[i]);
			}
		}
	}

	struct Iterator {
		Iterator(Scene* pScene, EntityIndex index, ComponentMask mask, bool all) : pScene(pScene), index(index), mask(mask), all(all) {}

		EntityID operator*() const {
			return pScene->entities[index].id;
		}

		bool operator==(const Iterator& other) const {
			// Compare two iterators
			return index == other.index || index == pScene->entities.size();
		}

		bool operator!=(const Iterator& other) const {
			return index != other.index && index != pScene->entities.size();
		}

		bool validIndex() {
			// It's a valid entity ID and it has the correct component mask
			return IsEntityValid(pScene->entities[index].id) && (all || mask == (mask & pScene->entities[index].mask));
		}

		Iterator& operator++() {
			// Move the iterator forward
			do {
				index++;
			} while (index < pScene->entities.size() && !validIndex());

			return *this;
		}

		EntityIndex index;
		Scene* pScene;
		ComponentMask mask;
		bool all{ false };

	};

	const Iterator begin() const {
		// Give an iterator to the beginning of this view
		int firstIndex = 0;
		while (firstIndex < pScene->entities.size() &&
			(componentMask != (componentMask & pScene->entities[firstIndex].mask) || !IsEntityValid(pScene->entities[firstIndex].id))) {
			firstIndex++;
		}

		return Iterator(pScene, firstIndex, componentMask, all);
	}

	const Iterator end() const {
		// Give an iterator to the end of this view
		return Iterator(pScene, EntityIndex(pScene->entities.size()), componentMask, all);
	}

	Scene* pScene{ nullptr };
	ComponentMask componentMask;
	bool all{ false };
};