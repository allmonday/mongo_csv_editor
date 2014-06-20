import logging
import sys
from pymongo import MongoClient
from bson.objectid import ObjectId

class Db2Csv(object):
    '''output key csv file'''

    def __init__(self, collection):

        self.col = collection


    def output_to_csv(self, file_name, *fields):
        '''input the fields you want to output, if field not exists,
        prog will stop'''
        with open(file_name, 'w') as dump:
            fields = ['_id'] + list(fields)
            dump.write(','.join(fields) + '\n')

            query = self.col.find()
            for q in query:
                try:
                    values = [str(q[i]) for i in fields]
                except KeyError:
                    print('you entered a field not existed')
                    sys.exit()
                line = ','.join(values)
                dump.write(line + '\n')


    def write_back_db(self, file_name):
        import csv
        confirm = input('''
            you are going to update db from file:%s
            do you want to update the database? (y or yes): '''%file_name)

        if confirm in ['y','yes']:
            print('start update\n')
            with open(file_name, 'r') as csvfile:
                fixed_data = csv.reader(csvfile, delimiter=',', 
                                        skipinitialspace=True)
                fixed_data = list(fixed_data)

                #get fields
                fields = fixed_data[0][1:]

                #update data
                for line in fixed_data[1:]:
                    _id = line[0]
                    _field_values = line[1:]

                    #combine key and value
                    revised_data_dict = dict(zip(fields, _field_values))
                    ret = self.col.update({'_id': ObjectId(_id)}, 
                                    {'$set': revised_data_dict })
                    print(ret)

            print('update finished')
        else: sys.exit()

    def __call__(self):
        pass
        #self.output_to_csv()



if __name__ == "__main__":

    #product = MongoClient('192.168.1.21')['caigen-development'].products_formula

    product = MongoClient()['test'].product

    d2c = Db2Csv(product)
    #d2c.output_to_csv('name', 'age')
    d2c.write_back_db('promula_products.csv')
