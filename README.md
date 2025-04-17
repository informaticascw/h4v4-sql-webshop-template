# h4v4-sql-webshop-template
Startcode voor het programmeren van een webshop met een html front end en python en database backend met rest api

Deze repo is onderdeel van het vak informatica op het Stanislascollege Westplantsoen.

Meer info over deze opdracht op [https://stanislas.informatica.nu](https://stanislas.informatica.nu/)

## Snel bekijken?

[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/informaticascw/h4v4-sql-webshop-template?quickstart=1

Start de webshop in de terminal van de Codespace met het commando 
```
bash start.sh
```

# Wat kan onze webshop
Wat heeft de webshop wel:
- Artikelen tonen
- Filteren van artikelen
- Zeer basic bestelproces (mailen wat je wilt kopen)

Wat heeft de webshop niet:
- Een winkelmand functie 
<br>(in plaats daarvan stuurt de klant een mailtje)
- Betaal functie 
<br>(in plaats daarvan stuurt webshop eigenaar een Tikkie)
- Inlog functie 
<br>(we schrijven niet in de database, dus dit is niet nodig) 
- Webpagina voor beheerder 
<br>(je moet de producten in je webshop aanpassen met sql opdrachten en dan de webshop herstarten)
- Voorraad en klantgegevens bijhouden

Hosting:

Onze webshop draait in een devcontainer op Codespaces. Dat betekent dat de webshop uitgaat als jij je browser afsluit. Je hebt een server nodig om je webshop permanent beschikbaar te maken, dat kost meestal een klein bedrag per maand en het vraagt wat technische handigheid om de webshop op de server te installeren.

# Basis uitleg hoe de webshop werkt
The basic idea is that a webpage of the shop is loaded by the browser and information on the articles in the shop are added to that depending on what the user selects.

1. You open a browser and navigate to the webshop. 
2. The browser downloads the html and css files from the server. It also downloads a piece of javascript code.
3. The javascript code is being executed by the browser. The javascript code connects to a link on the server that is connected to the api. This is called a REST-interface. Through the REST interface, the javascript code in the browser request information on the articles it needs to display.
4. The api is a programm on the server which connects to the database. It requests information from the database and sends it back to the browser. The result is sent in json-format.
5. The javascript programm in the browser looks at the json-file and adds elements containing articels in the shop to the DOM. The DOM is the model of the html files that the browser keeps in it memory and shows to the user. These elements added are displayed by the browser.

An alternative approach would be to have the server build complete web-pages including all information on articles. This is the idea behind the php programming language. The REST-interface is gaining popularity. An advantage of REST above php is that REST allows for more responsive (interfactive) websites.

# Uitleg hoe je de webshop kunt aanpassen 

## Server opnieuw starten
Gebruik het terminal window van Gitpod of Codespaces.<br>
Stop de server door typen van [CRTL]+[C].<br>
Start de server met het volgene commando.<br>
```
bash start.sh
```
Om de server te (her)starten kun je ook de start knop gebruiken die je ziet als je op het "run en debug" icoon in de iconenbalk links op het scherm drukt.

## Wijzigingen aanbrengen in de database
Wijzig de sql-commando's in het bestand db/create.sql<br>
Start de server opnieuw (zie elders hoe dat moet) nadat de sql-commando's gewijzigd zijn. Zo zorg je ervoor dat de database opnieuw gemaakt wordt door de nieuwe sql-commando's uit te voeren.

## Fouten zoeken in de database
Open de database in de terminal met het volgende commando
```
sqlite3 db/my.db
```
Je kunt met SQL commanda's zien wat er in de database staat.<br>
Bijvoorbeeld het commando: `SELECT * from Products;` (vergeet de ; aan het einde niet)

Meer handige commando's:<br>
- Een lijstje met tabellen `.tables`
- De namen van de kolommen in de tabel products: `.schema products`
- De eerste 3 rijen van de tabel products: `SELECT * FROM products LIMIT 3;`
- sqlite3 afsluiten: `.quit`

## Fouten zoeken in de api
Je kunt het antwoord van de api testen door achter de link naar je webshop /api/products te typen, bijvoorbeeld:<br>
`https://....-8080.app.github.dev/api/products` (voor codespaces, pas aan voor jouw webshop-adres)

Bekijk de terminal van de server, daar kun je foutmeldingen zien.
Je kunt in de code in de map api opdrachten toevoegen die inhoud van variabelen afdrukken. Bijvoorbeeld:
```
console.log("Waarde van i is ", i);
```
Start de server opnieuw (zie elders hoe dat moet) nadat de code gewijzigd is.

## Fouten zoeken in de webpages
Bekijk de console in de browser, daar kun je foutmeldingen zien.<br>
In Chrome open je de console in het menu -> Weergave -> Ontwikkelaar -> JavaScript-console. <br>
Je kunt in de code op strategische plaatsen de volgende opdracht toevoegen:
```
debugger
```
Als de console open staat dan stopt de browser met het uitvoeren van code als hij het debugger commando tegenkomt. Je kunt dan via de console opdrachten geven. Je kunt de inhoud van variabelen bekijken met de opdracht:
```
console.log("Waarde van i is ", i);
```

# Uitleg over bestanden en mappen

## data folder
Database with information on the arcticles in the shop. The commands in the init.sql file build te database. The database is build everytime start.sh is executed. 

## static folder
Static (non changing) html, css en js files. <br>
Images of products are located in a subfolder

## app folder
python file that starts webserver for static files and api.

## start.sh
Dit bestand bevat de commando's om de webshop (opnieuw) te starten. Je voert dit bestand uit in de terminal met het commando
```
bash start.sh
```

## .devcontainer 
Mappen met de configuratie voor Codespaces

## .vscode folder
Map met de configuratie voor de editor VS Code die wordt gebruikt door Gitpod en Codespaces

# Vraag en antwoord

## Codespace meldt "Oh no, it looks like you're offline"
Op sommige scholen blokkeert de firewall het gebruik van Codespaces. Dit is een instelling die alleen door de firewall beheerder kan worden aangepast. Tijdelijke oplossing: Verbind via een hotspot van je mobiel.

# Documentatie 
* Video over de werking van RESTful API's<br>
https://www.youtube.com/watch?v=-mN3VyJuCjM



* tutorial building a REST-api with postgressDB + jsnode + jsexpress<br>
https://blog.logrocket.com/setting-up-a-restful-api-with-node-js-and-postgresql-d96d6fc892d8/
* serving static files with jsexpress<br>
https://expressjs.com/en/starter/static-files.html
* basic html & css & javascript reference<br>
https://www.w3schools.com
* basic sql course<br>
https://www.khanacademy.org/computing/computer-programming/sql
* sqlite3 gebruiken op in Shell<br>
https://www.sqlite.org/cli.html
* better-sqlite library gebruiken in nodejs (javascript)<br>
https://github.com/JoshuaWise/better-sqlite3/blob/HEAD/docs/api.md
* shoppping basket lokaal opslaan<br>
google op local storage javascript basket
* bestelling mailen<br>
video met gebruik van nodemailer (module in javascript) vind je hier: https://youtu.be/Va9UKGs1bwI
* replit online editor en hosting ontwikkelomgeving<br>
https://docs.replit.com/
* gitpod online editor en hosting ontwikkelomgeving<br>
https://www.gitpod.io/docs/
* introduction to docker (kennis alleen nodig als je de repo heftig wilt aanpassen)<br>
https://docker-curriculum.com
* yarn (kennis alleen nodig als je de repo heftig wilt aanpassen)<br>
https://yarnpkg.com/getting-started

# Credits
- avs123a<br>
for a "Simple inventory list example with crud using : NodeJS, express framework, pug template, sqlite database and bootstrap". See https://github.com/avs123a/NodeJS-simple-example
- Robert Bakker [Notalifeform](https://www.gihub.com/Notalifeform)<br>
for help almost 24x7 with many questions and problems and providing basic shop called gitpodnode to be further developed by students on gitpod and deplyed freely on heroku. See https://gitpod.io/#https://github.com/Notalifeform/gitpodnode
- chatgpt for help converting the original idea (based on nodejs) to this idea (based on python)

