#pragma once
#include "Component.hpp"
#include <stdint.h>


struct Bullet : Component {
	uint32_t birthTime;
	int damage;
};