#pragma once
#include <cmath>
#include "SDL_stdinc.h"


class Math {
public:
	/// <summary>
	/// Linear interpolation. Interpolates between a and b given a weight
	/// </summary>
	/// <typeparam name="T">The data type for a and b</typeparam>
	/// <param name="a">Minimum value</param>
	/// <param name="b">Maximum value</param>
	/// <param name="weight">Interpolation weight between a and b</param>
	/// <returns>Linear interpolation between a and b</returns>
	template<class T>
	static T lerp(T a, T b, double weight) {
		double trueWeight = weight; // The actual weight the interpolation will use
		if (weight < 0) trueWeight = 0.0;
		if (weight > 1.0) trueWeight = 1.0;

		return (b - a) * trueWeight + a;
	}

	/// <summary>
	/// Cosinusoidal interpolation. Interpolates between a and b given a weight
	/// </summary>
	/// <typeparam name="T">The data type of a and b</typeparam>
	/// <param name="a">Minimum value</param>
	/// <param name="b">Maximum value</param>
	/// <param name="weight">Interpolation weight between a and b</param>
	/// <returns>Cosinusoidal interpolation between a and b</returns>
	template<class T>
	static T cerp(T a, T b, double weight) {
		double trueWeight = weight;
		if (weight < 0.0) trueWeight = 0.0;
		if (weight > 1.0) trueWeight = 1.0;

		return ((a - b) / 2) * cos(M_PI * trueWeight) + ((a + b) / 2);
	}
};