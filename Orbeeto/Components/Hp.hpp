#pragma once
#include "Component.hpp"


struct Hp : Component {
	int maxHp = 50;  // The max HP the entity can have
	int hp = 50;  // The current HP of the entity

	int hpMod = 0;
};