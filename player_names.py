import urllib
from bs4 import BeautifulSoup
from unidecode import unidecode

base_url = 'http://www.atpworldtour.com'

url1 = 'http://www.atpworldtour.com/Rankings/Singles.aspx?d=15.12.2014&r=1&c=#'
url2 = 'http://www.atpworldtour.com/Rankings/Singles.aspx?d=15.12.2014&r=101&c=#'
url3 = 'http://www.atpworldtour.com/Rankings/Singles.aspx?d=15.12.2014&r=201&c=#'
url4 = 'http://www.atpworldtour.com/Rankings/Singles.aspx?d=15.12.2014&r=301&c=#'
url5 = 'http://www.atpworldtour.com/Rankings/Singles.aspx?d=15.12.2014&r=401&c=#'
url6 = 'http://www.atpworldtour.com/Rankings/Singles.aspx?d=15.12.2014&r=501&c=#'
url7 = 'http://www.atpworldtour.com/Rankings/Singles.aspx?d=15.12.2014&r=601&c=#'

urls = [url1, url2, url3, url4, url5, url6, url7]

def make_url(player):
    parts = player.split('-')
    url1 = 'http://www.atpworldtour.com/Tennis/Players/%s/%s/%s.aspx' % (parts[-1][:2], parts[0][0], player)
    url2 = 'http://www.atpworldtour.com/Tennis/Players/%s/%s/%s.aspx' % (parts[-2][:2], parts[0][0], player)
    url3 = 'http://www.atpworldtour.com/Tennis/Players/Top-Players/%s.aspx' % player
    if len(parts) == 5:
        url2 = 'http://www.atpworldtour.com/Tennis/Players/%s/%s/%s.aspx' % (parts[1][:2], parts[0][0], player)
    if player == 'Izak-Van-Der-Merwe':
        url2 = 'http://www.atpworldtour.com/Tennis/Players/Va/I/Izak-Van-Der-Merwe.aspx'
    elif player == 'Jonathan-Dasnieres-De-Veigy':
        url2 = 'http://www.atpworldtour.com/Tennis/Players/Da/J/Jonathan-Dasnieres-De-Veigy.aspx'
    return (url1, url2, url3)

def get_main_player_links(f):

    for url in urls:
        print 'Getting players from: ' + url
        result = urllib.urlopen(url)
        html = result.read()
        soup = BeautifulSoup(html)

        rows = soup.find_all('tr')
        for row in rows:
            cells = row.find_all('td')
            for cell in cells:
                if 'class' in cell.attrs and 'first' in cell['class']:
                    links = cell.find_all('a')
                    if len(links) == 1:
                        player_url = base_url + links[0].attrs['href']
                        parts = (unidecode(unicode(links[0].string))).split(', ')
                        player = parts[1] + '-' + parts[0]
                        player = player.replace(' ', '-')
                        f.write('%s,%s,%s,%s\n' % (parts[1], parts[0], player, player_url))# firstname, lastname, hyphenated player name
    return None

def get_other_player_links(f):
    other_players = ['Brian-Dabul', 'Alessio-Di-Mauro', 'Rik-De-Voest', 'Jesse-Huta-Galung', 'Ariez-Elyaas-Deen-Heshaam', 'Izak-Van-Der-Merwe', 'Jonathan-Dasnieres-De-Veigy', 'Mousa-Shanan-Zayed', 'Andres-Artunedo-Martinavarro', 'Justin-Oneal', 'Bruno-Agostinelli', 'Sergio-Gutierrez-Ferrol', 'Arnau-Brugues-Davi', 'Albert-Brugues-Davi', 'Carlos-Gomez-Herrera', 'Daniel-King-Turner', 'Thierry-Ascione', 'Zack-Fleishman', 'Wishaya-Trongcharoenchaikul', 'Oleksandr-Dolgopolov-Sr', 'Clint-Bowles', 'Igor-Kunitsyn', 'David-Marrero', 'Felipe-Rios', 'Martin-Slanar', 'Kristian-Pless', 'Raemon-Sluiter', 'Arsenije-Zlatanovic', 'Grega-Zemlja', 'Roko-Karanusic', 'Dennis-Lajola', 'Stefano-Galvani', 'Sebastian-Rieschick', 'Kristof-Vliegen', 'Attila-Balazs', 'Colin-Ebelthite', 'Oliver-Marach', 'Martin-Emmrich', 'Jerome-Haehnel', 'Jiri-Vanek', 'Blake-Strode', 'Lars-Poerschke', 'Robin-Roshardt', 'Jan-Minar', 'Juan-Martin-Aranguren', 'Sandro-Ehrat', 'Lukas-Dlouhy', 'Chris-Guccione', 'Woong-Sun-Jun', 'Rameez-Junaid', 'Tomas-Cakl', 'Simon-Stadler', 'Robin-Vik', 'Gorka-Fraile', 'Takao-Suzuki', 'Marco-Crugnola', 'Francis-Tiafoe', 'Diego-Junqueira', 'Dawid-Olejniczak', 'Artem-Sitak', 'Colin-Fleming', 'Carsten-Ball', 'Bastian-Knittel', 'Josko-Topic', 'Jan-Lennard-Struff', 'Peng-Sun', 'Manuel-Sanchez', 'Santiago-Gonzalez', 'Harel-Levy', 'Romain-Jouan', 'Robert-Smeets', 'Juan-Pablo-Brzezicki', 'Chris-Eaton', 'Zhe-Li', 'Dominic-Inglot', 'Alun-Jones', 'Peerakiat-Siriluethaiwattana', 'Pablo-Galdon', 'Diego-Hartfield', 'Leonardo-Tavares', 'Denis-Gremelmayr', 'Kevin-Kim', 'Pavel-Snobel', 'Pierre-Ludovic-Duclos', 'Mikhail-Elgin', 'Ramon-Delgado', 'Brendan-Evans', 'Mehdi-Ziadi', 'Bartolome-Salva-Vidal', 'Clement-Reix', 'Adrian-Cruciat', 'Michael-Ryderstedt', 'Xin-Gao', 'Rabie-Chaki', 'Ilya-Belyaev', 'Dick-Norman', 'Amer-Delic', 'Tsung-Hua-Yang', 'Alexander-Peya', 'Flavio-Saretta', 'Sam-Warburg', 'Scoville-Jenkins', 'Ryan-Sweeting', 'Santiago-Ventura', 'Evgeny-Kirillov', 'Mao-Xin-Gong', 'Bjorn-Rehnquist', 'Bowen-Ouyang', 'Ludovic-Walter', 'Ivo-Minar', 'Andreas-Vinciguerra', 'Oscar-Hernandez', 'Jean-Rene-Lisnard', 'Fernando-Vicente', 'Lovro-Zovko', 'James-Lemke', 'Ivan-Sergeyev', 'Konstantinos-Economidis', 'Raven-Klaasen', 'Gabriel-Moraru', 'Josh-Goodall', 'Jason-Goodall', 'Richard-Bloomfield', 'Daniel-Koellerer', 'George-Bastl', 'Kyu-Tae-Im', 'Hicham-Khaddari', 'Rainer-Eitzinger', 'Aaron-Ramos', 'Alejandro-Ramos', 'Alberto-Ramos', 'Paul-Capdeville', 'Pierre-Hugues-Herbert', 'Nick-Lindahl', 'Joseph-Sirianni', 'Phillip-Simmonds', 'Jesse-Witten', 'Jean-Claude-Scherrer', 'Simon-Greul', 'Todd-Widom', 'Stephane-Bohli', 'Prakash-Amritraj', 'Nicolas-Renavand', 'Rohan-Bopanna', 'Alexander-Sadecky', 'Michael-Mcclune', 'Werner-Eschauer', 'Erik-Chvojka', 'Jan-Vacek', 'Roman-Valent', 'Scott-Lipsky', 'Jamie-Baker', 'Mikhail-Biryukov', 'Ryler-Deheart', 'Sergei-Bubka', 'Matteo-Viola', 'Henri-Kontinen', 'Michael-Yani', 'Denis-Matsukevich', 'Robert-Kendrick', 'Milos-Sekulic', 'Yuri-Schukin', 'Frantisek-Cermak', 'Alexander-Slabinsky', 'Sascha-Kloer', 'Filip-Prpic', 'Patrick-Ciorcila', 'Dominik-Meffert', 'James-Mcgee', 'Miguel-Angel-Lopez-Jaen', 'Cedrik-Marcel-Stebe', 'Rainer-Schuettler', 'Conor-Niland', 'Nikolai-Fidirko', 'Gabriel-Trujillo-Soler', 'Hugo-Armando', 'Sergey-Betov', 'Christophe-Rochus', 'Tomas-Zib', 'Mischa-Zverev', 'Marcos-Daniel', 'Michael-Daniel', 'Guillermo-Olaso', 'Michal-Mertinak', 'Roman-Borvanov', 'Karim-Maamoun', 'Tim-Goransson', 'Brian-Baker', 'Francesco-Piccari', 'Dieter-Kindlmann', 'Rik-De-Voest', 'Sebastian-Decoud', 'Petru-Alexandru-Luncanu', 'Noam-Okun', 'Suk-Young-Jeong', 'Thiago-Alves', 'Reda-El-Amrani', 'Nicolas-Devilder', 'Bruno-Echagaray', 'Clay-Thompson', 'Kittipong-Wachiramanowong', 'Philipp-Oswald', 'Sergio-Roitman', 'Aisam-Ul-Haq-Qureshi', 'Daniel-Munoz-De-La-Nava', 'Javier-Marti', 'Luka-Gregorc', 'Miguel-Angel-Reyes-Varela', 'Alexandre-Sidorenko', 'G-D-Jones', 'Petar-Jelenic', 'Benedikt-Dorsch', 'Yassine-Idmbarek', 'Andrey-Kumantsov', 'Robert-Farah', 'Ervin-Eleskovic', 'Peter-Luczak', 'Nathan-Pasha', 'Martin-Vassallo-Arguello', 'Guillermo-Alcaide', 'Massimo-Dellacqua', 'Jun-Chao-Xu', 'Franco-Ferreiro', 'Olivier-Patience', 'Younes-Rachidi', 'Laurent-Recouderc', 'Pedro-Sousa', 'Eduardo-Schwank', 'Sebastien-De-Chaunac', 'Andrea-Stoppini', 'Cecil-Mamiit', 'Mathieu-Montcourt', 'Ricardo-Mello', 'Hyung-Taik-Lee', 'Luka-Belic', 'Karlis-Lejnieks', 'Satoshi-Iwabuchi', 'Juan-Sebastian-Cabal', 'Romain-Bogaerts', 'Bruno-Rodriguez', 'Devin-Britton', 'Karim-Hossam', 'Augustin-Gensse', 'Pavol-Cervenak', 'Dusan-Vemic', 'Frederic-Niemeyer', 'Alex-Bogdanovic', 'Jonathan-Erlich', 'Tomas-Carbonell', 'Leander-Paes', 'Yannick-Noah', 'Kent-Carlsson', 'Mardy-Fish', 'Todd-Witsken', 'Donald-Johnson', 'Alberto-Mancini', 'Mike-Bryan', 'David-Nalbandian', 'Janko-Tipsarevic', 'Marc-Rosset', 'Stefan-Koubek', 'Francesco-Cancellotti', 'Jordi-Arrese', 'Max-Mirnyi', 'Todd-Martin', 'Henrik-Holm', 'MaliVai-Washington', 'Vincent-Spadea', 'Jacco-Eltingh', 'Ken-Flach', 'Franco-Davin', 'Alexander-Volkov', 'Karol-Kucera', 'David-Adams', 'Mariano-Puerta', 'Younes-F-El-Aynaoui', 'Derrick-Rostagno', 'Paul-Annacone', 'Agustin-Calleri', 'Carlos-Moya', 'Mario-Ancic', 'Patrick-McEnroe', 'Andrei-Chesnokov', 'Andrei-Pavel', 'Ben-Testerman', 'Juan-Ignacio-Chela', 'Francisco-Clavet', 'Thierry-Champion', 'Scott-Draper', 'Brad-Gilbert', 'Magnus-Gustafsson', 'Aaron-Krickstein', 'Libor-Pimek', 'Julian-Knowle', 'Renzo-Furlan', 'Guy-Forget', 'Hendrik-Dreekmann', 'Thomas-Enqvist', 'Sergi-Bruguera', 'Grant-Connell', 'Marcelo-Filippini', 'Goran-Prpic', 'Juan-Carlos-Ferrero', 'Ivan-Ljubicic', 'Pete-Sampras', 'Omar-Camporese', 'Richey-Reneberg', 'Guillermo-Coria', 'John-Fitzgerald', 'Mats-Wilander', 'Magnus-Larsson', 'David-Pate', 'Sebastien-Grosjean', 'Todd-Woodbridge', 'Cristiano-Caratti', 'Jose-Acasuso', 'Andre-Sa', 'Slobodan-Zivojinovic', 'Andy-Ram', 'Andrei-Cherkasov', 'Marat-Safin', 'Slava-Dosedel', 'Anders-Jarryd', 'Byron-Black', 'Mark-Knowles', 'Hicham-Arazi', 'Rick-Leach', 'Albert-Costa', 'Rodney-Harmon', 'Gustavo-Kuerten', 'Jim-Grabb', 'Joachim-Johansson', 'Igor-Andreev', 'Ramesh-Krishnan', 'Franco-Squillari', 'Robert-Seguso', 'Henrik-Sundstrom', 'Mahesh-Bhupathi', 'Arnaud-Clement', 'Amos-Mansdorf', 'Kevin-Ullyett', 'Wayne-Ferreira', 'Cedric-Pioline', 'Joakim-Nystrom', 'Alberto-Berasategui', 'Greg-Rusedski', 'Goran-Ivanisevic', 'Paul-Haarhuis', 'Bernd-Karbacher', 'Dominik-Hrbaty', 'Patrick-Rafter', 'Yevgeny-Kafelnikov', 'Thomas-Johansson', 'Nicolas-Kiefer', 'Martin-Jaite', 'Kelly-Jones', 'Ronald-Agenor', 'Fernando-Meligeni', 'Andres-Gomez', 'Richard-Fromberg', 'Gaston-Gaudio', 'Mikael-Pernfors', 'Pieter-Aldrich', 'Boris-Becker', 'Wally-Masur', 'Filip-Dewulf', 'Matt-Anger', 'Mark-Woodforde', 'Thierry-Tulasne', 'Jason-Stoltenberg', 'Taylor-Dent', 'Scott-Davis', 'Paradorn-Srichaphan', 'David-Wheaton', 'Milan-Srejber', 'Tim-Mayotte', 'Karel-Novacek', 'Felix-Mantilla', 'Danie-Visser', 'Guillermo-Canas', 'Stefan-Edberg', 'Luis-Horna', 'Michael-Stich', 'Magnus-Norman', 'Mariano-Zabaleta', 'Dan-Goldie', 'Sandon-Stolle', 'Jiri-Novak', 'Jeremy-Bates', 'Daniel-Nestor', 'Jerome-Golmard', 'Ivan-Lendl', 'Richard-Krajicek', 'Christian-Bergstrom', 'James-Blake', 'Wesley-Moodie', 'Nicolas-Lapentti', 'Jared-Palmer', 'Peter-Lundgren', 'Adrian-Voinea', 'Mark-Philippoussis', 'Marcelo-Rios', 'Andrea-Gaudenzi', 'Patrick-Galbraith', 'Petr-Korda', 'Nicolas-Massu', 'Andre-Agassi', 'Henri-Leconte', 'Bob-Bryan', 'Pat-Cash', 'Cyril-Suk', 'Martin-Verkerk', 'Wayne-Black', 'Chris-Woodruff', 'Jonathan-Stark', 'Jonas-Bjorkman', 'Karim-Alami', 'Brett-Steven', 'Jay-Berger', 'Horst-Skoff', 'Juan-Aguilera', 'Jan-Siemerink', 'Stephen-Huss', 'Jakob-Hlasek', 'Fabrice-Santoro', 'Nicklas-Kulti', 'Tim-Henman', 'Emilio-Sanchez', 'Ulf-Stenlund', 'Carlos-Costa', 'Sjeng-Schalken', 'Jaime-Yzaga', 'Thomas-Muster', 'Shuzo-Matsuoka', 'Michael-Chang', 'Alexander-Popp', 'Andy-Roddick', 'Alex-Corretja', 'Galo-Blanco', 'Nicolas-Escude', 'Laurie-Warder', 'Jimmy-Arias', 'Fernando-Gonzalez', 'Robin-Soderling', 'Andrei-Medvedev', 'Mikael-Tillstrom', 'Nenad-Zimonjic', 'Xavier-Malisse']

    print 'Scanning other players...'
    for i, other_player in enumerate(other_players):
        print 'Trying %s' % other_player
        parts = other_player.split('-')
        first = parts[0]
        last = '-'.join(parts[1:])
        url1, url2, url3 = make_url(other_player)
        other_player_data = None

        for url in [url1, url2, url3]:
            result = urllib.urlopen(url)
            html = result.read()
            if html.find('Page-Not-Found') == -1:
                other_player_data = (first, last, other_player, url)

        if other_player_data == None:
            print other_player
        else:
            f.write('%s,%s,%s,%s\n' % (other_player_data[0], other_player_data[1], other_player_data[2], other_player_data[3]))

        if i%10 == 0:
            print '%d other players done' % i
    return None

if __name__ == '__main__':
    f = open('player_names_links.txt', 'w')
    players = get_main_player_links(f)
    other_players = get_other_player_links(f)

