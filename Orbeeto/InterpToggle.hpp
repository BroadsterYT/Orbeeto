#pragma once
#include <functional>
#include "Math.hpp"
#include <iostream>


template<typename T>
class InterpToggle {
public:
	InterpToggle(std::function<T(T, T, double)> func, T val1, T val2, float cycleTime) : func(func), val1(val1), val2(val2), cycleTime(cycleTime) {
		weight = 0;
		lastWeight = 0;
		lastToggle = 0;
		active = false;
	}

	/// <summary>
	/// Sets the current state of the InterpToggle. If true, interpolates forward. False interpolates backward.
	/// </summary>
	/// <param name="state">The state to set to.</param>
	void setState(bool state) {
		active = state;
	}

	/// <summary>
	/// Toggles between forward/backward interpolation.
	/// </summary>
	void toggle() {
		if (active) {
			active = false;
		}
		else {
			active = true;
		}

		lastWeight = weight;
		lastToggle = TimeManip::getSDLTime();
	}

	T getValue() {
		if (active) {
			weight = lastWeight + (TimeManip::getSDLTime() - lastToggle) / cycleTime;
			weight = std::min(weight, 1.0);
		}
		else {
			weight = 1 - (TimeManip::getSDLTime() - lastToggle) / cycleTime - (1 - lastWeight);
			weight = std::max(weight, 0.0);
		}

		return func(val1, val2, weight);
	}

	double getWeight() {
		return weight;
	}

	void setWeight(double weight) {
		this->weight = weight;
	}

	float getCycleTime() {
		return cycleTime;
	}

	void setValue1(T newVal1) {
		val1 = newVal1;
	}

	void setValue2(T newVal2) {
		val2 = newVal2;
	}

private:
	std::function<T(T, T, double)> func;
	T val1;
	T val2;

	float cycleTime;
	double weight;  // Interpolation weight
	double lastWeight;

	double lastToggle;
	bool active;
};
