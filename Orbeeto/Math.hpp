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

	/// <summary>
	/// Takes an angle in degrees and returns the output in radians
	/// </summary>
	/// <typeparam name="T">Data type of input and output</typeparam>
	/// <param name="angle">The angle to convert from degrees to radians</param>
	/// <returns>The angle, in radians</returns>
	template<class T>
	static T rad(T angle) {
		return angle * (M_PI / 180.0);
	}

	/// <summary>
	/// Takes an angle in radians and returns the output in degrees
	/// </summary>
	/// <typeparam name="T">Data type of input and output</typeparam>
	/// <param name="angle">The angle to convert from radians to degrees</param>
	/// <returns>The angle, in degrees</returns>
	template<class T>
	static T deg(T angle) {
		return angle * (180.0 / M_PI);
	}
};