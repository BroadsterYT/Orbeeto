#pragma once
#include <bitset>
#include <cstdint>


using Entity = std::uint32_t;
const Entity MAX_ENTITIES = 4000;


using ComponentType = std::uint16_t;
const ComponentType MAX_COMPONENTS = 32;

/* A bitset used to represent what components an entity has. A component's unique ID is represented by a bit, where 1
means the entity has that component and 0 meand it does not. The unique ID is the "index" of the bit.
*/
using Signature = std::bitset<MAX_COMPONENTS>;
