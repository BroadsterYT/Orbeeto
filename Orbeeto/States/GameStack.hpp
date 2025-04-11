#pragma once
#include <stack>
#include <unordered_map>
#include "StateBase.hpp"


class GameStack {
public:
	void registerState(StateName name, StateBase* gameState);
	/// <summary>
	/// Adds a game state to the top of the stack
	/// </summary>
	/// <param name="state">The name of the state to push</param>
	void push(StateName name);
	/// <summary>
	/// Removes the state at the top of the stack and returns it
	/// </summary>
	/// <returns>The name of the popped state</returns>
	StateName pop();
	/// <summary>
	/// Swaps the state on top of the stack with the one provided
	/// </summary>
	/// <param name="state">The state to replace the state on top of the stack with</param>
	/// <returns>The name of the state that got replaced</returns>
	StateName swap(StateName name);

private:
	std::stack<StateBase*> stack;
	std::unordered_map<StateName, StateBase*> nameToState;  // Map with all states with the name as the key and the state instance as the value
	std::unordered_map<StateBase*, StateName> stateToName;  // Map with all states with the state instance as the key and the name as the value
	/// <summary>
	/// Determines if a state already exists within the map of all states
	/// </summary>
	/// <param name="name">The name of the state to check for</param>
	/// <returns>True if the state exists within the map, false otherwise</returns>
	bool isRegistered(StateName name);
};
