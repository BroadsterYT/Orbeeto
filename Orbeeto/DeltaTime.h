#pragma once
#include <vector>


class DeltaTime {
public:
	static const int bufferSize;
	static std::vector<float> deltaBuffer;
	static int bufferIndex;

	static uint64_t previousTime;
	static uint64_t currentTime;

	static float deltaTime;
	static float avgDeltaTime;
};