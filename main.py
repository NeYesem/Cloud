import webapp2
from numpy import genfromtxt
import numpy as np
from random import randint
from google.cloud import storage
from google.cloud import datastore
import json
import datetime

c15_18M = 17.6
c15_18F = 13.3
c18_30M = 15.0
c18_30F = 14.8
c30_60M = 11.4
c30_60F = 8.1
c60M = 11.7
c60F = 9.0
NO_EXERCISE = 1.2
LOW_EXERCISE = 1.375
MEDIUM_EXERCISE = 1.55
HIGH_EXERCISE = 1.725
VERY_HIGH_EXERCISE = 1.9
class MainPage(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'application/json'
        all_data = self.request.get("name")
        self.response.write("Hello, " + all_data + "\n")
        #self.response.write(all_data)
        #self.response.write(my_data)
        ds = datastore.Client()

        query = ds.query(kind='')
        my_data = np.zeros((10,9))
        for a in range(0,9):
            #query.add_filter('__key__', '>', ds.key('', 1))
            my_data = list(query.fetch(limit=9))
            for b in range(len(my_data)):
                my_data[a][b] = '{name}'.format(**my_data[b])
                self.response.write(my_data[a][b]+'\n')
            self.response.write('-----------------\n')
        my_data = [[ 1.,  8.,  5.,  4.,  6.,  0.,  0.,  0.,  0.],
 [15., 53., 38.,  4., 37., 54., 36., 55., 56.],
 [ 1., 16., 38., 37., 12.,  0.,  0.,  0.,  0.],
 [ 1., 13.,  4.,  5.,  8., 35.,  0.,  0.,  0.],
 [ 1., 13.,  6.,  4.,  8.,  0.,  0.,  0.,  0.],
 [ 1., 16., 57.,  0.,  0.,  0.,  0.,  0.,  0.],
 [ 1., 13.,  8., 19.,  6., 58., 59.,  7.,  0.],
 [35., 60., 28., 61., 17.,  1., 57.,  0.,  0.],
 [ 6.,  1.,  4.,  8.,  0.,  0.,  0.,  0.,  0.],
 [ 1.,  2.,  4.,  6.,  5., 45.,  8.,  0.,  0.]]
        my_data2 = [[56.,  0.,  0.,  0.,  0.,  0.],
 [25., 29., 40., 20.,  0.,  0.],
 [20., 34., 33., 32., 28., 30.],
 [ 9., 43., 14.,  0.,  0.,  0.],
 [44., 14., 43., 23.,  0.,  0.],
 [23.,  0.,  0.,  0.,  0.,  0.],
 [ 9., 10.,  0.,  0.,  0.,  0.],
 [20., 29.,  0.,  0.,  0.,  0.],
 [20.,  0.,  0.,  0.,  0.,  0.],
 [14., 11., 24.,  0.,  0.,  0.]]
        file = ['Glutensiz Kasik Dokmesi\n', 'Glutensiz Mercimek Koftesi\n', 'Tavada Glutensiz Pizza\n', 'Glutensiz Ispanakli Kek\n', 'Glutensiz Kolay Cupcake\n', 'Kuru Meyveli Kurabiye\n', 'Yumusacik Kek ile Glutensiz Tiramisu\n', 'Ispanakli borek\n', 'Glutensiz Kahvaltilik Mini Pankek\n', 'Glutensiz Kek\n']
        mealName = file

        rec_Scores = np.zeros(61)
        x = 10
        y = 9
        for a in range(0,61):
            rec_Scores[a] = 1
        for a in range(0 , x//2):
            rand = randint(1,5) 
            for b in range(0, y):
                if(int(my_data[a][b])!=0):
                    rec_Scores[int(my_data[a][b])-1] *= (0.7+0.1*rand)
            for b in range(0, 6):        
                if(int(my_data2[a][b])!=0):
                    rec_Scores[int(my_data2[a][b])-1] *= (0.88+0.04*rand)

        meal_Score = np.zeros(10)
        for a in range(0 , x):
            for b in range(0, y):
                meal_Score[a] += rec_Scores[int(my_data[a][b])-1]
        #self.response.write(meal_Score)

        maxMeal = meal_Score[0]
        index = 0        
        for a in range(1, x):
            if(meal_Score[a]>maxMeal):
                maxMeal = meal_Score[a]
                index = a
        meal_Score[index] = 0 
        self.response.write("Morning:" + mealName[index])

        maxMeal = meal_Score[0]
        index = 0       
        for a in range(1, x):
            if(meal_Score[a]>maxMeal):
                maxMeal = meal_Score[a]
                index = a
        meal_Score[index] = 0 
        self.response.write("Noon:" + mealName[index])

        maxMeal = meal_Score[0]
        index = 0        
        for a in range(1, x):
            if(meal_Score[a]>maxMeal):
                maxMeal = meal_Score[a]
                index = a
        meal_Score[index] = 0 
        self.response.write("Evening:"+mealName[index])

        

        entity = datastore.Entity(key=ds.key('meals'))
        entity.update({
            'meal': ''+mealName[index],
            'timestamp': datetime.datetime.utcnow()
        })

        query = ds.query(kind='meals', order=('-timestamp',))

        results = [
            'Time: {timestamp} meal: {meal}'.format(**x)
            for x in query.fetch(limit=3)]
        ds.put(entity)


        output = 'Last 3 meals:\n{}'.format('\n'.join(results))
        self.response.write(output)
        def basal_metabolism(weight,height,age,gender):
            if(gender):
                return 66.5+13.75*weight+5.003*height-6.775*age
            else:
                return 655.1+9.563*weight+1.85*height-4.676*age
app = webapp2.WSGIApplication([
    ('/', MainPage),
], debug=True)
