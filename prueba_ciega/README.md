# Prueba Ciega de Restauración Estructural (Protocolo Génesis v3.0.0)

Este directorio contiene los archivos de la Prueba Ciega ejecutada para validar el Motor MREI.

## Dictamen
Los resultados del dictamen oficial están publicados en Zenodo: [DOI 10.5281/zenodo.23481918](https://doi.org/10.5281/zenodo.23481918).

## Sello Criptográfico (SHA-256)
El hash de la repetición local es: `61243bb8e353fbd07545ea0864c851980c549409667d9b40ea8caebb9c471281`

## Contenido
- `referencia_secreta.pdb`: Estructura objetivo (Ground Truth).
- `entrada_perturbada.pdb`: Estructura con desviaciones.
- `salida_restaurada.pdb`: Estructura generada por el motor.
- `prueba_ciega_genesis.py`: Script de verificación Kabsch/SVD.
