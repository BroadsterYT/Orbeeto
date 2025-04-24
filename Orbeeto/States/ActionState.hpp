#pragma once
#include "StateBase.hpp"


class ActionState : public StateBase {
public:
	void onEnter() override;
	void onExit() override;
	void onSuspend() override;
	void onWakeup() override;
};