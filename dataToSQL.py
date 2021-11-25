from sqlConnector import sqlConnector


def makeTables(connector, table_names, table_attributes):
    for i in range(len(table_attributes)):
        connector.create_table(table_names[i], table_attributes[i])


def insertIntoTables(connector, table_name, dictionary, ID, values):
    lst = [ID]
    for value in values:
        lst.append(value)
    if dictionary.get(''.join(values), None) is None:
        connector.insert_into_table(table_name, lst)
        dictionary[''.join(values)] = ID
        ID += 1
    return dictionary, ID


def insertIntoGenerationTable(connector, generationID, generation, regionName):
    if generationID == int(generation):
        connector.insert_into_table('Generation', [generation, regionName])
        generationID += 1
    return generationID


def insertIntoCharacteristicsTable(connector, name, pokedex_number, generation, status, speciesID, typingID, height_m,
                                   weight_kg, abilityID, statsID, catch_rate, percentage_male):
    connector.insert_into_table('Characteristics',
                                [name, pokedex_number, generation, status, str(speciesID),
                                 str(typingID), height_m, weight_kg, str(abilityID), str(statsID), catch_rate, percentage_male])


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

            abilityDict, abilityID = insertIntoTables(connector, 'Abilities', abilityDict, abilityID, [ability_1, ability_2,
                                                            ability_hidden])
            speciesDict, speciesID = insertIntoTables(connector, 'Species', speciesDict, speciesID, [species])
            statsDict, statsID = insertIntoTables(connector, 'Stats', statsDict, statsID, [total_points, hp, attack, defense,
                                                      sp_attack, sp_defense, speed])
            typingDict, typingID = insertIntoTables(connector, 'Typing', typingDict, typingID, [type_1, type_2])
            generationID = insertIntoGenerationTable(connector, generationID, generation, region_name.strip())
            insertIntoCharacteristicsTable(connector, name, pokedex_number, generation, status, speciesDict[species],
                                           typingDict[type_1 + type_2], height_m, weight_kg,
                                           abilityDict[ability_1 + ability_2 + ability_hidden], statsDict[
                                               total_points + hp + attack + defense + sp_attack + sp_defense + speed], catch_rate, percentage_male)


def getTableAttributes(filename):
    characteristics = []
    with open(filename) as in_file:
        for line in in_file:
            characteristics.append(line.strip().split(','))
    return characteristics


def main():
    connector = sqlConnector()
    connector.createDatabase('pokemon')

    table_names = ['Characteristics', 'Generation', 'Species', 'Typing', 'Abilities', 'Stats']
    table_attributes = getTableAttributes('dataTypes.txt')

    makeTables(connector, table_names, table_attributes)
    insertDataIntoTables(connector, 'pokedex-slim.csv')

    connector.commit()


if __name__ == '__main__':
    main()
