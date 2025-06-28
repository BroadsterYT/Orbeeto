#include "ParticleEmitterSystem.hpp"


ParticleEmitterSystem::ParticleEmitterSystem() {}

void ParticleEmitterSystem::update() {
	for (auto entity : Game::ecs.getSystemGroup<ParticleEmitter, Transform>(Game::stack.peek())) {
		ParticleEmitter* pe = Game::ecs.getComponent<ParticleEmitter>(Game::stack.peek(), entity);
		Transform* trans = Game::ecs.getComponent<Transform>(Game::stack.peek(), entity);

		if (pe->buildupTime >= pe->nextFreq) {
			std::cout << pe->nextFreq << std::endl;

			pe->buildupTime = 0.0f;
			std::uniform_real_distribution<float> dist(pe->minFreq, pe->maxFreq);
			pe->nextFreq = dist(TimeManip::prng);
		}
		pe->buildupTime += TimeManip::deltaTime;
	}
}