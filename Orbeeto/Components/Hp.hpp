#pragma once
#include "Component.hpp"


struct Hp : Component {
	int maxHp = 50;  // The max HP the entity can have
	int hp = 50;  // The current HP of the entity

	int hpMod = 0;


	void serialize(std::ofstream& out) override {
		SerialHelper::serialize(out, &maxHp, &hp, &hpMod);
	}

	void deserialize(std::ifstream& in) override {
		SerialHelper::deserialize(in, &maxHp, &hp, &hpMod);
	}
};