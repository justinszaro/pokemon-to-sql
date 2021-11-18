from sqlConnector import sqlConnector


def createQueries():
    queries = {}
    questionsFile = open("questions.txt", "r")
    queryFile = open("queries.txt", "r")
    for question in questionsFile:
        question = question.strip()
        query = queryFile.readline()
        query = query.strip()
        data = question.split(',')
        queries[data[0]] = [question[2:], query]
    questionsFile.close()
    queryFile.close()
    return queries


def getResult(connector, outfile, queries, question):
    print(question, queries[question][0], sep='. ', file=outfile)
    print(queries[question][1], file=outfile)
    connector.query(queries[question][1])
    result = connector.fetchOne()
    while result is not None:
        print(*(result[i] for i in range(len(result))), sep=",", file=outfile)
        result = connector.fetchOne()
    print(file=outfile)


def main():
    queries = createQueries()
    connector = sqlConnector()
    connector.useDatabase('pokemon')
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j']
    with open('results.txt', 'w') as outfile:
        for letter in letters:
            getResult(connector, outfile, queries, letter)
    connector.commit()


if __name__=='__main__':
    main()