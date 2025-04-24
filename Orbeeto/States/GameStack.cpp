#include "GameStack.hpp"
#include <stdexcept>
#include <cassert>

#include <iostream>
#include "../InputManager.hpp"

#include "ActionState.hpp"
#include "InventoryState.hpp"


GameStack::GameStack() {
	registerState(StateName::ACTION, new ActionState());
	registerState(StateName::INVENTORY, new InventoryState());
	push(StateName::ACTION);
}

void GameStack::registerState(StateName name, StateBase* gameState) {
	assert(!isRegistered(name) && "Error: State has already been registered.");
	nameToState.insert({ name, gameState });
	stateToName.insert({ gameState, name });
}

bool GameStack::isRegistered(StateName name) {
	try {
		StateBase* test = nameToState.at(name);
		return true;
	}
	catch (std::out_of_range) {
		return false;
	}
}

void GameStack::push(StateName name) {
	assert(isRegistered(name) && "Error: Could not push to stack because game state is not registered.");
	
	if (!stack.empty()) {
		StateBase* currentTop = stack.top();
		currentTop->onSuspend();
	}

	stack.push(nameToState[name]);
	nameToState[name]->onEnter();
}

StateName GameStack::pop() {
	assert(!stack.empty() && "Error: Could not pop from stack because stack is empty.");
	
	StateBase* popped = stack.top();
	stack.pop();
	popped->onExit();

	if (!stack.empty()) {
		StateBase* newTop = stack.top();
		newTop->onWakeup();
	}

	return stateToName[popped];
}

StateName GameStack::swap(StateName name) {
	assert(!stack.empty() && "Error: Could not swap because stack is empty.");

	StateBase* popped = stack.top();
	stack.pop();
	popped->onExit();

	stack.push(nameToState[name]);
	nameToState[name]->onEnter();

	return stateToName[popped];
}

StateBase* GameStack::peek() {
	assert(!stack.empty() && "Error: Could not return top of stack because stack is empty.");
	return stack.top();
}

void GameStack::update() {
	if (InputManager::keysPressed[SDLK_q]) {
		swap(StateName::INVENTORY);
	}
	if (InputManager::keysPressed[SDLK_z]) {
		swap(StateName::ACTION);
	}
}