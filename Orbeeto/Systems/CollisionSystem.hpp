#pragma once
#include "../ECS.hpp"
#include "../Components/Collision.hpp"
#include "../Components/Transform.hpp"


void CollisionSystem(ECS& ecs) {
	for (auto& entity : ecs.getSystemGroup<Collision, Transform>()) {

	}
}