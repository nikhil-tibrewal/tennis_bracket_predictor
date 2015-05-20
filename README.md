# Tennis bracket predictor in Python

This repo contains code for a tennis match predictor. It is entirely written in Python using data from the last 5-6 years.

There are two active branches currently:
- **master**: The code in this branch uses 12 features:
  1. Court type (indoor or outdoor)
  2. Best of (number of sets is the match best of)
  3. Rank of winner
  4. Rank of loser
  5. Points on tour of the winner
  6. Points on tour of the loser
  7. Days since previous match of player 1 (left side in listing)
  8. Days since previous match of player 2 (right side in listing)
  9. Dummy for Hard surface
  10. Dummy for Clay surface
  11. Dummy for Carpet surface
  12. Dummy for Grass surface
