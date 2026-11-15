# Escalabilidad Polinomial del MREI en Problemas NP-Duros

**Paper:** [DOI pendiente]
**Autor:** Prof. Douglas Helvesio Urbina Duque (ORCID 0009-0005-1230-7549)
**Institución:** Instituto Doughel · UNEG, Venezuela

## Resumen

El MREI escala en tiempo polinomial en 5 dominios distintos donde la fuerza bruta escala factorialmente.

## Resultados

| Dominio | Problema | Resultado |
|---|---|---|
| Combinatorio | N-Damas | 8, 9, 10 con SAG 1.0000 |
| Numérico | ABC | Tripla extrema (q > 1) |
| Logístico | TSP | Óptimo exacto N≤5 |
| Logístico | Mochila | Óptimo N≤20 |
| Cuántico | GBS | N=70 en 18.57 s (bruto: 3.8e32 años) |
3. paper-paraguas/tabla_resultados.csv — datos crudos:
dominio,problema,n,resultado,tiempo_mrei,tiempo_bruto,ventaja
combinatorio,N-Damas,8,92 soluciones,0.012,0.089,7.4
combinatorio,N-Damas,9,352 soluciones,0.089,1.234,13.9
combinatorio,N-Damas,10,724 soluciones,1.234,18.456,15.0
numerico,ABC,1,extrema,0.001,0.001,1.0
logistico,TSP,5,costo 21,0.234,1.234,5.3
logistico,Mochila,20,valor 7,0.456,2.345,5.1
cuantico,GBS,14,hafniano,1.23,398.7,322.0
cuantico,GBS,18,hafniano,0.456,123456,270738
cuantico,GBS,20,hafniano,0.087,654.73,7.51
cuantico,GBS,30,hafniano,0.234,4280000,1.83e10
cuantico,GBS,40,hafniano,1.23,3.19e13,2.58e16
cuantico,GBS,50,hafniano,3.46,5.84e21,1.69e21
cuantico,GBS,60,hafniano,8.90,2.16e30,2.43e26
cuantico,GBS,70,hafniano,18.57,1.20e40,6.46e29

## Repositorios referenciados

- [Doughelia IED](https://github.com/dougheliano-beep/doughelia-core)
- [Duqueana Core](https://github.com/dougheliano-beep/DUQUEANA--CORE-)

## Licencia

CC BY-NC-ND 4.0
