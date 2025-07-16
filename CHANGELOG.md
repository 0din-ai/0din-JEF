# Changelog

All notable changes to this project will be documented in this file.


## [0.1.0] - 2025-05-15

### Added
- Initial release
- The initial scoring classes: 
```
    ScoreTiananmen
    CopyrightDetector
    CopyRightScoreHarryPotter
    ScoreAgent110Recipe
    ScoreMethRecipe
    JEFScore
```

### Changed
- Initialize release

### Fixed
- Initialize release

## [0.1.1] - 2025-05-19

### ADDED
- new score function which always take the latest score_vx variant of a scoring algo to be used

### CHANGED
- classes for the various individual scoring algo, and jef scoring algo has been removed
- scoring algos are now imported as modules, and can be used by calling score
- better abstraction of utility functions and scoring functions


## [0.1.2] - 2025-6-04

### CHANGED
- slight optimization to copyright algo. Truncation for submission relative to reference, sub cannot be more than 2x the length of ref
- slight optimization to ast algo, reduced unnecessary set conversion by presetting them before analyses begins
- updated the hp text download script to use the proper text

## [0.1.5] - 2025-6-12

### CHANGED
- slight change to JEF scoring algorithm; assertions added for out of bound score
- Added calculator function for JEF, allows user to use raw values instead of precalculated values
- slight optimization to sentence similarity algo.

## [0.1.6] - 2025-07-16
### CHANGED
- corrected constants for nerve agent test