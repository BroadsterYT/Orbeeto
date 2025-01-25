#pragma once
#include "System.hpp"


class PlayerSystem : public System {
public:
	PlayerSystem();

	void update();

private:
	void fireGrapple(const Entity& pEntity, Player* player, Transform* pTrans, Sprite* pSprite);
};