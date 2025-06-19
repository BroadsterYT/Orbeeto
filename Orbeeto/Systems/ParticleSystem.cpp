#include "ParticleSystem.hpp"


ParticleSystem::ParticleSystem() {}

void ParticleSystem::update() {
	for (auto entity : Game::ecs.getSystemGroup<Particle, Sprite, Transform>(Game::stack.peek())) {
		Particle* part = Game::ecs.getComponent<Particle>(Game::stack.peek(), entity);
		Sprite* sprite = Game::ecs.getComponent<Sprite>(Game::stack.peek(), entity);
		Transform* trans = Game::ecs.getComponent<Transform>(Game::stack.peek(), entity);
	}
}