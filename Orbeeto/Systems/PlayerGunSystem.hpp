#pragma once
#include "System.hpp"
#include "../InputManager.hpp"


class PlayerGunSystem : public System {
public:
	PlayerGunSystem();

	void update();

private:
	void fireBullet(Transform* ownerTrans, const int bulletId, const double rotAngle, const bool isLeft);
};