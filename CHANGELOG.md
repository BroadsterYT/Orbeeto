# v0.1.0-alpha

## Features

- Added ``CHANGELOG.md``.
- Removed unnecessary class ``InvisObj``.
- Implemented a locked wall (``LockedWall``) that can be activated with a button.
- Implemented ``@numba.njit`` to some mathematical functions

## Fixes

- Moved ``Player``, ``Room``, and ``RoomContainer`` classes to their own respective files.
- For player and all enemy classes: changed various in-game instance attributes into properties.
- Added ``self.layer`` attributes for more concise drawing of sprites.
- Began changing instance attribute names from mixedCase format to snake_case.
- Removed bullet dependencies on their firers.
- Removing need on an attack value for player/enemies to depend on. Now, only the bullet's damage and the entity's defense value determine the damage received.
- Fixed portal placement when placed on long/wide walls