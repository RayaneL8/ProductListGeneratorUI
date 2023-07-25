import ipywidgets as widgets
import requests
import time
import csv
import pandas
import os
from IPython.display import display, HTML,clear_output

#CLE SECRETE D'ADMIN
SHARED_SECRET = os.environ.get('SHARED_SECRET')

#CLE API
API_KEY = os.environ.get('API_KEY')

#[ADRESSE] : Contient l'adresse de l'api pour récupérer une liste de produit
URL_PRODUCTS = "https://%s:%s@souk-dubai-1400.myshopify.com/admin/api/2023-01/products.json" % (API_KEY, SHARED_SECRET)

#[ADRESSE] : Contient l'adresse de l'api pour récupérer un produit en particulier
URL_PRODUCT = "https://%s:%s@souk-dubai-1400.myshopify.com/admin/api/2023-01/products/" % (API_KEY, SHARED_SECRET)

#[ADRESSE] : Contient l'adresse de l'api pour récupérer une liste de produit de la catégorie LIBRAIRIE
URL_PRODUCTS_LIB = "https://%s:%s@souk-dubai-1400.myshopify.com/admin/api/2023-01/collections/493328433420/products.json" % (API_KEY, SHARED_SECRET)

#[ADRESSE] : Contient l'adresse de l'api pour récupérer une liste de produit de la catégorie PARFUMERIE
URL_PRODUCTS_PARF = "https://%s:%s@souk-dubai-1400.myshopify.com/admin/api/2023-01/collections/493329023244/products.json" % (API_KEY, SHARED_SECRET)

#[ADRESSE] : Contient l'adresse de l'api pour récupérer une liste de produit de la catégorie PRET A PORTER MIXTE
URL_PRODUCTS_PAP = "https://%s:%s@souk-dubai-1400.myshopify.com/admin/api/2023-01/collections/493328564492/products.json" % (API_KEY, SHARED_SECRET)

#[ADRESSE] : Contient l'adresse de l'api pour récupérer une liste de produit de la catégorie PRET A PORTER HOMME
URL_PRODUCTS_PAPH = "https://%s:%s@souk-dubai-1400.myshopify.com/admin/api/2023-01/collections/493328630028/products.json" % (API_KEY, SHARED_SECRET)

#[ADRESSE] : Contient l'adresse de l'api pour récupérer une liste de produit de la catégorie PRET A PORTER FEMME
URL_PRODUCTS_PAPF = "https://%s:%s@souk-dubai-1400.myshopify.com/admin/api/2023-01/collections/493328597260/products.json" % (API_KEY, SHARED_SECRET)

#[CHEMIN] : Contient le chemin d'accès par défaut du DRIVE d'écriture des fichier
PATH_WRITE_DRIVE = "/content/drive/MyDrive/CodeRayane/LIST/"

global url, chemin
global selectedURL, selectedOption, selectedNumber, selectedGender, selectedSKU, withDraft, withDraftOnly

url = URL_PRODUCTS
chemin = ""
selectedURL = None
selectedOption = None
selectedNumber = 0
selectedGender = None
selectedSKU = None
withDraft = None
withDraftOnly = None

# Création du menu déroulant avec les options
dropdownURL = widgets.Dropdown(
    options=['TOUT', 'LIBRAIRIE', 'PARFUMERIE',"PRET A PORTER",],
    description='Selectionnez:',
)
dropdownOption = widgets.Dropdown(
    options=['STOCK',"STOCK EN DESSOUS", 'POIDS', 'DOUBLON PRIX','SKU','SAMESKU',],
    description='Selectionnez:',
)
dropdownGender = widgets.Dropdown(
    options=['MIXTE', 'HOMME', 'FEMME'],
    description='Selectionnez:',
)

# Création des inputs
text_inputNumber = widgets.IntText(description='Stock:')
text_inputSKU = widgets.IntText(description='SKU:')

# Création des checkbox
checkboxDraft = widgets.Checkbox(description='Avec ébauche')
checkboxDraftOnly = widgets.Checkbox(description='Uniquement ébauche')

# Création des boutons de confirmation
buttonConfirmerURL = widgets.Button(description='Confirmer')
buttonConfirmerOption = widgets.Button(description='Confirmer')
buttonConfirmerNumber = widgets.Button(description='Confirmer')
buttonConfirmerGender = widgets.Button(description='Confirmer')
buttonConfirmerSKU = widgets.Button(description='Confirmer')

def get_250_products(endpoint):
    global url
    r = requests.get(url+"?page_info="+endpoint+"&limit=250")
    return r

def rowAppend(p,pv,writer,count):
    global selectedOption
    row = []
    row.append(p['title'].ljust(30))
    print(p['title']+" \ ",end = "")
    if pv['title'] != "Default Title" and pv['title'] != "":
        row.append(pv['title'])
        print(pv['title'],end="")
    else:
        row.append(" ")
    if selectedOption == "STOCK" or selectedOption == "STOCK EN DESSOUS":
      print(" | STOCK = "+str(pv['inventory_quantity']))
      row.append(str(pv['inventory_quantity']))
    elif selectedOption == "POIDS" :
      print(" | POIDS = "+str(pv['weight'])+str(pv['weight_unit']))
      row.append(str(pv['weight'])+str(pv['weight_unit']))
    elif selectedOption == "DOUBLON PRIX":
      print(" | "+str(pv['price'])+" & "+str(pv['compare_at_price']))
      row.append(str(pv['price'])+" & "+str(pv['compare_at_price']))
    elif selectedOption == "SKU" or selectedOption == "SAMESKU":
      print(" | SKU = "+str(pv['sku']))
      row.append(" | SKU = "+str(pv['sku'])+"\n")
    writer.writerow(row)
    count = count + 1
    return count

def writeStock(p, pv, number, count,withDraft):
    with open(PATH_WRITE_DRIVE + chemin + ".csv", "a", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        if f.tell() == 0:
            writer.writerow(["Produits".ljust(30), "Variants", "Stock"])  # Écrire les en-têtes de colonne
        if (pv['inventory_quantity'] == number) :
            if withDraftOnly:
                if p['status'] == "draft":
                    count = rowAppend(p,pv,writer,count)
            elif not withDraft:
                if p['status'] == "active":
                    count = rowAppend(p,pv,writer,count)
            else:
                count = rowAppend(p,pv,writer,count)
    return count



def writeStockBellow(p, pv, number, count,withDraft):
    with open(PATH_WRITE_DRIVE + chemin + ".csv", "a", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        if f.tell() == 0:
            writer.writerow(["Produits", "Variants", "Stock"])  # Écrire les en-têtes de colonne
        if (pv['inventory_quantity'] <= number):
            if withDraftOnly:
                if p['status'] == "draft":
                    count = rowAppend(p,pv,writer,count)
            elif not withDraft:
                if p['status'] == "active":
                    count = rowAppend(p,pv,writer,count)
            else:
                count = rowAppend(p,pv,writer,count)
    return count

def writeWeight(p, pv, count,withDraft):
    with open(PATH_WRITE_DRIVE + chemin + ".csv", "a", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        if f.tell() == 0:
            writer.writerow(["Produits", "Variants", "Poids"])  # Écrire les en-têtes de colonne
        if pv['weight_unit'] != "g" and pv['weight'] >1:
            if withDraftOnly:
                if p['status'] == "draft":
                    count = rowAppend(p,pv,writer,count)
            elif not withDraft:
                if p['status'] == "active":
                    count = rowAppend(p,pv,writer,count)
            else:
                count = rowAppend(p,pv,writer,count)
    return count

def writeDoublePrice(p, pv, count,withDraft):
    with open(PATH_WRITE_DRIVE + chemin + ".csv", "a", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        if f.tell() == 0:
            writer.writerow(["Produits", "Variants", "Prix"])  # Écrire les en-têtes de colonne
        if (pv['compare_at_price'] == pv['price']):
            if withDraftOnly:
                if p['status'] == "draft":
                    count = rowAppend(p,pv,writer,count)
            elif not withDraft:
                if p['status'] == "active":
                    count = rowAppend(p,pv,writer,count)
            else:
                count = rowAppend(p,pv,writer,count)
    return count

def writeSKU(p, pv,sku, count,withDraft):
    with open(PATH_WRITE_DRIVE + chemin + ".csv", "a", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        if f.tell() == 0:
            writer.writerow(["Produits", "Variants", "SKU"])  # Écrire les en-têtes de colonne
        if pv['sku'] == sku:
            if withDraftOnly:
                if p['status'] == "draft":
                    count = rowAppend(p,pv,writer,count)
            elif not withDraft:
                if p['status'] == "active":
                    count = rowAppend(p,pv,writer,count)
            else:
                count = rowAppend(p,pv,writer,count)
    return count

def writeAllAux(products,count):
    global url,selectedOption,selectedNumber,selectedSKU,withDraft
    for p in products['products']:
        if url == URL_PRODUCTS:
            for pv in p['variants']:
                if selectedOption == "STOCK":
                    count = writeStock(p,pv,selectedNumber,count,withDraft)
                elif selectedOption == "STOCK EN DESSOUS":
                    count = writeStockBellow(p,pv,selectedNumber,count,withDraft)
                elif selectedOption == "POIDS":
                    count = writeWeight(p,pv,count,withDraft)
                elif selectedOption == "DOUBLON PRIX":
                    count = writeDoublePrice(p,pv,count,withDraft)
                elif selectedOption == "SKU":
                    count = writeSKU(p,pv,selectedSKU,count,withDraft)

        elif url != URL_PRODUCTS:
            id = p['id']
            time.sleep(0.4)
            r2 = requests.get(URL_PRODUCT+str(id)+".json",timeout=20).json()
            try:
                for pv2 in r2['product']['variants']:
                    if selectedOption == "STOCK":
                        count = writeStock(p,pv2,selectedNumber,count,withDraft)
                    elif selectedOption == "STOCK EN DESSOUS":
                        count = writeStockBellow(p,pv2,selectedNumber,count,withDraft)
                    elif selectedOption == "POIDS":
                        count = writeWeight(p,pv2,count,withDraft)
                    elif selectedOption == "DOUBLON PRIX":
                        count = writeDoublePrice(p,pv2,count,withDraft)
                    elif selectedOption == "SKU":
                        count = writeSKU(p,pv2,selectedSKU,count,withDraft)

            except:
                print(r2 + "Erreur de connexion")
    return count

def nbSameSKUaux(products,count,sku,r):
    try:
        if is_html(r.text):
            return count
        else:
            for p in products['products']:
                if url == URL_PRODUCTS:
                    for pv in p["variants"]:
                        if pv["sku"] == sku:
                            print(p['title']+" \ ",end = "")
                            if pv['title'] != "Default Title" or "":
                                print(pv['title'],end ="")
                            print(" | SKU = "+str(pv['sku']))
                            count = count+1
            else:
                id = p['id']
                time.sleep(0.4)
                r2 = requests.get(URL_PRODUCT+str(id)+".json",timeout=20).json()
                for pv2 in r2['product']['variants']:
                    print(sku,pv2['sku'])
                    if pv2["sku"] == sku:
                            print(p['title']+" \ ",end = "")
                            if pv2['title'] != "Default Title" or "":
                                print(pv2['title'],end ="")
                            print(" | SKU = "+str(pv2['sku']))
                            count = count+1

    except:
        print("KEY ERROR !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        print(r.text)
    return count

def nbSameSKU(sku):
    endpoint = ""
    end_while = 1
    count = 0
    while(end_while != -1):
        r = get_250_products(endpoint)
        if r.headers.get('Link') != None:
            if r.headers.get('Link').find('previous') == -1:
                fpage_info = r.headers.get('Link').find('page_info=')
                fpage_info_end = r.headers.get('Link').find('>')
            else :
                fpage_info = r.headers.get('Link').find('page_info=',r.headers.get('Link').find('previous'),r.headers.get('Link').find('next'))
                fpage_info_end = r.headers.get('Link').find('>',r.headers.get('Link').find('previous'))
            endpoint = r.headers.get('Link')[fpage_info+10:fpage_info_end]
            end_while = r.headers.get('Link').find('next')
            count = nbSameSKUaux(r.json(),count,sku,r)
        else:
            count = nbSameSKUaux(r.json(),count,sku,r)
            end_while = -1
    print("TOTAL = "+str(count))
    return count

def sameSKU():
    global url
    dictSKU = {}
    endpoint = ""
    end_while = 1
    while(end_while != -1):
        r = get_250_products(endpoint)
        if r.headers.get('Link') != None:
            if r.headers.get('Link').find('previous') == -1:
                fpage_info = r.headers.get('Link').find('page_info=')
                fpage_info_end = r.headers.get('Link').find('>')
            else :
                fpage_info = r.headers.get('Link').find('page_info=',r.headers.get('Link').find('previous'),r.headers.get('Link').find('next'))
                fpage_info_end = r.headers.get('Link').find('>',r.headers.get('Link').find('previous'))
            endpoint = r.headers.get('Link')[fpage_info+10:fpage_info_end]
            end_while = r.headers.get('Link').find('next')
            for p in r.json()["products"]:
                for pv in p["variants"]:
                    if pv["sku"] not in dictSKU:
                        temp = nbSameSKU(pv["sku"])
                        if temp >1:
                            dictSKU[pv["sku"]] = temp
                        print(dictSKU)
        else:
            for p in r.json()["products"]:
                if url == URL_PRODUCTS:
                    for pv in p["variants"]:
                        if pv["sku"] not in dictSKU:
                            temp = nbSameSKU(pv["sku"])
                            if temp >1:
                                dictSKU[pv["sku"]] = temp
                            print(dictSKU)
                else:
                    id = p['id']
                    time.sleep(0.4)
                    r2 = requests.get(URL_PRODUCT+str(id)+".json",timeout=20).json()
                    for pv2 in r2['product']['variants']:
                        if pv2["sku"] not in dictSKU:
                            temp = nbSameSKU(pv2["sku"])
                            if temp >1:
                                dictSKU[pv2["sku"]] = temp
                            print(dictSKU)
        print("FINIT")

def is_html(data):
    return data.startswith('<!DOCTYPE html>')

def convertCSVtoXLSX(csv_filename, xlsx_filename):
    df = pandas.read_csv(csv_filename)
    df.to_excel(xlsx_filename, index=False)

def writeAll():
    f = open(PATH_WRITE_DRIVE+chemin+".csv","w")
    f.close()
    endpoint = ""
    end_while = 1
    count = 0
    while(end_while != -1):
        r = get_250_products(endpoint)
        if r.headers.get('Link') != None:
            if r.headers.get('Link').find('previous') == -1:
                fpage_info = r.headers.get('Link').find('page_info=')
                fpage_info_end = r.headers.get('Link').find('>')
            else :
                fpage_info = r.headers.get('Link').find('page_info=',r.headers.get('Link').find('previous'),r.headers.get('Link').find('next'))
                fpage_info_end = r.headers.get('Link').find('>',r.headers.get('Link').find('previous'))
            endpoint = r.headers.get('Link')[fpage_info+10:fpage_info_end]
            end_while = r.headers.get('Link').find('next')
            count = writeAllAux(r.json(),count)
        else:
            count = writeAllAux(r.json(),count)
            end_while = -1
    with open(PATH_WRITE_DRIVE+chemin+".csv","a") as f:
        writer = csv.writer(f)
        writer.writerow(["TOTAL = "+str(count)])
    print("TOTAL = "+str(count))
    return "FINIT"



# Affiche le menu déroulant et le bouton
display(HTML("Choisissez la collection de produits"))
display(dropdownURL, buttonConfirmerURL)
display(checkboxDraft)
display(checkboxDraftOnly)

# Fonction appelée lorsque le bouton est cliqué
def on_buttonConfirmerURL_clicked(b):
    global selectedURL,url,chemin,withDraft,withDraftOnly
    if withDraft and withDraftOnly:
        chemin = "Ebauche_"
    elif withDraft and not withDraftOnly:
        chemin = "AvecEbauche_"
    elif not withDraft and withDraftOnly:
        chemin = "Ebauche_"
    selectedURL = dropdownURL.value
    if selectedURL == "TOUT":
        url = URL_PRODUCTS
        chemin = chemin +"TOUT"
    elif selectedURL == "LIBRAIRIE":
        url = URL_PRODUCTS_LIB
        chemin = chemin +"LIBRAIRIE"
    elif selectedURL == "PARFUMERIE":
        url = URL_PRODUCTS_PARF
        chemin = chemin+"PARFUMERIE"
    elif selectedURL == "PRET A PORTER":
        clear_output()
        chemin = chemin+"PRET_A_PORTER"
        display(dropdownGender,buttonConfirmerGender)
        return
    clear_output()
    display(HTML("Choisissez le type de vérification :</br>"))
    display(HTML("<strong>STOCK</strong> = Stock choisie (choisir 0 pour Rupture de Stock)</br>"))
    display(HTML("<strong>StockEnDessous</strong> = Stock en dessous du nombre choisie</br>"))
    display(HTML("<strong>POIDS</strong> = Poids incorrect</br>"))
    display(HTML("<strong>DOUBLONPRIX</strong> = Prix avant et après réduction similaire "))
    display(HTML("<strong>SKU</strong> = SKU similaire à celui choisie "))
    display(HTML("<strong>DOUBLONSKU</strong> = Produits avec le même SKU "))
    display(dropdownOption,buttonConfirmerOption)

    print(f"La valeur choisie est {selectedURL}\n L'URL est : {url}")

def on_buttonConfirmerOption_clicked(b):
    global selectedOption,chemin,END,inputNumber
    selectedOption = dropdownOption.value
    if selectedOption == "STOCK":
        clear_output()
        display(text_inputNumber,buttonConfirmerNumber)
        return
    elif selectedOption == "STOCK EN DESSOUS":
        clear_output()
        display(text_inputNumber,buttonConfirmerNumber)
        return
    elif selectedOption == "POIDS":
        chemin = chemin+"_POIDS_INCORRECT"
    elif selectedOption == "DOUBLON PRIX":
        chemin = chemin+"_DOUBLON_PRIX"
    elif selectedOption == "SKU":
        chemin = chemin+"_SKU"
        clear_output()
        display(text_inputSKU,buttonConfirmerSKU)
        return
    elif selectedOption == 'SAMESKU':
        clear_output()
        sameSKU()
        return
    clear_output()
    print(f"La valeur choisie est {selectedOption}\n")
    print(writeAll())

def on_buttonConfirmerNumber_clicked(b):
    global selectedNumber, chemin, selectedOption
    selectedNumber = int(text_inputNumber.value)
    if selectedOption == "STOCK":
        chemin = chemin+"_STOCK"
    if selectedOption == "STOCK EN DESSOUS":
        chemin = chemin +"_STOCK_EN_DESSOUS_DE"
    if selectedNumber == 0 and selectedOption == "STOCK":
        chemin = chemin+"_RUPTURE_DE_STOCK"
    else:
        chemin = chemin+"_"+str(selectedNumber)
    print(f"La valeur choisie est {selectedNumber}\n")
    print(writeAll())

def on_buttonConfirmerGender_clicked(b):
    global selectedGender, chemin,url
    selectedGender = dropdownGender.value
    if selectedGender == "MIXTE":
        url = URL_PRODUCTS_PAP
    elif selectedGender == "HOMME":
        url = URL_PRODUCTS_PAPH
        chemin = chemin + "_HOMME"
    elif selectedGender == "FEMME":
        url = URL_PRODUCTS_PAPF
        chemin = chemin + "_FEMME"
    clear_output()
    display(dropdownOption,buttonConfirmerOption)

def on_buttonConfirmerSKU_clicked(b):
    global selectedSKU,chemin,url
    selectedSKU = str(text_inputSKU.value)
    chemin = chemin+"_"+str(selectedSKU)
    print(f"La valeur choisie est {selectedSKU}\n")
    print(writeAll())

def checkbox_callbackDraft(change):
    global withDraft, chemin
    if change['new']:
        withDraft = True
    else:
        withDraft = False


def checkbox_callbackDraftOnly(change):
    global withDraftOnly, chemin
    if change['new']:
        withDraftOnly = True
    else:
        withDraftOnly = False

# Associe la fonction de rappel à l'événement "on_click" du bouton
buttonConfirmerURL.on_click(on_buttonConfirmerURL_clicked)
buttonConfirmerOption.on_click(on_buttonConfirmerOption_clicked)
buttonConfirmerNumber.on_click(on_buttonConfirmerNumber_clicked)
buttonConfirmerGender.on_click(on_buttonConfirmerGender_clicked)
buttonConfirmerSKU.on_click(on_buttonConfirmerSKU_clicked)
checkboxDraft.observe(checkbox_callbackDraft, 'value')
checkboxDraftOnly.observe(checkbox_callbackDraftOnly, 'value')


