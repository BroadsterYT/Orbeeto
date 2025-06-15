#include "TimeManip.hpp"
#include <iostream>
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
	currentTime = SDL_GetPerformanceCounter();
	deltaTime = (currentTime - previousTime) / (float)SDL_GetPerformanceFrequency();
	previousTime = currentTime;

	// Update Buffer
	deltaBuffer[bufferIndex] = deltaTime;
	bufferIndex = (bufferIndex) % deltaBuffer.size();

	avgDeltaTime = std::accumulate(deltaBuffer.begin(), deltaBuffer.end(), 0.0f) / bufferSize;
	//std::cout << pow(avgDeltaTime, -1) << std::endl;
}

float TimeManip::getDeltaAdjuster() {
	return avgDeltaTime * 10000.0f;  // I have no clue why using 10000 works but it does for now
}

uint64_t TimeManip::getTime() {
	using namespace std::chrono;
	return duration_cast<milliseconds>(system_clock::now().time_since_epoch()).count();
	//return SDL_GetPerformanceCounter();
}

double TimeManip::getSDLTime() {
	return (double)SDL_GetPerformanceCounter() / (double)SDL_GetPerformanceFrequency();
}

uint64_t TimeManip::getTimeDiff(uint64_t compTime) {
	return getTime() - compTime;
}