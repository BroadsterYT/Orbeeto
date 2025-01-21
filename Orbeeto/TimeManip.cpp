#include "TimeManip.hpp"
#include <chrono>
#include <SDL.h>
#include <numeric>


int const TimeManip::bufferSize = 50;
int TimeManip::bufferIndex = 0;
std::vector<float> TimeManip::deltaBuffer(bufferSize, 0.0f);

uint64_t TimeManip::previousTime = 0;
uint64_t TimeManip::currentTime = 0;

float TimeManip::deltaTime = 0.0f;
float TimeManip::avgDeltaTime = 0.0f;

void TimeManip::calculateDeltaTime() {
	// Delta Time
	TimeManip::currentTime = SDL_GetPerformanceCounter();
	TimeManip::deltaTime = (TimeManip::currentTime - TimeManip::previousTime) / (float)SDL_GetPerformanceFrequency();
	TimeManip::previousTime = TimeManip::currentTime;

	// Update Buffer
	TimeManip::deltaBuffer[TimeManip::bufferIndex] = TimeManip::deltaTime;
	TimeManip::bufferIndex = (TimeManip::bufferIndex) % TimeManip::deltaBuffer.size();

	TimeManip::avgDeltaTime = std::accumulate(TimeManip::deltaBuffer.begin(), TimeManip::deltaBuffer.end(), 0.0f) / TimeManip::bufferSize;
}

float TimeManip::getDeltaAdjuster() {
	return avgDeltaTime * 10000.0f;
}

uint64_t TimeManip::getTime() {
	using namespace std::chrono;
	return duration_cast<milliseconds>(system_clock::now().time_since_epoch()).count();
}

uint64_t TimeManip::getTimeDiff(uint64_t compTime) {
	return getTime() - compTime;
}