#pragma once
#include "Component.hpp"


enum class TrinketType {
	NONE,
	BUTTON,
};


struct Trinket : Component {
	TrinketType type = TrinketType::BUTTON;
	bool active = false;
};