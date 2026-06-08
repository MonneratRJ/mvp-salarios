# NOVO CAGED MOV Schema

## Source

- Base folder: `ftp://ftp.mtps.gov.br/pdet/microdados/NOVO%20CAGED/`
- File type: `CAGEDMOVYYYYMM.7Z`
- Extracted text file: `CAGEDMOVYYYYMM.txt`
- Delimiter: `;`
- Encoding: UTF-8

## File naming pattern

The year and month in the folder path must match the file name.

Example:

- Folder: `2026/202604/`
- File: `CAGEDMOV202604.7Z`
- Extracted text: `CAGEDMOV202604.txt`

## Current confirmed columns

1. competênciamov
2. região
3. uf
4. município
5. seção
6. subclasse
7. saldomovimentação
8. cbo2002ocupação
9. categoria
10. graudeinstrução
11. idade
12. horascontratuais
13. raçacor
14. sexo
15. tipoempregador
16. tipoestabelecimento
17. tipomovimentação
18. tipodedeficiência
19. indtrabintermitente
20. indtrabparcial
21. salário
22. tamestabjan
23. indicadoraprendiz
24. origemdainformação
25. competênciadec
26. indicadordeforadoprazo
27. unidadesaláriocódigo
28. valorsaláriofixo

## Notes

- The raw file is semicolon-separated.
- Column names are preserved here exactly as observed in the source header.
- This schema note should be expanded when we inspect more months and verify whether the layout stays stable.
