#pragma once
#include "Component.hpp"
#include <stdint.h>


struct TeleportLink : public Component {
	uint32_t* linkedTo = nullptr;
};