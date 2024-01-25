# Sistemi za digitalnu obradu signala
## Dodavanje muzičkih efekata u audio signal korištenjem razvojnog okruženja ASDP-21489
Repozitorijum se sastoji od programa napisanog korištenjem Python programskog jezika, koji služi za učitavanje audio fajlova sa ekstenzijom .wav, implementaciju audio efekata i primjenjivanje na učitani audio signal, te generisanje modifikovanog audio fajla (direktorijum Python). Audio efekti su po istom principu implementirani u C programskom jeziku korištenjem CrossCore Embedded Studio razvojnog okruženja, a program je namijenjen za ADSP-21489 platformu (direktorijum CCES). 

## Pregled osnovnih funkcionalnosti
- Učitavanje .wav fajla i njegova konverzija u niz
- Eksportovanje niza odmjeraka audio signala u header fajl koji će se u ključiti u CCES projekat
- Implementacija audio efekata u Pythonu i generisanje .wav fajlova modifikovanih odmjeraka
- Implementacija audio efekata u C programskom jeziku
- Eksportovanje modifikovanih signala u tekstualne datoteke it C programskog jezika
- Čitanje tekstualnih datoteka i generisanje audio fajlova u Pythonu.

## Način pokretanja programa
  Program u Pythonu se pokreće standardno korištenjem sljedeće komande:
```
python effects.py
```
Sve potrebne biblioteke je moguće instalirati korištenjem sljedećih komandi (primjer):
```
python -m pip install scipy
python install ipython
python install matplotlib
```
Projekat razvijen unutar CCES razvojnog okruženja je potrebno otvoriti u istom, te izabrati Debug konfiguraciju za datu platformu (SHARC, ADSP-21489, EZ-KIT). Napomena je da se tekstualne datoteke za upisivanje obrađeni odmjeraka budu smješteni u Debug folder.
