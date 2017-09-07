import discord
import imgkit
import requests
import shutil
import urllib, requests
from io import StringIO
from beautifultable import BeautifulTable
import gspread
from oauth2client.service_account import ServiceAccountCredentials

client = discord.Client()
war = False
number_list = ['!1,', '!2,', '!3,', '!4,', '!5,', '!6,', '!7,']
table_6 = [15, 12, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1]
table_5 = [12, 10, 8, 7, 6, 5, 4, 3, 2, 1]
table_4 = [10, 8, 6, 5, 4, 3, 2, 1]
LU = []
total_6 = 82
total_5 = 58
total_4 = 39
sum = 0
race = 0
war_list = []
welcius = False
maintenance = "Not planned"

URL_GENERADOR_TABLAS = "http://welcius.pythonanywhere.com/createtable"


def getTablaWar(rutaImagen, infoClanLocal, infoScoresClanLocal, infoClanRival, infoScoresClanRival):
    # pre: Los parametros siguen los siguientes formatos
    #		infoClan -> ["nombre del clan", "tag del clan"]
    #		infoScores -> [("nombre jugador 1", "score jugador 1"), ("nombre jugador 2", "score jugador 2"), ...]
    # post: guarda la imagen de la tabla a crear en rutaImagen, retorna True si todo ha sido correcto

    listaParametros = ["player_name_A1", "", "player_score_A1", "",
                       "player_name_A2", "", "player_score_A2", "",
                       "player_name_A3", "", "player_score_A3", "",
                       "player_name_A4", "", "player_score_A4", "",
                       "player_name_A5", "", "player_score_A5", "",
                       "player_name_A6", "", "player_score_A6", "",
                       "player_name_B1", "", "player_score_B1", "",
                       "player_name_B2", "", "player_score_B2", "",
                       "player_name_B3", "", "player_score_B3", "",
                       "player_name_B4", "", "player_score_B4", "",
                       "player_name_B5", "", "player_score_B5", "",
                       "player_name_B6", "", "player_score_B6", "",
                       "clan_name_A", infoClanLocal[0], "clan_tag_A", infoClanLocal[1],
                       "clan_name_B", infoClanRival[0], "clan_tag_B", infoClanRival[1]]

    for i in range(0, min(6, len(infoScoresClanLocal))):
        listaParametros[4 * i + 1] = infoScoresClanLocal[i][0]
        listaParametros[4 * i + 3] = infoScoresClanLocal[i][1]

    for i in range(0, min(6, len(infoScoresClanRival))):
        listaParametros[6 * 4 + 4 * i + 1] = infoScoresClanRival[i][0]
        listaParametros[6 * 4 + 4 * i + 3] = infoScoresClanRival[i][1]

    parametros = dict(zip(listaParametros[0::2], listaParametros[1::2]))

    try:
        r = requests.post(URL_GENERADOR_TABLAS, data=parametros, stream=True)
    except:
        return False

    if r.status_code == 200:
        with open(rutaImagen, 'wb') as f:
            r.raw.decode_content = True
            shutil.copyfileobj(r.raw, f)
        return True
    return False

def mostrarimagen(nick):
    scope = ['https://spreadsheets.google.com/feeds']
    credentials = ServiceAccountCredentials.from_json_keyfile_name('CEMK-0ed44d25f869.json', scope)
    gc = gspread.authorize(credentials)
    wks = gc.open("TTMontewario").sheet1
    val = wks.get_all_values()
    val.sort(key=lambda x: x[3])
    indice = [x[1] for x in val].index(str(nick))
    return val[indice][4]



def sumatiempos(num, new):

    mintotal = int(int(num) / 100000)
    sectotal = int((int(num) - int(mintotal) * 100000) / 1000)
    miltotal = int(num) - int(mintotal) * 100000 - int(sectotal) * 1000

    minnew = int(int(new) / 100000)
    secnew = int((int(new) - int(minnew) * 100000) / 1000)
    milnew = int(new) - int(minnew) * 100000 - int(secnew) * 1000

    sumamil = milnew + miltotal
    bonussec = 0
    if (sumamil >= 1000):
        sumamil = sumamil - 1000
        bonussec = 1
    sumasec = bonussec + secnew + sectotal

    bonusmin = 0
    if (sumasec >= 60):
        sumasec = sumasec - 60
        bonusmin = 1
    print (sumasec)
    print (sumamil)
    sumamin = bonusmin + minnew + mintotal

    return int(sumamin * 100000 + sumasec * 1000 + sumamil)

def cargar(num):
    min = int(int(num)/100000)
    sec = int((int(num) - int(min)*100000)/1000)
    mil = int(num)-int(min)*100000-int(sec)*1000
    if(mil==0):
        return (str(min) + ":" + str(sec) + ",00" + str(mil))
    elif(mil<100):
        return (str(min) + ":" + str(sec) + ",0" + str(mil))
    else:
        return (str(min) + ":" + str(sec) + "," + str(mil))

def creadortablas(equipos, resultadostabla, typewar):

    arrmess = str(resultadostabla).split(",")
    if(len(arrmess)!=typewar*4): return "Introduce una cantidad de players correcta"
    if(len(str(equipos).split(","))!=2): return "Introduce dos equipos separados por comas"
    sum1 = 0
    sum2 = 0
    jugadores1 = []
    jugadores2 = []
    puntuaciones1 = []
    puntuaciones2 = []
    for x in range(0, typewar * 4):
        if (x % 2 != 0):
            if (x < typewar * 2):
                puntuaciones1.append(arrmess[x])
                sum1 += int(arrmess[x])
            else:
                puntuaciones2.append(arrmess[x])
                sum2 += int(arrmess[x])
        else:
            if (x < typewar * 2):
                jugadores1.append(arrmess[x])
            else:
                jugadores2.append(arrmess[x])

    test = []
    if(welcius):
        test2=[]
        test1=[]
        puntuaciones3=[]
        puntuaciones4=[]
        for x in range(0, typewar):
            test1.append((str(jugadores1[x]), str(puntuaciones1[x])))
            test2.append((str(jugadores2[x]), str(puntuaciones2[x])))
        getTablaWar("Tablitatabla2.jpg",
                    (str(str(equipos).split(",")[0]), str(str(equipos).split(",")[0])),
                    test1,
                    (str(str(equipos).split(",")[1]), str(str(equipos).split(",")[1])),
                    test2)
        print(test1)
        print(test2)
    else:
        table = BeautifulTable()
        test.append([str(str(equipos).split(",")[0]), "Puntuacion", str(str(equipos).split(",")[1]),"Puntuacion"])
        table.column_headers = [str(str(equipos).split(",")[0]), "Puntuacion", str(str(equipos).split(",")[1]),
                                "Puntuacion"]
        for x in range(0, typewar):
            test.append([str(jugadores1[x]), str(puntuaciones1[x]), str(jugadores2[x]), str(puntuaciones2[x])])
            table.append_row([str(jugadores1[x]), str(puntuaciones1[x]), str(jugadores2[x]), str(puntuaciones2[x])])
        test.append(["Total", sum1, "Total", sum2])
        table.append_row(["Total", sum1, "Total", sum2])
        if (sum1 < sum2):
            table.append_row(["Derrota por", str(sum1 - sum2), "Victoria de", "+" + str(sum2 - sum1)])
            test.append(["Derrota por", str(sum1 - sum2), "Victoria de", "+" + str(sum2 - sum1)])
        elif (sum1 == sum2):
            table.append_row(["Empate!", 0, "Empate!", 0])
            test.append(["Empate!", 0, "Empate!", 0])
        else:
            table.append_row(["Victoria de", "+" + str(sum1 - sum2), "Derrota por", str(sum2 - sum1)])
            test.append(["Victoria de", "+" + str(sum1 - sum2), "Derrota por", str(sum2 - sum1)])
        return test
    return


def addwar(IDs):
    global war_list
    for x, y, r, t in war_list:
        if str(IDs) == x:
            return True
    war_list.append([str(IDs), 0, 0, 0])
    return False


def existwar(IDs):
    global war_list
    for x, y, r, t in war_list:
        if str(IDs) == x:
            return True
    return False


def deletewar(IDs):
    global war_list
    count = 0
    for x, y, r, t in war_list:
        if str(IDs) == x:
            war_list.pop(count)
            return True
        count = count + 1
    return False

def savehtml(vec):
    html = '<style>#customer {background: url("tabla1.png")'
    html +='no-repeat;border-collapse: collapse;width:1000px;height:563px;text-align: center;}#customer th,#customer td {border: 1px solid black;}#customer tr:nth-child(2){color: #DAA520;}#customer tr:nth-child(3){color: #C0C0C0;}#customer tr:nth-child(4){color: #B87333;}</style>'
    html += '<table id="customer">'
    html += "<tr>"
    html += "<td>Fecha</td>"
    html += "<td>Jugador</td>"
    html += "<td>Equipo</td>"
    html += "<td>Tiempo</td>"
    html += "</tr>"
    for x in range(0, len(vec)):
        html += "<tr>"
        html += "<td>" + str(vec[x][0]) + "</td>"
        html += "<td>" + str(vec[x][1]) + "</td>"
        html += "<td>" + str(vec[x][2]) + "</td>"
        html += "<td>" + str(vec[x][3]) + "</td>"
        html += "</tr>"
    html += "</table>"

    with open("Tablita.html", "w") as text_file:
        print(html, file=text_file)
    return html

def savehtmltable(vec):
    html = '<style>#customer {background: url("tabla2.png")'
    html += 'no-repeat;border-collapse: collapse;color: white;width:1024px;height:576px;text-align: center;}#customer th {color: white;},#customer td {border: 1px white;color: white;}</style>'
    html += '<table id="customer">'
    for x in range(0, len(vec)):
        html += "<tr>"
        html += "<td>" + str(vec[x][0]) + "</td>"
        html += "<td>" + str(vec[x][1]) + "</td>"
        html += "<td>" + str(vec[x][2]) + "</td>"
        html += "<td>" + str(vec[x][3]) + "</td>"
        html += "</tr>"
    html += "</table>"

    with open("Tablitatabla.html", "w") as text_file:
        print(html, file=text_file)
    options = {
        'xvfb': ''
    }

    imgkit.from_file('Tablitatabla.html', 'Tablitatabla.jpg', options=options)
    return

def mostrartablaTTindiv():
    scope = ['https://spreadsheets.google.com/feeds']
    credentials = ServiceAccountCredentials.from_json_keyfile_name('CEMK-0ed44d25f869.json', scope)
    gc = gspread.authorize(credentials)
    wks = gc.open("TTMontewario").sheet1
    val = wks.get_all_values()
    val.sort(key=lambda x: x[3])

    table = BeautifulTable()
    table.column_headers = ["Fecha", "Jugador", "Equipo", "Tiempo"]
    jugadores = []
    tablita = []
    for x in range(0, len(val) - 1):
        if not str(val[x][1]) in jugadores:
            tablita.append([str(val[x][0]), str(val[x][1]), str(val[x][2]), cargar(val[x][3])])
            jugadores.append(str(val[x][1]))
    savehtml(tablita)
    options = {
        'xvfb': ''
    }

    imgkit.from_file('Tablita.html', 'Tablita.jpg', options=options)


def mostrartablaTTgrupo():
    teams = []
    jugadores=[]
    scope = ['https://spreadsheets.google.com/feeds']
    credentials = ServiceAccountCredentials.from_json_keyfile_name('CEMK-0ed44d25f869.json', scope)
    gc = gspread.authorize(credentials)
    wks = gc.open("TTMontewario").sheet1
    val = wks.get_all_values()
    val.sort(key=lambda x: x[3])

    table = BeautifulTable()
    table.column_headers = ["Equipo", "Tiempo"]
    for x in range(0, len(val) - 1):
        if not str(val[x][2]) in [x[0] for x in teams]:
            teams.append([str(val[x][2]), int(val[x][3]), 0])
            jugadores.append(str(val[x][1]))
        else:
            indice = [x[0] for x in teams].index(str(val[x][2]))
            if (teams[indice][2] < 2 and not str(val[x][1]) in jugadores):
                entero = int(teams[indice][1])
                teams[indice][1] = sumatiempos(entero, val[x][3])
                teams[indice][2] += 1
                jugadores.append(str(val[x][1]))
    print (teams)
    teams.sort(key=lambda x: x[1])
    for x in range(0, len(teams)):
        table.append_row([str(teams[x][0]),str(cargar(teams[x][1]))])
    return table
# Pre: War exists
# Post: Returns the sum of the war IDs

def getindexwar(IDs):
    count = 0
    global war_list
    for x, y, r, t in war_list:
        if str(IDs) == x:
            return count
        count += 1
    return 0


@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print('------')

@client.event
async def on_message(message):
    global number_list
    global welcius
    global race
    global LU
    global war_list
    global maintenance
    await client.change_presence(game=discord.Game(name='Marrec Menut'))
    if any(message.content.startswith(word) for word in number_list):
        id = message.channel.name
        war = existwar(id)
        if war == True:
            ind = getindexwar(id)
            tupla = war_list[ind]
            typewar = tupla[3]
            race = tupla[2]
            sum = tupla[1]
            arrmess = str(message.content).split(",")
            arrmess[0] = arrmess[0].split("!")[1]
            if typewar == 0:
                typewar = len(arrmess)
            elif typewar != len(arrmess):
                await client.send_message(message.channel, "Review number of players")
                return
            if len(arrmess) > 6:
                await client.send_message(message.channel, "More players than needed soz")
            else:
                total = []
                table = []
                if typewar == 5:
                    total = total_5
                    table = table_5
                elif typewar == 6:
                    total = total_6
                    table = table_6
                elif typewar == 4:
                    total = total_4
                    table = table_4
                tempo = 0
                repes = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
                for x in range(0, typewar):
                    if (int(arrmess[x]) <= 0):
                        await client.send_message(message.channel, "Don't put negative positions")
                        return
                    if (int(arrmess[x]) > typewar * 2) and typewar < 7:
                        await client.send_message(message.channel,
                                                  "Por favor, ¿tan malo eres que acabaste peor que el ultimo?")
                        return
                    if repes[int(arrmess[x]) - 1] == 1:
                        await client.send_message(message.channel, "Please retard, dont repeat positions")
                        return
                    tempo = tempo + table[int(arrmess[x]) - 1]
                    repes[int(arrmess[x]) - 1] = 1
                sum = sum + (tempo - (total - tempo))
                race += 1
                await client.send_message(message.channel, "Carrera número " + str(race))
                print(message.author)
                if (tempo - (total - tempo)) < 0:
                    await client.send_message(message.channel,
                                              "Resultados de la carrera " + str(tempo - (total - tempo)))
                    await client.send_message(message.channel, "Resultados totales " + str(sum))
                else:
                    await client.send_message(message.channel,
                                              "Resultados de la carrera " + str(tempo - (total - tempo)))
                    await client.send_message(message.channel, "Resultados totales " + str(sum))
                war_list[ind][1] = sum
                war_list[ind][2] = race
                war_list[ind][3] = typewar
        else:
            await client.send_message(message.channel, "No hay war empezada, empieza una")
    elif message.content.startswith('_help'):
        await client.send_message(message.channel,
                                  "Hi this is a war bot, here you have the available public commands for version 1.0 : ")
        await client.send_message(message.channel, "1. _startwar : Starts a war")
        await client.send_message(message.channel, "2. _stopwar : Stops the war")
        await client.send_message(message.channel, "3. _warstatus : Current punctuation of the war")
        await client.send_message(message.channel, "4. _listwars : Current active wars")
        await client.send_message(message.channel,
                                  "5. _war X: You want to war so your mates need to be notificate. The number is optional and would be a 6 if you are searching a 6v6")
        await client.send_message(message.channel, "6. _author : Gumer")
        await client.send_message(message.channel, "7. _maintenance : When is the next maintenance for upgrading")
        await client.send_message(message.channel, "8. _createtable : For creating war tables")
    elif message.content.startswith('_maintenance'):
        await client.send_message(message.channel, maintenance)
    elif message.content.startswith('_maintenancefx'):

        await client.send_message(message.channel, "Write when you want the maintenance to be planned")
        maintenance = await client.wait_for_message(author=message.author)
    elif message.content.startswith('_warstatus'):
        id = message.channel.name
        war = existwar(id)
        if war == True:
            ind = getindexwar(id)
            sum = war_list[ind][1]
            if (sum >= 0 and sum < 100):
                await client.send_message(message.channel, 'Winning by  ' + str(sum))
            elif (sum > 200):
                await client.send_message(message.channel, 'Winning by  ' + str(sum))
                await client.send_message(message.channel, 'Sure its versus DOEUF')
            elif (sum > 100):
                await client.send_message(message.channel, 'Winning by ' + str(sum))
                await client.send_message(message.channel, 'Welcius is not playing, right?')
            else:
                await client.send_message(message.channel, 'Losing by ' + str(sum))
                if (sum < -200):
                    await client.send_message(message.channel, 'Retire for life...')
                elif (sum < -150):
                    await client.send_message(message.channel, 'Are you FE?...')
                elif (sum < -100):
                    await client.send_message(message.channel, 'Que puto paquetes perdiendo de tanto')
                else:
                    await client.send_message(message.channel, 'Come on!')
        else:
            await client.send_message(message.channel, "There's no started war")

    elif message.content.startswith('_startwar'):
        id = message.channel.name
        war = addwar(id)
        if war == True:
            await client.send_message(message.channel, "There's already a war, tolai. Are you fucking blind?")
        else:
            await client.send_message(message.channel, "You have just started a war")
            await client.send_message(message.channel,
                                      "Remember that positions list must start with !, example: !1,2,3,4,5,6 ok no, we are not severance")
    elif message.content.startswith('_stopwar'):
        id = message.channel.name
        war = existwar(id)
        if war == True:
            ind = getindexwar(id)
            sum = war_list[ind][1]
            deletewar(id)
            if (sum < 0):
                await client.send_message(message.channel, "The war finished " + str(sum))
            else:
                await client.send_message(message.channel, "The war finished " + str(sum))
        else:
            await client.send_message(message.channel, "There's no active war, retard")

    elif message.content.startswith('_author'):
        if str(message.author) == "gumer#5813":
            await client.send_message(message.channel, "You are my author, my sir Gumer")
        else:
            await client.send_message(message.channel, "My author is Gumer")

    elif message.content.startswith('_war'):
        await client.send_message(message.channel, str(message.author) + " wants war @here")

    elif message.content.startswith('_starwar'):
        await client.send_message(message.channel, "Write it right, retard")
    elif message.content.startswith('Hola a todos'):
        await client.send_message(message.channel, ":-P Hola " + message.author.mention)
    elif message.content.startswith('_listwars'):
        counter = 1
        if len(war_list) != 0:
            for x, y, r, t in war_list:
                await client.send_message(message.channel, str(counter) + ".  " + x)
                counter += 1
        else:
            await client.send_message(message.channel, "No active wars")
    elif message.content.startswith('LU?'):
        if len(LU) == 0:
            await client.send_message(message.channel, "El lider no ha configurado la LU aun ")
            return
        await client.send_message(message.channel, "La LU de la war es: ")
        for x in range(0, len(LU)):
            await client.send_message(message.channel, LU[x] + ", ")

    elif message.content.startswith('addLU'):
        if str(message.author) == "gumer#5813":
            await client.send_message(message.channel, "Introduce el nombre del jugador a añadir")
            msg = await client.wait_for_message(author=message.author)
            LU.append(str(msg.content))
            await client.send_message(message.channel, str(msg.content) + "  Añadido a la LU")
        else:
            await client.send_message(message.channel, "No tienes derechos para añadir a la LU")

    elif message.content.startswith('clearLU'):
        if str(message.author) == "gumer#5813":
            LU = []
            await client.send_message(message.channel, "LU vaciada")
    elif message.content.startswith('_createtable'):
        await client.send_message(message.channel, 'Cuantos jugadores tiene tu equipo?')
        numerowar = await client.wait_for_message(author=message.author)
        await client.send_message(message.channel, 'Introduce los dos equipos separados por una coma')
        equipos = await client.wait_for_message(author=message.author)
        await client.send_message(message.channel, 'Introduce jugador,puntuacion,siguientejugador,puntuacion...primero los del primer equipo y luego los del otro')
        puntuaciones = await client.wait_for_message(author=message.author)
        vec= creadortablas(equipos.content, puntuaciones.content, int(numerowar.content))
        savehtmltable(vec)
        with open('Tablitatabla.jpg', 'rb') as f:
            await client.send_file(message.channel, f)
    elif message.content.startswith('_creartabla'):
        await client.send_message(message.channel, 'Cuantos jugadores tiene tu equipo?')
        numerowar = await client.wait_for_message(author=message.author)
        await client.send_message(message.channel, 'Introduce los dos equipos separados por una coma')
        equipos = await client.wait_for_message(author=message.author)
        await client.send_message(message.channel,'Introduce jugador,puntuacion,siguientejugador,puntuacion...primero los del primer equipo y luego los del otro')
        puntuaciones = await client.wait_for_message(author=message.author)
        welcius=True
        creadortablas(equipos.content, puntuaciones.content, int(numerowar.content))
        with open('Tablitatabla2.jpg', 'rb') as f:
            await client.send_file(message.channel, f)
        welcius = False
    elif message.content.startswith('Adiós'):
        if str(message.author) == "Millán#0171":
            await client.send_message(message.channel, "Adiosito " + message.author.mention + " por fin te vas, paquete. Estabas mejor en GM (Cuando estaba vivo)")
        elif str(message.author) == "Hernán#5166":
            await client.send_message(message.channel, "Adios " + message.author.mention + " zumito")
        elif str(message.author) == "Jumo#4236":
            await client.send_message(message.channel, "Adiosito " + message.author.mention + " Hernán. Recuerda, siempre estarás por debajo de Millán")
        else: await client.send_message(message.channel, "Adiosito " + message.author.mention + " por fin te vas, paquete")
    #TORNEO TT
    elif message.content.startswith('_listaTT'):
        await client.send_message(message.channel, "GBA CIRCUITO MARIO SEMANA 3")
        await client.send_message(message.channel, "Clasificación Grupos")
        await client.send_message(message.channel, mostrartablaTTgrupo())
        await client.send_message(message.channel, "Clasificación individual")
        mostrartablaTTindiv()
        with open('Tablita.jpg', 'rb') as f:
            await client.send_file(message.channel, f)
    elif message.content.startswith('_splits'):
        await client.send_message(message.channel, "Nombre del jugador")
        nick = await client.wait_for_message(author=message.author)
        url=mostrarimagen(nick.content)
        await client.send_message(message.channel, url)

client.run('')
