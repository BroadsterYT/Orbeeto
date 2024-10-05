#pragma once
#include "../ECS/System.hpp"
#include "../ECS/Coordinator.hpp"


class CollisionSystem : public System {
private:
	Coordinator* coordinator;

public:
	void init(Coordinator* coord);
	void update();
};
