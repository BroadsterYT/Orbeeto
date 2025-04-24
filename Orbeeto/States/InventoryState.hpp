#pragma once
#include "StateBase.hpp"


class InventoryState : public StateBase {
public:
	void onEnter() override;
	void onExit() override;
	void onSuspend() override;
	void onWakeup() override;
};