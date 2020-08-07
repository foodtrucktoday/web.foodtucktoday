#  Copyright (c) 2020 Romain ODET
#
#      This program is free software: you can redistribute it and/or modify
#      it under the terms of the GNU General Public License as published by
#      the Free Software Foundation, either version 3 of the License, or
#      (at your option) any later version.
#
#      This program is distributed in the hope that it will be useful,
#      but WITHOUT ANY WARRANTY; without even the implied warranty of
#      MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#      GNU General Public License for more details.
#
#      You should have received a copy of the GNU General Public License
#      along with this program.  If not, see <https://www.gnu.org/licenses/>.

import datetime
import os

import dotenv
import pymysql

dotenv.load_dotenv()  # for python-dotenv method


class Model:
    # Constructor, connect to database
    def __init__(self):
        host = os.environ.get('bdd_host')
        port = int(os.environ.get('bdd_port'))
        user = os.environ.get('bdd_user')
        password = os.environ.get('bdd_password')
        db = os.environ.get('bdd_name')
        self.con = pymysql.connect(host=host, port=port, user=user, password=password, db=db,
                                   cursorclass=pymysql.cursors.DictCursor)
        self.cur = self.con.cursor()

    def __enter__(self):
        return self

    # Destructor, disconnect from database
    def __exit__(self, type, value, traceback):
        if (self.con):
            self.con.close()

    def GetFoodtruckToday(self):
        now = datetime.datetime.today()
        return self.sqlQuery(
            """
                select foodtruck.id as f_id, foodtruck.name as f_name, category.name as c_name,
       planning.day_id as p_day, planning.active as active, places.name as pl_name,
       foodtruck.phone as f_phone, foodtruck.email as f_email, 
       foodtruck.website as f_website, foodtruck.facebook as f_facebook, 
       places.latitude as pl_latitude, places.longitude as pl_longitude, 
       places.address as pl_address

        from foodtruck
        
        left join category on foodtruck.category_id = category.id
        left join planning on foodtruck.id = planning.foodtruck_id
        inner join places on planning.places_id = places.id
        
        where planning.day_id = '%s'
        order by places.id
            """ % now.weekday())

    def GetFoodtruckDay(self, id):
        now = datetime.datetime.today()
        return self.sqlQuery(
            """
            select foodtruck.id as f_id, foodtruck.name as f_name, category.name as c_name,
           planning.day_id as p_day, planning.active as active, places.name as pl_name,
           foodtruck.phone as f_phone, foodtruck.email as f_email, 
           foodtruck.website as f_website, foodtruck.facebook as f_facebook, 
           places.latitude as pl_latitude, places.longitude as pl_longitude, 
           places.address as pl_address
    
            from foodtruck
            
            left join category on foodtruck.category_id = category.id
            left join planning on foodtruck.id = planning.foodtruck_id
            inner join places on planning.places_id = places.id
            
            where planning.day_id = '%s'
            order by places.id
            """ % id)

    def GetFoodtruckPlace(self, id):
        return self.sqlQuery(
            """
            select foodtruck.id as f_id, foodtruck.name as f_name, category.name as c_name,
           planning.day_id as p_day, planning.active as active, places.name as pl_name,
           foodtruck.phone as f_phone, foodtruck.email as f_email, 
           foodtruck.website as f_website, foodtruck.facebook as f_facebook, 
           places.latitude as pl_latitude, places.longitude as pl_longitude, 
           places.address as pl_address
    
            from foodtruck
            
            left join category on foodtruck.category_id = category.id
            left join planning on foodtruck.id = planning.foodtruck_id
            inner join places on planning.places_id = places.id
            
            where places.id = '%s'
            order by places.id
            """ % id)

    def getPlace(self, id):
        return self.sqlQueryOne(
            """
            select places.name as pl_name
            from places
            where places.id = '%s'
       """ % id)

    # Execute an SQL query and returns the result
    def sqlQuery(self, q):
        res = self.cur.execute(q)
        return self.cur.fetchall()

        # Execute an SQL query and returns the result

    def sqlQueryOne(self, q):
        res = self.cur.execute(q)
        return self.cur.fetchone()
