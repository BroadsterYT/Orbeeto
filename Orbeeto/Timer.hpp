#pragma once
#include "TimeManip.hpp"


class Timer {
public:
	Timer(bool startOnInit = true);

	/// <summary>
	/// Returns the current running time of the timer
	/// </summary>
	/// <returns>The amount of time passed (end - start)</returns>
	uint64_t getTime() const;
	/// <summary>
	/// Starts the timer
	/// </summary>
	/// <returns>The real-world time when the timer was started</returns>
	uint64_t start();
	/// <summary>
	/// Pauses the timer. The time will stop running
	/// </summary>
	/// <returns>The real-world time when the timer was paused</returns>
	uint64_t pause();
	/// <summary>
	/// Causes the timer to continue after being paused
	/// </summary>
	/// <returns>The real-word time when the timer was resumed</returns>
	uint64_t resume();
	/// <summary>
	/// Restarts the timer by setting its time to 0.
	/// </summary>
	/// <returns>The real-world time when the timer was reset</returns>
	uint64_t restart();

private:
	bool started;
	bool paused;
	uint64_t startTime;
	uint64_t endTime;
};