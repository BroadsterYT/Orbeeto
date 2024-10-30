#pragma once
#include "Component.hpp"


struct Defense : Component {
	int maxDef;  // The max defense the entity can have
	int def;  // The current defense of the entity

	int defMod = 0;
};