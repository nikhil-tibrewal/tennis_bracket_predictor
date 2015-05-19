# Head 2 head
# country of two players
# height of players
# righty vs lefty
# avg serve speed

import csv
import numpy as np
import random
import scipy.io as sio
import numpy as np
import datetime as dt
import random
import sys

from sklearn.metrics import accuracy_score
import sklearn.linear_model

def getIndices(headers, reqdFields):
    fieldsIdxMap = {}
    for i, h in enumerate(headers):
        if h in reqdFields:
            fieldsIdxMap[h] = i
    return fieldsIdxMap

def sanityCleanPlayer(player):
    player = player.strip()
    sanityDict = {'Djokovic M.': 'Djokovic N.',
                  'Del Potro J.': 'Del Potro J.M.',
                  'Statham J.': 'Statham R.',
                  'Kuznetsov Al.': 'Kuznetsov A.',
                  'de Chaunac S.': 'De Chaunac S.',
                  'Kuznetsov An.': 'Kuznetsov A.',
                  'Munoz de La Nava D.': 'Munoz de la Nava D.',
                  'Munoz-De La Nava D.': 'Munoz de la Nava D.',
                  'Stebe C-M.': 'Stebe C.M.',
                  'Matsukevitch D.': 'Matsukevich D.',
                  'Viola Mat.': 'Viola M.',
                  'Kohlschreiber P..': 'Kohlschreiber P.',
                  'Struff J-L.': 'Struff J.L.',
                  'Herbert P-H.': 'Herbert P.H.',
                  'Kim K': 'Kim K.',
                  'Van der Merwe I.': 'Van Der Merwe I.',
                  'Van D. Merwe I.': 'Van Der Merwe I.',
                  'Dutra Da Silva R.': 'Dutra Silva R.',
                  'de Voest R.': 'De Voest R.',
                  'Estrella V.': 'Estrella Burgos V.'}
    if player in sanityDict:
        player = sanityDict[player]
    return player

def getPlaysValue(plays):
    if plays == 'Right':
        return 0
    return 1

dataFiles = ['2008.csv', '2009.csv', '2010.csv', '2011.csv', '2012.csv', '2013.csv', '2014.csv']
playerBioFile = 'player_bio.txt'

# Load Player bios in memory
playerBios = {}
notFoundBios = set()
missingDataBios = set()
with open(playerBioFile, 'rU') as f:
    for line in f:
        parts = line.strip().split(',')
        if parts[2] == ' Republic of':
            parts[2] = parts[2] + ',' + parts[3]
            parts.pop(3)

        if len(parts) == 8:
            if parts[0] in playerBios:
                playerBios[parts[0]].append(parts[1:])
            else:
                playerBios[parts[0]] = [parts[1:]]
        else:
            missingDataBios.add(line)

# Get training data for matches
matchData_X = []
matchData_Y = []
(players, playerId) = ({}, 1)
(surfaceTypes, surfaceId) = ({}, 0)
numSurfaces = 4
(courtTypes, courtId) = ({}, 0)
reqdFields = ['Date', 'Court', 'Surface', 'Best of', 'WRank', 'LRank', 'WPts', 'LPts', 'Winner', 'Loser', 'Comment', 'Lsets'] # Fields needed in training data
dateFormat = '%m/%d/%y'
birthDateFormat = '%d.%m.%Y'

for dataFile in dataFiles:
    print 'Scanning file ' + dataFile + '....'
    with open('data/' + dataFile, 'rU') as f:
        reader = csv.reader(f)
        headers = reader.next()
        fieldsIdxMap = getIndices(headers, reqdFields)

        for row in reader:
            if (row[fieldsIdxMap['Comment']] == 'Completed' and
            row[fieldsIdxMap['WRank']] != 'N/A' and row[fieldsIdxMap['LRank']] != 'N/A'): # Only use completed matches for now

                # Add surface and players to id map (sort of a database)
                prevWinnerMatch, prevLoserMatch = (None, None)
                bioWinner, bioLoser = (None, None)
                ps = [row[fieldsIdxMap['Winner']], row[fieldsIdxMap['Loser']]]
                for i, player in enumerate(ps):
                    player = sanityCleanPlayer(player)
                    if not players.has_key(player):
                        players[player] = (playerId, row)
                        playerId += 1
                    else:
                        if i == 0:
                            prevWinnerMatch = players[player][1]
                        else:
                            prevLoserMatch = players[player][1]
                        players[player] = (players[player][0], row)

                    if player in playerBios:
                        if i == 0:
                            bioWinner = playerBios[player]
                        else:
                            bioLoser = playerBios[player]
                    else:
                        notFoundBios.add(player)

                if (prevWinnerMatch == None or prevLoserMatch == None or bioWinner == None or bioLoser == None):
                    continue

                if not surfaceTypes.has_key(row[fieldsIdxMap['Surface']]):
                    surfaceTypes[row[fieldsIdxMap['Surface']]] = surfaceId
                    surfaceId += 1

                if not courtTypes.has_key(row[fieldsIdxMap['Court']]):
                    courtTypes[row[fieldsIdxMap['Court']]] = courtId
                    courtId += 1
                court = float(courtTypes[row[fieldsIdxMap['Court']]])

                # Get sets lots in previous match, and days since previous match
                currentMatchDate = dt.datetime.strptime(row[fieldsIdxMap['Date']], dateFormat)
                prevWinnerMatchDate, prevLoserMatchDate = (dt.datetime.strptime(prevWinnerMatch[fieldsIdxMap['Date']], dateFormat), dt.datetime.strptime(prevLoserMatch[fieldsIdxMap['Date']], dateFormat))
                daysPrevMatchWinner, daysPrevMatchLoser = ((currentMatchDate - prevWinnerMatchDate).days, (currentMatchDate - prevLoserMatchDate).days)
                prevLSetsWinner, prevLSetsLoser = (float(prevWinnerMatch[fieldsIdxMap['Lsets']]) / float(prevWinnerMatch[fieldsIdxMap['Best of']]),
                    float(prevLoserMatch[fieldsIdxMap['Lsets']]) / float(prevLoserMatch[fieldsIdxMap['Best of']]))

                # Get player biodata
                bioWinner, bioLoser = (random.choice(bioWinner), random.choice(bioLoser))
                winnerBirthDate, loserBirthDate = (dt.datetime.strptime(bioWinner[2], birthDateFormat), dt.datetime.strptime(bioLoser[2], birthDateFormat))
                winnerAge, loserAge = ((winnerBirthDate - currentMatchDate).days, (loserBirthDate - currentMatchDate).days)
                winnerHeight, loserHeight = (float(bioWinner[3]), float(bioLoser[3]))
                winnerWeight, loserWeight = (float(bioWinner[4]), float(bioLoser[4]))
                winnerPlays, loserPlays = (getPlaysValue(bioWinner[5]), getPlaysValue(bioLoser[5]))
                winnerProAge, loserProAge = (currentMatchDate.year - int(bioWinner[6]), currentMatchDate.year - int(bioLoser[6]))

                # Set surfaces
                surfaces = [0 for i in xrange(numSurfaces)]
                surfaces[surfaceTypes[row[fieldsIdxMap['Surface']]]] = 1

                # Randomly switch winner and loser positions to get some y=1 points in training also
                r = np.array(row)
                r = np.array([float(court), float(r[fieldsIdxMap['Best of']]),
                    float(r[fieldsIdxMap['WRank']]), float(r[fieldsIdxMap['LRank']]),
                    float(r[fieldsIdxMap['WPts']]), float(r[fieldsIdxMap['LPts']]), float(daysPrevMatchWinner),
                    float(daysPrevMatchLoser), float(surfaces[0]), float(surfaces[1]), float(surfaces[2]), float(surfaces[3]),
                    prevLSetsWinner, prevLSetsLoser, float(winnerAge), float(loserAge), float(winnerHeight), float(loserHeight),
                    float(winnerWeight), float(loserWeight), float(winnerPlays), float(loserPlays), float(winnerProAge), float(loserProAge)])
                y = 0 # Left is the winner
                if (random.random() >= 0.5):
                    # court, best of,  wRank, lRank, wPts, lPts, days since previous match P1, days previous match P2, 4 surface dummies
                    r = np.array([r[0], r[1], r[3], r[2], r[4], r[5], r[6], r[7], r[8], r[9], r[10], r[11], r[12], r[13], r[14], r[15], r[16], r[17], r[18], r[19], r[20], r[21], r[22], r[23]])
                    y = 1 # Right is the winner
                matchData_X.append(r)
                matchData_Y.append(y)

print 'Not found player biodata for:', notFoundBios
print 'Missing info player data for %d players' % len(missingDataBios)

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

(train_X, test_X, train_Y, test_Y) = (matchData_X[:13000], matchData_X[13000:], matchData_Y[:13000], matchData_Y[13000:])
model = sklearn.linear_model.LogisticRegression(penalty='l2')
model = model.fit(train_X, train_Y)

# Test on remaining points
predicted_Y = np.array(model.predict(test_X))  # Predict the chance that rank 1 will beat rank 70 on surface 1 (clay) and outdoor
print predicted_Y[:5]
actual_Y = np.array(test_Y)

print 'Accuracy:', accuracy_score(actual_Y, predicted_Y)

