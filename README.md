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
- **fieldsmap**: This is a testing branch where I am testing new features, especially bio data of players such as height, country, weight, right handed vs left handed, years the player has been playing professionally, age etc. I also added a bunch of other non demographic features like the number of sets lost in the previous match since I expected this to affect the current match (players with longer previous matches might be more tired coming in to this match). To get the bio data for this branch, I have a script that crawls ATP World Tour website for all players and gets the information. Due to different number of words comprising a name (some players have 4 names, some 2, some 3), the exact URL of the player differs. Since there's a limited number of players that have these edge cases (much smaller compared to the total size of ~700), I decided to manually go and find a way to generate URLs for these players. This script runs once and writes the bio data of the players in a separate file so it doesn't need to run again.

Both branches ignore some matches such as retired. In the future, I'd also like to get historical weather data to see if it improves the model. This is because sometimes matches are delayed due to rain, and in the past this has drastically affected results.

###Here is the current accuracy of the two models:
- **master**: ~68%
- **fieldsmap**: ~67%

These implementations use Logistic Regression to predict winner and loser. The biggest limitation of this model is the size of the data set. Even over 7 years of data, there's only 17000 matches. Furthermore, a lot of these players (especially the low ranked ones) do not have enough bio data (in which case their matches are ignored). Yet, to mirror real world ML applications, I'm implementing an approach where the first 13000 matches are used as training set, and the remaining are used as test set.

# Running the script
To run this script, just clone the repo and run
```
python mastermind.py
```
All the preprocessing is done and exists in the relevant .txt files. If you happen to delete any of them, you'll have to run the crawlers to get the data (or you could just clone again :))

# Future of this implementation
I love tennis! So I'm definitely going to pick this up again. Add more features to it, try out other classifiers, and eventually build a small fun webapp that has two fields to choose players and will tell the user which player will win if they were to play against each other.

And just because I'm a Rafa Nadal fan... **VAMOS!**
