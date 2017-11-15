import haravasto
from random import randint
import time


tila = {
	"kentta": None,
	"nakyvakentta": None,
	"liput": None,
	"miinat": None,
	"aloitus": None
}

def luo_kentta():
	"""Luo kentän käyttäjän antamien asetusten mukaan"""
	leveys, korkeus, maara = kysy_asetukset()
	print("Hiiren vasen aukaisee ruutuja, hiiren oikea asettaa lipun\nPeli päättyy, kun kaikkien miinojen paikalle on asetettu lippu")

	nakyvakentta = []
	kentta = []
	for rivi in range(korkeus):
		kentta.append([])
		nakyvakentta.append([])
		for sarake in range(leveys):
			kentta[-1].append(" ")
			nakyvakentta[-1].append(" ")
	tila["liput"] = []
	tila["nakyvakentta"] = nakyvakentta
	tila["kentta"] = kentta
	miinoita(kentta, maara)
	numeroi_ruudut(kentta)

def kysy_asetukset():
	"""Kysyy käyttäjältä asetukset ja tarkastaa ne"""
	print("Vaikeusasteet ovat Micro$oft Minesweeperin mukaiset ja näin ollen vaikuttavat kentän kokoon, sekä miinojen määrään\n")
	while True:
		try:	
			print("Valitse 1. jos haluat pelata helpolla vaikeusasteella\nValitse 2. jos haluat pelata keskivaikealla vaikeusasteella\nValitse 3. jos haluat pelata vaikeimmalla vaikeusasteella")
			print("Valitse 4. jos haluat päättää asetukset itse\n")
			valinta = int(input("Syötä valintasi: "))
			if valinta == 1:
				leveys = 8
				korkeus = 8
				maara = 10
				return leveys, korkeus, maara
			elif valinta == 2:
				leveys = 16
				korkeus = 16
				maara = 40
				return leveys, korkeus, maara
			elif valinta == 3:
				leveys = 24
				korkeus = 24
				maara = 99
				return leveys, korkeus, maara
			elif valinta == 4:
				leveys = int(input("Syötä kentän leveys kokonaislukuna: "))
				korkeus = int(input("Syötä kentän korkeus kokonaislukuna: "))
				maara = int(input("Syötä miinojen lukumäärä: "))
				if leveys < 1 or korkeus < 1 or maara > leveys*korkeus:
					print("Kenttä on liian pieni tai miinoja on enemmän kuin ruutuja.\n")
				else:
					return leveys, korkeus, maara
			else:
				print("Virheellinen valinta.\n")
		except ValueError:
			print("Syötä arvot kokonaislukuina\n")

def miinoita(kentta, maara):
	"""Asettaa kentällä N kpl miinoja satunnaisiin paikkoihin."""
	miinat = []
	for i in range(maara):
			x = randint(0, len(kentta) - 1)
			y = randint(0, len(kentta) - 1)
			if kentta[x][y] != "x":
				kentta[x][y] = "x"
				miinat.append((x, y))
	# Asettaa kentän tiedot kirjastoon
	tila["miinat"] = miinat
	tila["kentta"] = kentta

def numeroi_ruudut(kentta): 
	"""Muuttaa ruutujen arvot vastaamaan viereisten miinojen määrää"""
	for rivinro, rivi in enumerate(kentta):
		for sarakenro, sarake in enumerate(rivi):
			if sarake != "x":
				# Ottaa naapureiden arvot
				arvot = [kentta[r][s] for r, s in etsi_naapurit(rivinro, sarakenro)]
				# Laskee kuinka monta on miinoja
				if arvot.count("x") > 0:
					kentta[rivinro][sarakenro] = str(arvot.count("x"))
				else:
					kentta[rivinro][sarakenro] = "0"
	# Asettaa ruutujen numeroarvot kirjastoon
	tila["kentta"] = kentta

def etsi_naapurit(x, y):
	"""Etsii ruudun naapurit ja palauttaa ne"""
	leveys = len(tila["kentta"])
	korkeus = len(tila["kentta"][0])
	naapurit = []
	for nx in range(min(max(x-1, 0), leveys), min(max(x+2, 0), leveys)):
		for ny in range(min(max(y-1, 0), korkeus), min(max(y+2, 0), korkeus)):
				naapurit.append((nx, ny))
	return naapurit

def tulvataytto(x, y, tarkastettu=[]):
	"""Merkitsee kentällä olevat tuntemattomat alueet turvalliseksi siten, että täyttö aloitetaan annetusta x, y -pisteestä."""
	naapurit = etsi_naapurit(x, y)
	for x, y in naapurit:
		if (x, y) not in tarkastettu:
			tarkastettu.append((x, y))
			if tila["kentta"][x][y] != "x" and tila["nakyvakentta"][x][y] != "f":
				tila["nakyvakentta"][x][y] = tila["kentta"][x][y]

			if tila["kentta"][x][y] == "0":
				tulvataytto(x, y)


def tarkista_voitto(x, y):
	#tarkistaa onko liput samoissa paikoissa kuin miinat
	if set(tila["liput"]) == set(tila["miinat"]):
		print("Voitit pelin :)")
		print("Aikaa kului: {:.2f} sekunttia".format(lopeta_kello()))
		piirra_kentta()

def tarkista_havio(x, y):
	#tarkistaa onko painetussa kohdassa miina
	if tila["kentta"][x][y] == "x":
		print("Hävisit pelin :(")
		print("Aikaa kului: {:.2f} sekunttia".format(lopeta_kello()))
		tila["nakyvakentta"] = tila["kentta"]
		piirra_kentta()

def avaa_ruutu(x, y):
	tarkista_havio(x, y)
	#jos on lippu, poistaa sen
	if (x, y) == tila["liput"]:
		tila["liput"].remove((x, y))
		#näytä ruutu
		tila["nakyvakentta"][x][y] = tila["kentta"][x][y] 
		piirra_kentta()

	if tila["nakyvakentta"][x][y] == " ":
		if int(tila["kentta"][x][y]) > 0:
			tila["nakyvakentta"][x][y] = tila["kentta"][x][y] 
		if tila["kentta"][x][y] == "0":
			tulvataytto(x, y)
		piirra_kentta()


def aseta_lippu(x, y):
	# Tarkistaa onko ruutu tyhjä
	if tila["nakyvakentta"][x][y] == " ":
		tila["nakyvakentta"][x][y] = "f"
		tila["liput"].append((x, y))
		tarkista_voitto(x, y)
	# Poistaa lipun
	elif tila["nakyvakentta"][x][y] == "f":
		tila["nakyvakentta"][x][y] = " "
		tila["liput"].remove((x, y))
		print(tila["liput"])
	else:
		print("Ei voi asettaa lippua")

	piirra_kentta()

def aloita_kello():
	# Aloittaa pelin kulkua mittaavan sekunttikellon
	tila["aloitus"] = time.time()

def lopeta_kello():
	# Lopettaa pelin kulkua mittaavan sekunttikellon
	loppuaika = time.time()
	total = loppuaika - tila["aloitus"]
	return total

def hiiri_kasittelija(x, y, nappi, muokkausnapit):
	"""Tätä funktiota kutsutaan kun käyttäjä klikkaa sovellusikkunaa hiirellä."""
	x = int(x / 40)
	y = int(y / 40)
	if nappi == haravasto.HIIRI_VASEN:
		avaa_ruutu(x, y)
	elif nappi == haravasto.HIIRI_OIKEA:
		aseta_lippu(x, y)

def piirra_kentta(): 
	"""Käsittelijäfunktio, joka piirtää kaksiulotteisena listana kuvatun miinakentän ruudut näkyviin peli-ikkunaan.
	Funktiota kutsutaan aina kun pelimoottori pyytää ruudun näkymän päivitystä."""
	haravasto.tyhjaa_ikkuna()
	haravasto.piirra_tausta()
	haravasto.aloita_ruutujen_piirto()
	for x in range(len(tila["nakyvakentta"])):
		for y in range(len(tila["nakyvakentta"][0])):
				haravasto.lisaa_piirrettava_ruutu(tila["nakyvakentta"][x][y], x * 40, y * 40)
	haravasto.piirra_ruudut()

def main():
	luo_kentta()
	haravasto.lataa_kuvat("spritet")
	haravasto.luo_ikkuna(len(tila["nakyvakentta"] * 40), len(tila["nakyvakentta"][0] * 40))
	haravasto.aseta_piirto_kasittelija(piirra_kentta)
	haravasto.aseta_hiiri_kasittelija(hiiri_kasittelija)
	aloita_kello()
	haravasto.aloita()
if __name__ == "__main__":
	main()