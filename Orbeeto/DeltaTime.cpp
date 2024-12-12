#include "DeltaTime.h"


int const DeltaTime::bufferSize = 50;

std::vector<float> DeltaTime::deltaBuffer(bufferSize, 0.0f);

int DeltaTime::bufferIndex = 0;

uint64_t DeltaTime::previousTime = 0;

uint64_t DeltaTime::currentTime = 0;

float DeltaTime::deltaTime = 0.0f;

float DeltaTime::avgDeltaTime = 0.0f;