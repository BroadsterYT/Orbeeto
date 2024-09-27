#pragma once
#include <iostream>

#include "Coordinator.hpp"

#include "HealthSystem.hpp"
#include "Health.hpp"


extern Coordinator oCoordinator;


void HealthSystem::init() {}

void HealthSystem::update() {
	for (const auto& entity : mEntities) {
		auto& HealthSystem = oCoordinator.getComponent<Health>(entity);
		   
		HealthSystem.health++;
		std::cout << HealthSystem.health << std::endl;
	}
}