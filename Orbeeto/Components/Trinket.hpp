#pragma once
#include "Component.hpp"


enum class TrinketType {
	BUTTON,
};


struct Trinket : Component {
	TrinketType type = TrinketType::BUTTON;
	bool active = false;
};