#pragma once
#include <vector>


class TimeManip {
public:
	static const int bufferSize;
	static int bufferIndex;
	static std::vector<float> deltaBuffer;

	static uint64_t previousTime;
	static uint64_t currentTime;

	static float deltaTime;
	static float avgDeltaTime;

	static void calculateDeltaTime();
	static float getDeltaAdjuster();
	/// <summary>
	/// Returns the time (in milliseconds) since January 1st, 1970
	/// </summary>
	/// <returns>The time (in milliseconds) since January 1st, 1970</returns>
	static uint64_t getTime();
	/// <summary>
	/// Returns the difference between the current time and the given time
	/// </summary>
	/// <param name="compTime">The time (in milliseconds) to compare to the current time</param>
	/// <returns>The difference between the current time and the given time</returns>
	static uint64_t getTimeDiff(uint64_t compTime);
};