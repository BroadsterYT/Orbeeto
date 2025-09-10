#include "WindowManager.hpp"
#include <numeric>


int Window::WIDTH = 1280;

int Window::HEIGHT = 720;

std::pair<int, int> Window::getAspectRatio() {
	int gcd = std::gcd(WIDTH, HEIGHT);

	return std::make_pair(WIDTH / gcd, HEIGHT / gcd);
}