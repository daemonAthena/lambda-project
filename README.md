
This is young Daemon Athena's computer science 1 final project. It is a game I made using the pygame module. Once I re-read the thing I will edit this for a more in depth walkthrough of mechanics and functions.

## Helper Functions
There is a series of utility functions which:
    - convert things to and from the grid the game goes by to the pixel position of sprites rendered in game.
    - obtain distance of two points
    - a function which returns the closest possible point given a set of points.
    - Adds a point to a given point in a given direction and distance.
    - Returns a set of points forming a ring at distance n from the given point. An n-ring has 8n vertices surrounding the center.
    - Takes two points and returns the direct path as a list.

## Classes

Terrain: 
    Terrain Attributes
    - *type*
    - *position*
    - render
    - color
    - penalty
    - advantage

Unit:
    Unit Attributes
    - *color*
    - *type*
    - *position*
    - movement
    - strength
    - image

    Unit Functions
    - range
    - attack_range

## 