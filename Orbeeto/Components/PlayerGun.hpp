#pragma once


struct PlayerGun {
	const Entity* owner;  // Pointer to player entity
	float cooldown;  // The base rate at which the gun fires bullets
	float heatDissipation;  // 
};