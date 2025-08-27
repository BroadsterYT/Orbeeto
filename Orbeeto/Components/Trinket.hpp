#pragma once
#include "Component.hpp"


enum class TrinketType {
	button,
};


struct Trinket : Component {
	TrinketType type = TrinketType::button;
	bool active = false;


	void serialize(std::ofstream& out) override {
		uint32_t rawType = static_cast<uint32_t>(type);
		SerialHelper::serialize(out, &rawType);

		SerialHelper::serialize(out, &active);
	}

	void deserialize(std::ifstream& in) override {
		uint32_t rawType;
		SerialHelper::deserialize(in, &rawType);
		type = static_cast<TrinketType>(rawType);

		SerialHelper::deserialize(in, &active);
	}
};