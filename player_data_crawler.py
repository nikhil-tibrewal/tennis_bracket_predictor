# Crawl ATP World tour web page for some personal data for players
# height, birthdate, nationality, wieght, turned pro year, righty vs lefty

import urllib
from bs4 import BeautifulSoup
from d import get_all_player_links

player_info_id = 'playerBioInfoList'
player_nationality_id = 'playerBioInfoFlag'
players = []

players_file = open('player_names_links.txt', 'rU')
# players_file.seek(-71618, 2)
for line in players_file:
    parts = line.strip().split(',')
    parts = map(lambda x: x.strip(), parts)
    players.append(tuple(parts))

f = open('player_bio.txt', 'w')

not_found_players = []

def get_data_write_2_file(player, url, player_nationality_id, player_info_id):
    result = urllib.urlopen(url)
    html = result.read()
    soup = BeautifulSoup(html)

    nationality = soup.find(id=player_nationality_id).p.string

    name_parts = player[2].split('-')
    if player[2] == 'Juan-Martin-Del-Potro':
        name = 'Del Potro J.M.'
    elif player[2] == 'Younes-F-El-Aynaoui':
        name = 'El Aynaoui Y.'
    elif player[2] == 'Jose-(Rubin)-Statham':
        name = 'Statham R.'
    elif player[2] == 'Massimo-Dellacqua':
        name = "Dell'Acqua M."
    elif player[2] == 'G-D-Jones':
        name = 'Jones G.D.'
    elif player[2] == 'Miguel-Angel-Reyes-Varela':
        name = 'Reyes-Varela M.A.'
    elif player[2] == 'Aisam-Ul-Haq-Qureshi':
        name = 'Qureshi A.U.H.'
    elif player[2] == 'Gabriel-Trujillo-Soler':
        name = 'Trujillo G.'
    elif player[2] == 'Miguel-Angel-Lopez-Jaen':
        name = 'Lopez-Jaen M.A.'
    elif player[2] == 'Bartolome-Salva-Vidal':
        name = 'Salva B.'
    elif player[2] == 'Alex-Bogomolov-Jr.':
        name = 'Bogomolov A.'
    elif player[2] == 'Oleksandr-Dolgopolov-Sr':
        name = 'Dolgopolov O.'
    elif player[2] == 'Hans-Podlipnik-Castillo':
        name = 'Podlipnik H.'
    elif player[2] == 'Justin-Oneal':
        name = "O'Neal J."
    elif player[2] == 'Mousa-Shanan-Zayed':
        name = 'Zayed M. S.'
    elif player[2] == 'Jonathan-Dasnieres-De-Veigy':
        name = 'Dasnieres de Veigy J.'
    elif player[2] == 'Izak-Van-Der-Merwe':
        name = 'Van Der Merwe I.'
    elif player[2] == 'Ariez-Elyaas-Deen-Heshaam':
        name = 'Deen Heshaam A.'
    elif player[2] == 'Thiemo-de-Bakker':
        name = 'De Bakker T.'
    elif player[2] == 'Daniel-Munoz-De-La-Nava':
        name = 'Munoz de la Nava D.'
    elif len(name_parts) == 2:
        name = name_parts[1] + ' ' + name_parts[0][0] + '.'
    elif len(name_parts) == 3:
        if name_parts[1] == 'De' or name_parts[1] == 'El' or player[2] in ['Roberto-Carballes-Baena', 'Andres-Artunedo-Martinavarro', 'Rogerio-Dutra-Silva', 'Jesse-Huta-Galung', 'Cristobal-Saavedra-Corvalan', 'Victor-Estrella-Burgos', 'Alessio-Di-Mauro']:
            name = name_parts[1] + ' ' + name_parts[2] + ' ' + name_parts[0][0] + '.'
        elif player[2] in ['Somdev-K-Devvarman']:
            name = name_parts[2] + ' ' + name_parts[0][0] + '.'
        elif player[2] in ['Yen-Hsun-Lu', 'Jo-Wilfried-Tsonga', 'Paul-Henri-Mathieu', 'Juan-Ignacio-Chela', 'Juan-Carlos-Ferrero', 'John-Patrick-Smith', 'Juan-Sebastian-Cabal', 'Hyung-Taik-Lee', 'Jun-Chao-Xu', 'Suk-Young-Jeong', 'Petru-Alexandru-Luncanu', 'Cedrik-Marcel-Stebe', 'Jean-Claude-Scherrer', 'Pierre-Hugues-Herbert', 'Kyu-Tae-Im', 'Juan-Ignacio-Londero', 'Jean-Rene-Lisnard', 'Mao-Xin-Gong', 'Tsung-Hua-Yang', 'Pierre-Ludovic-Duclos', 'Juan-Pablo-Brzezicki', 'Jan-Lennard-Struff', 'Juan-Martin-Aranguren', 'Woong-Sun-Jun']:
            name = name_parts[2] + ' ' + name_parts[0][0] + '.' + name_parts[1][0] + '.'
        elif player[2] in ['Roberto-Bautista-Agut']:
            name = name_parts[1] + ' ' + name_parts[0][0] + '.'
        elif player[2] in ['Daniel-Gimeno-Traver', 'Albert-Ramos-Vinolas', 'Andreas-Haider-Maurer', 'Edouard-Roger-Vasselin', 'Guillermo-Garcia-Lopez', 'Martin-Vassallo-Arguello', 'Adrian-Menendez-Maceiras', 'Pablo-Carreno-Busta', 'Daniel-King-Turner', 'Carlos-Gomez-Herrera', 'Sergio-Gutierrez-Ferrol', 'Arnau-Brugues-Davi', 'Albert-Brugues-Davi', 'Ruben-Ramirez-Hidalgo']:
            name = name_parts[1] + '-' + name_parts[2] + ' ' + name_parts[0][0] + '.'


    infos = [name, nationality, player[2]]
    bio_info_list = soup.find(id=player_info_id).find_all('li')
    for info in bio_info_list:
        text = info.get_text()

        if ('Age' in text):
            id_start = text.find('(')
            date_str = str(text[id_start+1:-1])
            infos.append(date_str)

        if ('Height' in text):
            id_start = text.find('(')
            infos.append(str(text[id_start+1:-4]))

        if ('Weight' in text):
            id_start = text.find('(')
            infos.append(str(text[id_start+1:-4]))

        if ('Plays' in text):
            if 'Left' in text:
                infos.append('Left')
            else:
                infos.append('Right')

        if ('Turned Pro' in text):
            infos.append(str(text[-4:]))
    return infos

i = 0
for player in players:
    url = player[3]
    print 'Gathering data for %s (%s)' % (player[2], url)
    try:
        infos = get_data_write_2_file(player, url, player_nationality_id, player_info_id)
        f.write(','.join(infos) + '\n')
    except Exception as e:
        not_found_players.append(player)
        print '   Error: ' + e.message
    i += 1
    if i%100 == 0:
        print '======= %d Players Done =======' % i
        print not_found_players

print not_found_players
