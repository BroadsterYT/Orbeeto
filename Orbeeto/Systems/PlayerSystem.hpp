#pragma once
#include "System.hpp"


class PlayerSystem : public System {
public:
	PlayerSystem();

	void update();

private:
	/// <summary>
	/// Fires a grappling hook entity
	/// </summary>
	/// <param name="pEntity"></param>
	/// <param name="player"></param>
	/// <param name="pTrans"></param>
	/// <param name="pSprite"></param>
	void fireGrapple(const Entity& pEntity, Player* player, Transform* pTrans, Sprite* pSprite);
	void firePortal(Entity* pEntity, Player* player, Transform* pTrans, Sprite* pSprite);
};