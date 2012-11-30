import unittest
import Logger
import handler
import sqlite3
import os

location = 'C:\\Users\\Cimara\\Documents\\GitHub\\EECS393-RasPiHome\\Client Stuff\\test.txt' #this is the location I currently am using
class TestHomeAutomation(unittest.TestCase):

	def setUp(self):
		print '\n'
		
	def test_append(self):
		#verify the inputInvalid method (and other logger methods) will successfully
		#append to the logger file
		Logger.inputInvalid("Successfully appended.")
		f = open(location, 'r+')
		testString = f.read()
		f.close()
		self.assertTrue(testString.endswith("appended."))
		print "Append test completed"
		
	def test_accessdb(self):
		createDB = sqlite3.connect("myDatabase")

		query = createDB.cursor()
		query.execute('SELECT SQLITE_VERSION() ')
		data = query.fetchone()
		bID = 1
		buildings = query.execute('SELECT * FROM piServer_building WHERE id = %s' % bID)
		self.assertIsNotNone(buildings)
		
		print "Access DB entries test completed"
		
		for building in buildings:
			owner = building[2]
			self.assertIsNotNone(owner)
			self.assertEqual(building[1], "MyHouse")
		print "Access DB attribute test completed"
		
	def test_killserver(self):
		os.system("C:\Users\Cimara\Documents\GitHub\EECS393-RasPiHome\ServerStart.bat")
		pass
		
if __name__ == '__main__':
	unittest.main()
