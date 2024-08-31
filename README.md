# Desafio---Secret-ria-de-Dados-

Quantos chamados foram abertos no dia 01/04/2023?

SELECT COUNT(*) AS total_chamados
FROM `datario.adm_central_atendimento_1746.chamado`
WHERE DATE(data_inicio) = '2023-04-01';
Resposta: 1756.

Qual o tipo de chamado que teve mais teve chamados abertos no dia 01/04/2023?

SELECT id_tipo, COUNT(*) AS total_chamados
FROM `datario.adm_central_atendimento_1746.chamado`
WHERE DATE(data_inicio) = '2023-04-01'
GROUP BY id_tipo
ORDER BY total_chamados DESC
LIMIT 1;
Resposta: O tipo de chamado que teve mais chamados abertos foi o 782 com 366 chamados. 

Quais os nomes dos 3 bairros que mais tiveram chamados abertos nesse dia?

SELECT id_bairro, COUNT(*) AS total_chamados
FROM `datario.adm_central_atendimento_1746.chamado`
WHERE DATE(data_inicio) = '2023-04-01'
GROUP BY id_bairro
ORDER BY total_chamados DESC
LIMIT 3;
Resposta: Os 3 bairros com mais chamados foram o bairro Campo Grande (144) com 113 chamados, o bairro Tijuca (33) com 89 chamados e o bairro null - consta null na tabela com 73 chamados. 

Qual o nome da subprefeitura com mais chamados abertos nesse dia?

SELECT nome_unidade_organizacional, COUNT(*) AS total_chamados
FROM `datario.adm_central_atendimento_1746.chamado`
WHERE DATE(data_inicio) = '2023-04-01'
GROUP BY nome_unidade_organizacional
ORDER BY total_chamados DESC
LIMIT 1;
Resposta: A subprefeitura com mais chamados foi a GM-RIO - Guarda Municipal do Rio de Janeiro com 498 chamados.


Existe algum chamado aberto nesse dia que não foi associado a um bairro ou subprefeitura na tabela de bairros? Se sim, por que isso acontece?

SELECT id_chamado, data_inicio, id_bairro, nome_unidade_organizacional
FROM `datario.adm_central_atendimento_1746.chamado`
WHERE DATE(data_inicio) = '2023-04-01'
AND (id_bairro IS NULL OR id_bairro = '' OR nome_unidade_organizacional IS NULL OR nome_unidade_organizacional = '');
Resposta: Foram 73 chamados abertos não associados á um bairro. Os 73 chamados foram associados á uma subprefeitura. Isso acontece por que dados não cadastrados, erro no registro, chamada fora da area de cobertura ou problemas na integração dos dados. 


Quantos chamados com o subtipo "Perturbação do sossego" foram abertos desde 01/01/2022 até 31/12/2023 (incluindo extremidades)?

SELECT COUNT(*) AS total_chamados
FROM `datario.adm_central_atendimento_1746.chamado`
WHERE subtipo = 'Perturbação do sossego'
AND DATE(data_inicio) BETWEEN '2022-01-01' AND '2023-12-31';
Resposta: 42830 chamados. 


Selecione os chamados com esse subtipo que foram abertos durante os eventos contidos na tabela de eventos (Reveillon, Carnaval e Rock in Rio).
Quantos chamados desse subtipo foram abertos em cada evento?

WITH eventos_relevantes AS (
SELECT evento, data_inicial, data_final
FROM `datario.turismo_fluxo_visitantes.rede_hoteleira_ocupacao_eventos`
WHERE evento IN ('Reveillon', 'Carnaval', 'Rock in Rio')
)
SELECT COUNT(*) AS total_chamados
FROM `datario.adm_central_atendimento_1746.chamado` c
JOIN eventos_relevantes e
ON DATE(c.data_inicio) BETWEEN e.data_inicial AND e.data_final
WHERE c.subtipo = 'Perturbação do sossego'
AND DATE(c.data_inicio) BETWEEN '2022-01-01' AND '2023-12-31';
Resposta: 1214 chamados. 



Qual evento teve a maior média diária de chamados abertos desse subtipo?

WITH eventos_relevantes AS (
SELECT evento, data_inicial, data_final
FROM `datario.turismo_fluxo_visitantes.rede_hoteleira_ocupacao_eventos`
WHERE evento IN ('Reveillon', 'Carnaval', 'Rock in Rio')
)
SELECT e.evento, COUNT(*) AS total_chamados
FROM `datario.adm_central_atendimento_1746.chamado` c
JOIN eventos_relevantes e
ON DATE(c.data_inicio) BETWEEN e.data_inicial AND e.data_final
WHERE c.subtipo = 'Perturbação do sossego'
AND DATE(c.data_inicio) BETWEEN '2022-01-01' AND '2023-12-31'
GROUP BY e.evento;
Resposta: O evento com a maior média diaária de chamados foi o Rock In Rio com 834 chamados. 

Compare as médias diárias de chamados abertos desse subtipo durante os eventos específicos (Reveillon, Carnaval e Rock in Rio) e a média diária de chamados abertos desse subtipo considerando todo o período de 01/01/2022 até 31/12/2023.


WITH eventos_relevantes AS (
SELECT evento, data_inicial, data_final
FROM `datario.turismo_fluxo_visitantes.rede_hoteleira_ocupacao_eventos`
WHERE evento IN ('Reveillon', 'Carnaval', 'Rock in Rio')
),
AS (
SELECT e.evento,
COUNT(*) AS total_chamados,
DATE_DIFF(MAX(c.data_inicio), MIN(c.data_inicio), DAY) + 1 AS dias_evento
FROM `datario.adm_central_atendimento_1746.chamado` c
JOIN eventos_relevantes e
ON DATE(c.data_inicio) BETWEEN e.data_inicial AND e.data_final
WHERE c.subtipo = 'Perturbação do sossego'
AND DATE(c.data_inicio) BETWEEN '2022-01-01' AND '2023-12-31'
GROUP BY e.evento
),
media_diaria_eventos AS (
SELECT evento,
total_chamados / dias_evento AS media_diaria_evento
FROM chamados_por_evento
),
chamados_total_periodo AS (
SELECT COUNT(*) AS total_chamados_total,
DATE_DIFF('2023-12-31', '2022-01-01', DAY) + 1 AS dias_total
FROM `datario.adm_central_atendimento_1746.chamado`
WHERE subtipo = 'Perturbação do sossego'
AND DATE(data_inicio) BETWEEN '2022-01-01' AND '2023-12-31'
),
media_diaria_total AS (
    SELECT total_chamados_total / dias_total AS media_diaria_total
    FROM chamados_total_periodo
)
SELECT e.evento, 
       e.media_diaria_evento, 
       t.media_diaria_total
FROM media_diaria_eventos e
CROSS JOIN media_diaria_total t;
Resposta:  1) Rock in Rio - 83.4 - 58.671232876712331  2)Carnaval - 60.25 - 58.671232876712331  3) Reveillon - 46.333333333333336 -58.671232876712331



