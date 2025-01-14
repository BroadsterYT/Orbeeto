#include "DeltaTime.hpp"
#include <SDL.h>
#include <numeric>


int const DeltaTime::bufferSize = 50;

std::vector<float> DeltaTime::deltaBuffer(bufferSize, 0.0f);

int DeltaTime::bufferIndex = 0;

uint64_t DeltaTime::previousTime = 0;

uint64_t DeltaTime::currentTime = 0;

float DeltaTime::deltaTime = 0.0f;

float DeltaTime::avgDeltaTime = 0.0f;

void DeltaTime::calculateDeltaTime() {
	// Delta Time
	DeltaTime::currentTime = SDL_GetPerformanceCounter();
	DeltaTime::deltaTime = (DeltaTime::currentTime - DeltaTime::previousTime) / (float)SDL_GetPerformanceFrequency();
	DeltaTime::previousTime = DeltaTime::currentTime;

	// Update Buffer
	DeltaTime::deltaBuffer[DeltaTime::bufferIndex] = DeltaTime::deltaTime;
	DeltaTime::bufferIndex = (DeltaTime::bufferIndex) % DeltaTime::deltaBuffer.size();

	DeltaTime::avgDeltaTime = std::accumulate(DeltaTime::deltaBuffer.begin(), DeltaTime::deltaBuffer.end(), 0.0f) / DeltaTime::bufferSize;
}

float DeltaTime::getDeltaAdjuster() {
	return avgDeltaTime * 10000.0f;
}