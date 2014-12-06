import csv
import numpy as np
import random
import scipy.io as sio
import numpy as np
import datetime as dt

from sklearn.metrics import accuracy_score
import sklearn.linear_model

def getIndices(headers, reqdFields):
    (result, winnerIdx, loserIdx, surfaceIdx, commentIdx, winnerRankIdx, loserRankIdx, courtIdx, dateIdx) = ([], -1, -1, -1, -1, -1, -1, -1, -1)
    for i, h in enumerate(headers):
        if h == 'Winner':
            winnerIdx = i
        elif h == 'Loser':
            loserIdx = i
        elif h == 'Surface':
            surfaceIdx = i
        elif h == 'Comment':
            commentIdx = i
        elif h == 'WRank':
            winnerRankIdx = i
        elif h == 'LRank':
            loserRankIdx = i
        elif h == 'Court':
            courtIdx = i
        elif h == 'Date':
            dateIdx = i
        if h in reqdFields:
            result.append(i)
    return (result, winnerIdx, loserIdx, surfaceIdx, commentIdx, winnerRankIdx, loserRankIdx, courtIdx, dateIdx)

dataFiles = ['2008.csv', '2009.csv', '2010.csv', '2011.csv', '2012.csv', '2013.csv', '2014.csv']

matchData_X = []
matchData_Y = []
(players, playerId) = ({}, 1)
(surfaceTypes, surfaceId) = ({}, 0)
numSurfaces = 4
(courtTypes, courtId) = ({}, 0)
reqdFields = ['Date', 'Court', 'Surface', 'Best of', 'WRank', 'LRank', 'WPts', 'LPts'] # Fields needed in training data
dateFormat = '%m/%d/%y'

for dataFile in dataFiles:
    print 'Scanning file ' + dataFile + '....'
    with open('data/' + dataFile, 'rU') as f:
        reader = csv.reader(f)
        headers = reader.next()
        headerIndices, winnerIdx, loserIdx, surfaceIdx, commentIdx, winnerRankIdx, loserRankIdx, courtIdx, dateIdx = getIndices(headers, reqdFields)
        headerIndices = np.array(headerIndices)

        for row in reader:
            if row[commentIdx] == 'Completed' and row[winnerRankIdx] != 'N/A' and row[loserRankIdx] != 'N/A': # Only use completed matches for now

                # Add surface and players to id map (sort of a database)
                prevWinnerMatch, prevLoserMatch = (None, None)
                ps = [row[winnerIdx], row[loserIdx]]
                for i, player in enumerate(ps):
                    if not players.has_key(player):
                        players[player] = (playerId, row)
                        playerId += 1
                    else:
                        if i == 0:
                            prevWinnerMatch = players[player][1]
                        else:
                            prevLoserMatch = players[player][1]
                        players[player] = (players[player][0], row)

                if (prevWinnerMatch == None or prevLoserMatch == None):
                    continue

                if not surfaceTypes.has_key(row[surfaceIdx]):
                    surfaceTypes[row[surfaceIdx]] = surfaceId
                    surfaceId += 1

                if not courtTypes.has_key(row[courtIdx]):
                    courtTypes[row[courtIdx]] = courtId
                    courtId += 1
                court = float(courtTypes[row[courtIdx]])

                currentMatchDate = dt.datetime.strptime(row[dateIdx], dateFormat)
                prevWinnerMatchDate, prevLoserMatchDate = (dt.datetime.strptime(prevWinnerMatch[dateIdx], dateFormat), dt.datetime.strptime(prevLoserMatch[dateIdx], dateFormat))
                daysPrevMatchWinner, daysPrevMatchLoser = ((currentMatchDate - prevWinnerMatchDate).days, (currentMatchDate - prevLoserMatchDate).days)

                # Set surfaces
                surfaces = [0 for i in xrange(numSurfaces)]
                surfaces[surfaceTypes[row[surfaceIdx]]] = 1

                # Randomly switch winner and loser positions to get some y=1 points in training also
                r = np.array(row)
                r = r[headerIndices]
                r = np.array([float(court), float(r[3]), float(r[4]), float(r[5]), float(r[6]), float(r[7]), float(daysPrevMatchWinner), float(daysPrevMatchLoser), float(surfaces[0]), float(surfaces[1]), float(surfaces[2]), float(surfaces[3])])
                y = 0 # Left is the winner
                if (random.random() >= 0.5):
                    # court, best of,  wRank, lRank, wPts, lPts, days since previous match P1, days previous match P2, 4 surface dummies
                    r = np.array([r[0], r[1], r[3], r[2], r[4], r[5], r[6], r[7], r[8], r[9], r[10], r[11]])
                    y = 1 # Right is the winner
                matchData_X.append(r)
                matchData_Y.append(y)
                # matchData.append((r, y))

matchData_X = np.array(matchData_X)
matchData_Y = np.array(matchData_Y)

print 'Num players:', len(players)
print 'Num matches:', matchData_X.shape[0]
print 'Num features:', matchData_X.shape[1]
print 'Sample:'
print matchData_X[:5]
print matchData_Y[:5]
print surfaceTypes
print courtTypes

# At this point we have all the training data we need
# Train on first N data points

model = sklearn.linear_model.LogisticRegression(penalty='l2')
model = model.fit(matchData_X[:16000], matchData_Y[:16000])

# Test on remaining points
predicted_Y = np.array(model.predict(matchData_X[16000:]))  # Predict the chance that rank 1 will beat rank 70 on surface 1 (clay) and outdoor
print predicted_Y[:5]
actual_Y = np.array(matchData_Y[16000:])

print 'Accuracy:', accuracy_score(actual_Y, predicted_Y)

