import unittest
from sqlConnector import sqlConnector


class MyTestCase(unittest.TestCase):
    connector = sqlConnector()

    @staticmethod
    def create_test_database():
        MyTestCase.connector.query('drop database if exists test')
        MyTestCase.connector.query('create database test')
        MyTestCase.connector.query('use test')

    def test_createSQLConnectorInstance(self):
        result = MyTestCase.connector.query('Show databases;')
        self.assertEqual([('astronaut',), ('beer',), ('employees',), ('information_schema',), ('lahmansbaseballdb',), ('literature',), ('menagerie',), ('music',), ('mysql',), ('performance_schema',), ('president',), ('relational_algebra',), ('students',), ('sys',), ('tech',), ('tutorial',), ('warships',)], result)

    @staticmethod
    def test_create_database():
        MyTestCase.create_test_database()
        MyTestCase.connector.query('drop database test;')

    @unittest.expectedFailure
    def test_database_does_not_exist(self):
        MyTestCase.connector.query('Drop database if exists test;')
        MyTestCase.connector.query('Use test')

    def test_create_table(self):
        MyTestCase.create_test_database()
        MyTestCase.connector.create_table('numbers', ['number INT'])
        self.assertEqual([('numbers',)], MyTestCase.connector.query('show tables'))
        MyTestCase.connector.query('drop database test')

    def test_insert_into_tables(self):
        MyTestCase.create_test_database()
        MyTestCase.connector.create_table('numbers', ['number INT'])
        MyTestCase.connector.insert_into_table('numbers', ['1'])
        self.assertEqual([(1,)], MyTestCase.connector.query('select * from numbers'))
        MyTestCase.connector.query('Drop database test')


if __name__ == '__main__':
    unittest.main()
