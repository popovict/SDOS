# Sistemi za digitalnu obradu signala
## Dodavanje muzičkih efekata u audio signal korištenjem razvojnog okruženja ASDP-21489
Repozitorijum se sastoji od programa napisanog korištenjem Python programskog jezika, koji služi za učitavanje audio fajlova sa ekstenzijom .wav, implementaciju audio efekata i primjenjivanje na učitani audio signal, te generisanje modifikovanog audio fajla (direktorijum Python). Audio efekti su po istom principu implementirani u C programskom jeziku korištenjem CrossCore Embedded Studio razvojnog okruženja, a program je namijenjen za ADSP-21489 platformu (direktorijum CCES). Detalji implementaciji se mogu pronaći u izvještaju SDOS_2024_Tanja_Popovic_1218_17.pdf. 

## Pregled osnovnih funkcionalnosti
- Učitavanje .wav fajla i njegova konverzija u niz odmjeraka
- Eksportovanje niza odmjeraka audio signala u header fajl koji će se u ključiti u CCES projekat
- Implementacija audio efekata u Pythonu i generisanje .wav fajlova na osnovu modifikovanih odmjeraka
- Implementacija audio efekata u C programskom jeziku
- Eksportovanje modifikovanih signala u tekstualne datoteke u C programskom jeziku
- Čitanje tekstualnih datoteka i generisanje audio fajlova u Pythonu.

U Python direktorijumu su zbog bolje preglednosti objedinjeni .wav fajlovi generisani unutar Pythona (Python wav files direktorijum), dok su .wav fajlovi generisani na osnovu tekstualnih datoteka smješteni u direktorijum C wav files. U direktorijumu Txt audio samples se nalaze tekstualne datoteke generenisane iz projekta unutar CCESa.
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
Projekat razvijen unutar CCES razvojnog okruženja je potrebno otvoriti u istom, te izabrati Debug konfiguraciju za datu platformu (SHARC, ADSP-21489, EZ-KIT). Napomena je da se tekstualne datoteke za upisivanje obrađenih odmjeraka budu smješteni u Debug folder, te upisati odgovarajući naziv datoteke u fopen funkciji.
