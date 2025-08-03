#pragma once
#include "Component.hpp"


struct Grapple : Component {
	uint32_t owner = 0;
	uint32_t grappledTo = 0;


	void serialize(std::ofstream& out) override {
		out.write(reinterpret_cast<const char*>(&owner), sizeof(owner));
		out.write(reinterpret_cast<const char*>(&grappledTo), sizeof(grappledTo));
	}

	void deserialize(std::ifstream& in) override {
		in.read(reinterpret_cast<char*>(&owner), sizeof(owner));
		in.read(reinterpret_cast<char*>(&grappledTo), sizeof(grappledTo));
	}
};