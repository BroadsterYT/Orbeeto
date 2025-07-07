#pragma once
#include "../Entity.hpp"


class StateBase {
public:
	StateBase(bool allowUpdateBelow = false);

	/// <summary>
	/// Called when the state is added to the game stack
	/// </summary>
	virtual void onEnter() = 0;
	/// <summary>
	/// Called when the state is popped from the stack
	/// </summary>
	virtual void onExit() = 0;
	/// <summary>
	/// Called when another state is pushed above this one on the game stack
	/// </summary>
	virtual void onSuspend() = 0;
	/// <summary>
	/// Called when the state above this one is popped from the game stack
	/// </summary>
	virtual void onWakeup() = 0;

	/// <summary>
	/// Returns the vector cointaining the entity descriptions for all entities in this state
	/// </summary>
	std::vector<EntityDesc>& getEntityDescs();
	/// <summary>
	/// Adds an EntityDesc instance to the vector of all instances in the state
	/// </summary>
	/// <param name="edesc">The entity description to add</param>
	void addEntityDesc(EntityDesc edesc);

private:
	std::vector<EntityDesc> entityDescs;  // A vector of all the entities currently in the game state
	bool allowUpdateBelow = false;  // When true, will allow entities in the state immediately below to continue updating
};
