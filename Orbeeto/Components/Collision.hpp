#pragma once
#include "Component.hpp"
#include "../Vector2.hpp"
#include <cmath>
#include <iostream>
#include <SDL_stdinc.h>


struct Collision : Component {
	int hitWidth = 64;
	int hitHeight = 64;
	Vector2 hitPos = { 0, 0 };

	bool tpFlag = false;  // Lets other objects detect entity teleportation
	//std::bitset<32> physicsTags = std::bitset<32>().reset();


	void serialize(std::ofstream& out) override {
		SerialHelper::serialize(out, &hitWidth, &hitHeight, &hitPos.x, &hitPos.y, &tpFlag);
	}

	void deserialize(std::ifstream& in) override {
		SerialHelper::deserialize(in, &hitWidth, &hitHeight, &hitPos.x, &hitPos.y, &tpFlag);
	}
};


struct CanPush_PTag : public Component {};

struct Pushable_PTag : public Component {};

struct Wall_PTag : public Component {};

//struct Player_PTag : public Component {};

//struct Grapple_PTag : public Component {};

//struct Portal_PTag : public Component {};

struct PortalBullet_PTag : public Component {};

struct CanHoldPortal_PTag : public Component {};

struct CanTeleport_PTag : public Component {};

struct Projectile_PTag : public Component {
	bool player = true;
	bool enemy = false;


	void serialize(std::ofstream& out) override {
		SerialHelper::serialize(out, &player, &enemy);
	}

	void deserialize(std::ifstream& in) override {
		SerialHelper::deserialize(in, &player, &enemy);
	}
};

struct Hurtable_PTag : public Component {};

struct Enemy_PTag : public Component {};