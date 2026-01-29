#pragma once
#include "Component.hpp"


enum class TrinketType {
	button,
};


struct Trinket : Component {
	TrinketType type = TrinketType::button;
	bool active = false;
};