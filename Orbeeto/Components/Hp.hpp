#pragma once
#include "Component.hpp"


struct Hp : Component {
	int maxHp = 50;  // The max HP the entity can have
	int hp = 50;  // The current HP of the entity

	int hpMod = 0;


	void serialize(std::ofstream& out) override {
		out.write(reinterpret_cast<const char*>(&maxHp), sizeof(maxHp));
		out.write(reinterpret_cast<const char*>(&hp), sizeof(hp));

		out.write(reinterpret_cast<const char*>(&hpMod), sizeof(hpMod));
	}

	void deserialize(std::ifstream& in) override {
		in.read(reinterpret_cast<char*>(&maxHp), sizeof(maxHp));
		in.read(reinterpret_cast<char*>(&hp), sizeof(hp));

		in.read(reinterpret_cast<char*>(&hpMod), sizeof(hpMod));
	}
};