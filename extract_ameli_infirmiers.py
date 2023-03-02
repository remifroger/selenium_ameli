# -*- coding: utf-8 -*-

'''
Extraction de l'annuaire Ameli adaptable pour toute recherche (ici sur les infirmiers sur tous les codes postaux)
Les résultats de recherche sont limités à 1000 résultats (20 rés. par page) d'où l'intérêt de boucler sur les codes postaux (car pas de code postal ayant plus de 1000 résultats)
Au bout d'un certain nombre de requêtes, le serveur du site renvoie une page d'erreur 'The requested URL is rejected (...)' qui est géré par ce programme en fermant la page et en relançant le code sur le dernier code postal interrogé
A terme, cette erreur peut évoluer et le serveur d'Ameli peut s'équiper de programmes plus sophistiqués
Installation au préalable de Python 2.7+, Mozilla Firefox et de Geckodriver
'''

import os, sys
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
import time
import re
#from bs4 import BeautifulSoup
import pandas as pd
import unicodedata
import numpy
from fake_useragent import UserAgent

# création de la classe infirmière avec les attributs d'export
class infirmiere(object):
    def __init__(self, nom, adr, cv, tel):
        self.nom = nom
        self.adr = adr
        self.cv = cv
        self.tel = tel

# on pilote sur Ameli avec Selenium et Firefox
# il faut au préalable installer Geckodriver dans une version compatible à Firefox et Selenium puis le mettre dans le PATH

# fonction pour paramétrer la page d'accueil jusqu'au remplissage de la recherche d'adresse (qu'on va ensuite alimenter avec la liste des codes postaux)
# on retourne le driver et le dernier clique
def scrappe():
    useragent = UserAgent()
    profile = webdriver.FirefoxProfile()
    profile.set_preference("general.useragent.override", useragent.random)    
    driver = webdriver.Firefox(firefox_profile=profile)    
    driver.get("http://annuairesante.ameli.fr/")
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "buttonPS"))).click()
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "a.popin-autocomplete-ps-professions.popin-autocomplete-enable"))).click()
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.LINK_TEXT, "Infirmier"))).click()
    a = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "formProximite"))).click()
    return a, driver

# on lance la fonction scrappe() (2 variables car 2 return)
elt, driver = scrappe()
# on initialise le code postal de départ de la boucle
current_cp = "50000"
# liste des codes postaux sur laquelle on va boucler
cp = ["50000","50100","50110","50120","50130","50140","50150","50160","50170","50180","50190","50200","50210","50220","50230","50240","50250","50260","50270","50290","50300","50310","50320","50330","50340","50350","50360","50370","50380","50390","50400","50410","50420","50430","50440","50450","50460","50470","50480","50490","50500","50510","50520","50530","50540","50550","50560","50570","50580","50590","50600","50610","50620","50630","50640","50660","50670","50680","50690","50700","50710","50720","50730","50740","50750","50760","50770","50800","50810","50840","50850","50860","50870","50880","50890","51000","51100","51110","51120","51130","51140","51150","51160","51170","51190","51200","51210","51220","51230","51240","51250","51260","51270","51290","51300","51310","51320","51330","51340","51350","51360","51370","51380","51390","51400","51420","51430","51450","51460","51470","51480","51490","51500","51510","51520","51530","51600","51700","51800","52000","52100","52110","52120","52130","52140","52150","52160","52170","52190","52200","52210","52220","52230","52240","52250","52260","52270","52290","52300","52310","52320","52330","52340","52360","52370","52400","52410","52500","52600","52700","52800","53000","53100","53110","53120","53140","53150","53160","53170","53190","53200","53210","53220","53230","53240","53250","53260","53270","53290","53300","53320","53340","53350","53360","53370","53380","53390","53400","53410","53420","53440","53470","53480","53500","53540","53600","53640","53700","53800","53810","53940","53950","53960","53970","54000","54100","54110","54111","54112","54113","54114","54115","54116","54118","54119","54120","54121","54122","54123","54129","54130","54134","54135","54136","54140","54150","54160","54170","54180","54190","54200","54210","54220","54230","54240","54250","54260","54270","54280","54290","54300","54310","54320","54330","54340","54350","54360","54370","54380","54385","54390","54400","54410","54420","54425","54430","54440","54450","54460","54470","54480","54490","54500","54510","54520","54530","54540","54550","54560","54570","54580","54590","54600","54610","54620","54630","54640","54650","54660","54670","54680","54690","54700","54710","54720","54730","54740","54750","54760","54770","54780","54790","54800","54810","54820","54830","54840","54850","54860","54870","54880","54890","54910","54920","54930","54940","54950","54960","54970","54980","54990","55000","55100","55110","55120","55130","55140","55150","55160","55170","55190","55200","55210","55220","55230","55240","55250","55260","55270","55290","55300","55310","55320","55400","55430","55500","55600","55700","55800","55840","56000","56100","56110","56120","56130","56140","56150","56160","56170","56190","56200","56220","56230","56240","56250","56260","56270","56290","56300","56310","56320","56330","56340","56350","56360","56370","56380","56390","56400","56410","56420","56430","56440","56450","56460","56470","56480","56490","56500","56510","56520","56530","56540","56550","56560","56570","56580","56590","56600","56610","56620","56630","56640","56650","56660","56670","56680","56690","56700","56730","56740","56750","56760","56770","56780","56800","56840","56850","56860","56870","56880","56890","56910","56920","56930","56950","57000","57050","57070","57100","57120","57130","57140","57150","57155","57160","57170","57175","57180","57185","57190","57200","57220","57230","57240","57245","57250","57255","57260","57270","57280","57290","57300","57310","57320","57330","57340","57350","57360","57365","57370","57380","57385","57390","57400","57405","57410","57412","57415","57420","57430","57440","57445","57450","57455","57460","57470","57480","57490","57500","57510","57515","57520","57525","57530","57535","57540","57550","57560","57565","57570","57580","57590","57600","57620","57630","57635","57640","57645","57650","57655","57660","57670","57680","57685","57690","57700","57710","57720","57730","57740","57770","57780","57790","57800","57810","57815","57820","57830","57840","57850","57855","57860","57865","57870","57880","57890","57905","57910","57915","57920","57925","57930","57935","57940","57950","57960","57970","57980","57990","97100","97110","97111","97112","97113","97114","97115","97116","97117","97118","97119","97120","97121","97122","97123","97125","97126","97127","97128","97129","97130","97131","97133","97134","97136","97137","97139","97140","97141","97142","97150","97160","97170","97180","97190","97200","97211","97212","97213","97214","97215","97216","97217","97218","97220","97221","97222","97223","97224","97225","97226","97227","97228","97229","97230","97231","97232","97233","97234","97240","97250","97260","97270","97280","97290","97300","97310","97311","97312","97313","97314","97315","97316","97317","97318","97319","97320","97330","97340","97350","97351","97352","97353","97354","97355","97356","97360","97370","97380","97390","97400","97410","97411","97412","97413","97414","97416","97417","97418","97419","97420","97421","97422","97423","97424","97425","97426","97427","97429","97430","97431","97432","97433","97434","97435","97436","97437","97438","97439","97440","97441","97442","97450","97460","97470","97480","97490","97500","97600","97605","97615","97620","97625","97630","97640","97650","97660","97670","97680","98000","98600","98610","98620","98701","98703","98704","98705","98706","98707","98708","98709","98710","98711","98712","98714","98716","98718","98719","98720","98721","98722","98723","98724","98725","98726","98727","98728","98729","98730","98731","98732","98733","98734","98735","98740","98741","98742","98743","98744","98745","98746","98747","98748","98749","98750","98751","98752","98753","98754","98755","98760","98761","98762","98763","98764","98765","98766","98767","98768","98769","98770","98771","98772","98773","98774","98775","98776","98777","98778","98779","98780","98781","98782","98783","98784","98785","98786","98787","98788","98789","98790","98792","98793","98794","98795","98796","98799","98800","98809","98810","98811","98812","98813","98814","98815","98816","98817","98818","98819","98820","98821","98822","98823","98824","98825","98826","98827","98828","98829","98830","98831","98832","98833","98834","98835","98836","98837","98838","98839","98840","98850","98859","98860","98870","98874","98875","98876","98877","98878","98880","98881","98882","98883","98884","98885","98889","98890"]
# déclaration de la liste b qui reçoit le code source au fil de la boucle
b = []

# boucle sur chaque code postal pour remplir et lancer la rechercher, la boucle démarre à la valeur de current_cp
for val in cp[cp.index(current_cp):]:
    current_cp = val
    element1 = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "formOu")))
    element1.clear()
    element1.send_keys(val)
    dd = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.NAME, "submit_final"))).click()
    #dd.send_keys(webdriver.common.keys.Keys.ENTER)   
    
    try: 
        # on vérifie que l'entête soit présente pour continuer
        WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.ID, "entete")))
       
        while True:
        # tant que le bouton page suivante existe, on clique
            try:
                a = driver.page_source  
                b.append(str(a.encode("utf-8")))  
                with open("file_all.txt", "w") as output:
                    output.write(str(b))                 
                #WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "img[src*='/resources_ver/20170116185211/images/pagination_next.png']"))).click()
                elm = driver.find_element_by_css_selector("img[src*='/resources_ver/20170116185211/images/pagination_next.png']")
                elm.click()  
                time.sleep(3)
            except NoSuchElementException:
            # à la dernière page, on retourne sur la page de recherche
                driver.get("http://annuairesante.ameli.fr/modifier_votre_recherche_1.html")
                break
    except:
        # sinon on ferme le driver et on relance (permet de contourner la page d'erreur)
        driver.close()
        elt, driver = scrappe()

# on quitte le WebDriver
driver.quit()

# réouverture du texte stockant le code source
with open('file_all.txt', 'r') as myfile:
    exp = myfile.read().replace('\n', '')

# récupération d'une partie du code source    
expFiltre = re.findall('<div class="liste-professionnel">(.*?)<div id="bascadre">', str(exp))

list_inf = []

# boucle sur chaque bloc correspondant à un infirmier
for data in re.findall('<div class="item-professionnel">(.*?)<div class="clear"></div></div><div class="clear"></div></div>', str(expFiltre)):

    # nom et prénom
    if re.findall('.html">(.*?)</a></h2>', str(data)):
        s_nom_prenom = str(re.findall('.html">(.*?)</a></h2>', str(data))).strip('[]')
    else:
        s_nom_prenom = 'N'
    
    # adresse
    if re.findall('class="item left adresse">(.*?)</div>', str(data)):
        s_adresse = str(re.findall('class="item left adresse">(.*?)</div>', str(data))).strip('[]')
    else:
        s_adresse = 'N'
        
    # carte vitale
    if re.findall('<div class="pictos">(.*?)</div>', str(data)):
        s_carte_vitale = str(re.findall('<div class="pictos">(.*?)</div>', str(data))).strip('[]')
    else:
        s_carte_vitale = 'N'
        
    # téléphone
    if re.findall('tel', str(data)):
        s_tel = str(re.findall('tel">(.*?)</div>', str(data))).strip('[]')
    else:
        s_tel = 'N'
    
    # instanciation de l'objet
    inf = infirmiere(s_nom_prenom, s_adresse, s_carte_vitale, s_tel)
    list_inf.append(inf)

n = []
a = []
c = []
t = []

# alimentation des attributs de l'object
for i in list_inf:
    n.append(i.nom)
    a.append(i.adr)
    c.append(i.cv)
    t.append(i.tel)

# on récupère le tableau, transposition des lignes-colonnes et export en csv
ar = numpy.array([n, a, c, t])
u = ar.transpose()
df = pd.DataFrame(u, columns = ['nom_pren', 'adresse', 'carte_vit', 'tel'])
df.to_csv('extract_all.csv', sep=';', encoding='utf-8')