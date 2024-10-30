#pragma once
#include "Component.hpp"


struct Hp : Component {
	int maxHp;  // The max HP the entity can have
	int hp;  // The current HP of the entity

	int hpMod = 0;
};