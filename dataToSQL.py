from sqlConnector import sqlConnector


def makeTables(connector, table_names, table_attributes):
    for i in range(len(table_attributes)):
        connector.create_table(table_names[i], table_attributes[i])


def quotes(string):
    return '"' + string + '"'


def insertIntoAbilityTable(connector, abilityDict, abilityID, ability_1, ability_2, ability_hidden):
    if abilityDict.get((ability_1 + ability_2 + ability_hidden), None) is None:
        connector.insert_into_table('Abilities', [str(abilityID), quotes(ability_1), quotes(ability_2), quotes(ability_hidden)])
        abilityDict[ability_1 + ability_2 + ability_hidden] = abilityID
        abilityID += 1
    return abilityDict, abilityID


def insertIntoSpeciesTable(connector, speciesDict, speciesID, species):
    if speciesDict.get(species, None) is None:
        connector.insert_into_table('Species', [str(speciesID), quotes(species)])
        speciesDict[species] = speciesID
        speciesID += 1
    return speciesDict, speciesID


def insertIntoStatsTable(connector, statsDict, statsID, total_points, hp, attack, defense, sp_attack, sp_defense, speed):
    if statsDict.get((total_points + hp + attack + defense + sp_attack + sp_defense + speed), None) is None:
        connector.insert_into_table('Stats', [str(statsID), total_points, hp, attack, defense, sp_attack, sp_defense, speed])
        statsDict[total_points + hp + attack + defense + sp_attack + sp_defense + speed] = statsID
        statsID += 1
    return statsDict, statsID


def insertIntoTypingTable(connector, typingDict, typingID, type_1, type_2):
    if typingDict.get(type_1 + type_2, None) is None:
        connector.insert_into_table('Typing', [str(typingID), quotes(type_1), quotes(type_2)])
        typingDict[type_1 + type_2] = typingID
        typingID += 1
    return typingDict, typingID


def insertIntoGenerationTable(connector, generationID, generation, regionName):
    if generationID == int(generation):
        connector.insert_into_table('Generation', [generation, quotes(regionName)])
        generationID += 1
    return generationID


def insertIntoCharacteristicsTable(connector, name, pokedex_number, generation, status, speciesID, typingID, height_m, weight_kg, abilityID, statsID):
    connector.insert_into_table('Characteristics', [quotes(name), pokedex_number, generation, quotes(status), str(speciesID), str(typingID), height_m, weight_kg, str(abilityID), str(statsID)])


def insertDataIntoTables(connector, filename):
    abilityDict, speciesDict, statsDict, typingDict = [dict(), dict(), dict(), dict()]
    abilityID, speciesID, statsID, typingID, generationID = [1, 1, 1, 1, 1]
    with open(filename) as in_file:
        in_file.readline()
        for line in in_file:
            components = line.split(',')
            pokedex_number, name, generation, status, species, type_1, type_2, height_m, weight_kg, abilities_number, \
            ability_1, ability_2, ability_hidden, total_points, hp, attack, defense, sp_attack, sp_defense, speed, \
            catch_rate, percentage_male, region_name = components

            abilityDict, abilityID = insertIntoAbilityTable(connector, abilityDict, abilityID, ability_1, ability_2,
                                                            ability_hidden)
            speciesDict, speciesID = insertIntoSpeciesTable(connector, speciesDict, speciesID, species)
            statsDict, statsID = insertIntoStatsTable(connector, statsDict, statsID, total_points, hp, attack, defense,
                                                      sp_attack, sp_defense, speed)
            typingDict, typingID = insertIntoTypingTable(connector, typingDict, typingID, type_1, type_2)
            generationID = insertIntoGenerationTable(connector, generationID, generation, region_name.strip())
            insertIntoCharacteristicsTable(connector, name, pokedex_number, generation, status, speciesDict[species], typingDict[type_1 + type_2], quotes(height_m), quotes(weight_kg), abilityDict[ability_1 + ability_2 + ability_hidden], statsDict[total_points + hp + attack + defense + sp_attack + sp_defense + speed])


def main():
    connector = sqlConnector()
    connector.createDatabase('pokemon')

    characteristics_table = ['name VARCHAR(40)', 'pokedex_number INT', 'generation INT',
                             'status VARCHAR(20)', 'species_ID INT', 'typing_ID INT', 'height_m VARCHAR(20)',
                             'weight_m VARCHAR(20)', 'ability_ID INT', 'stats_ID INT']
    generation_table = ['generation INT', 'region_name VARCHAR(20)']
    species_table = ['species_ID INT', 'species VARCHAR(255)']
    typing_table = ['typing_ID INT', 'type_primary CHAR(10)', 'type_secondary CHAR(10)']
    ability_table = ['ability_ID INT', 'ability_1 CHAR(20)', 'ability_2 CHAR(20)',
                     'ability_hidden CHAR(20)']
    stats_table = ['stats_ID INT', 'total_points FLOAT', 'hp FLOAT', 'attack FLOAT',
                   'defense FLOAT', 'sp_attack FLOAT', 'sp_defense FLOAT', 'speed FLOAT']
    table_names = ['Characteristics', 'Generation', 'Species', 'Typing', 'Abilities', 'Stats']
    table_attributes = [characteristics_table, generation_table, species_table, typing_table, ability_table,
                        stats_table]
    makeTables(connector, table_names, table_attributes)
    insertDataIntoTables(connector, 'pokedex-slim.csv')

    connector.commit()


if __name__ == '__main__':
    main()
