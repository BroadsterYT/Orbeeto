#include "ParticleEmitterSystem.hpp"


ParticleEmitterSystem::ParticleEmitterSystem() {}

void ParticleEmitterSystem::update() {
	for (auto entity : Game::ecs.getSystemGroup<ParticleEmitter, Transform>(Game::stack.peek())) {

	}
}