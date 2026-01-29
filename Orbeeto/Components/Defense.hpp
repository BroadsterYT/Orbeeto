#pragma once
#include "Component.hpp"


struct Defense : Component {
	int maxDef = 10;  // The max defense the entity can have
	int def = 10;  // The current defense of the entity

	int defMod = 0;
};