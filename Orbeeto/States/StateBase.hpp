#pragma once


enum class StateName {
	ACTION,
};

class StateBase {
public:
	StateBase(StateName name, bool allowUpdateBelow = false);

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
	/// Returns the "name" of the game state
	/// </summary>
	StateName getName();

private:
	StateName name;
	bool allowUpdateBelow = false;
};
