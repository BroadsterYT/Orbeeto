#pragma once
#include "SDL.h"
#include "Game.hpp"
#include "Vector2.hpp"
#include "InterpToggle.hpp"


class Camera {
public:
	Camera(int posX = 0, int posY = 0, int width = 0, int height = 0);

	int getX();
	int getY();
	
	int getWidth();
	void setWidth(int newWidth);
	int getHeight();
	void setHeight(int newHeight);

	void printDetails();

	void focus(int posX, int posY);
	void cinematicFocus(Entity entity, const Vector2& entityVel, double entityAccelConst);

private:
	SDL_Rect camera;

	InterpToggle<Vector2> tpToggle = InterpToggle<Vector2>(Math::cerp<Vector2>, Vector2(0, 0), Vector2(0, 0), 2);
	InterpToggle<int> tpToggleX = InterpToggle<int>(Math::cerp<int>, 0, 0, 2);
	InterpToggle<int> tpToggleY = InterpToggle<int>(Math::cerp<int>, 0, 0, 2);

	bool isTeleporting = false;
	bool lastTpCheck = true;
	float tpWeight = 0.0f;
};
