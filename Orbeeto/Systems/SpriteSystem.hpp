#pragma once
#include "System.hpp"
#include <vector>
#include "../WindowManager.hpp"


class SpriteSystem : public System {
public:
	SpriteSystem(SDL_Renderer* renderer);
	void render(SDL_Renderer* renderer);

private:
	SDL_Texture* renderBuffer;

	/// <summary>
	/// Finds the lower/upper bound of the screen in which a sprite can render
	/// </summary>
	/// <param name="width">Will find bound for width if true, will otherwise find height bound</param>
	/// <param name="lower">Will find the lower bound if true, will otherwise find the upper bound</param>
	/// <param name="lower">The zoom-in scale of the screen</param>
	/// <returns>The sprite bound for the specified dimension/direction</returns>
	int spriteClip(bool width, bool lower, float scale);
};