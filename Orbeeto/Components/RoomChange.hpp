#pragma once
#include "Component.hpp"
#include "../Vector2.hpp"


struct RoomChange : Component {
	Vector2 jumpTo = Vector2(0, 0);
	Vector2 playerSpawnPos = Vector2(0, 0);
};