#pragma once
#include <unordered_map>

#include "SDL.h"
#include "Vector2.hpp"


class InputManager {
public:
	/// <summary>
	/// Unordered map that keeps track of each key and whether or not
	/// it is pressed down
	/// </summary>
	static std::unordered_map<int, bool> keysPressed;

	/// <summary>
	/// Unordered map that keeps track of the number of times each
	/// key has been released
	/// </summary>
	static std::unordered_map<int, unsigned int> keysReleased;

	static int mousePosX;
	static int mousePosY;

	/// <summary>
	/// Updates the unordered map of key presses
	/// </summary>
	/// <param name="event">The SDL event being evaluated</param>
	static void handleKeyPresses(SDL_Event event);
	
	/// <summary>
	/// Updates the number of times each key has been released. 
	/// Will also update its value in the key press map to false.
	/// </summary>
	/// <param name="event">The SDL event being evaluated</param>
	static void handleKeyReleases(SDL_Event event);
	
	/// <summary>
	/// Prints each key/value pair in the keys pressed map
	/// </summary>
	static void printKeysPressed();

	/// <summary>
	/// Prints each key/value pair in the keys released map
	/// </summary>
	static void printKeysReleased();
};