#include "Timer.hpp"
#include <cassert>


Timer::Timer(bool startOnInit) {
	started = false;
	paused = false;
	startTime = 0;
	endTime = 0;

	if (startOnInit) {
		start();
	}
}

uint64_t Timer::getTime() const {
	assert(started && "Error: Timer cannot return time because timer has not been started.");
	
	if (!paused) {
		return TimeManip::getTimeDiff(startTime);
	}
	else {
		return endTime - startTime;
	}
}

uint64_t Timer::start() {
	assert(!started && "Error: Timer has already been started");
	started = true;
	startTime = TimeManip::getTime();

	return TimeManip::getTime();
}

uint64_t Timer::pause() {
	assert(started && "Error: Timer cannot be paused because timer has not been started.");
	paused = true;

	uint64_t currentTime = TimeManip::getTime();
	endTime = currentTime;
	return currentTime;
}

uint64_t Timer::resume() {
	assert(started && "Error: Timer cannot resume because timer has not been started.");
	paused = false;

	return TimeManip::getTime();
}

uint64_t Timer::restart() {
	assert(started && "Error: Timer cannot be reset because timer was never started.");

	uint64_t currentTime = TimeManip::getTime();
	startTime = currentTime;
	return currentTime;
}