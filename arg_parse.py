
import sys
import os
import argparse

def main():    
    #adding command line arguments
    parser = argparse.ArgumentParser(prog='Weather informaiton gather', 
                                     description='''Comparing weather data from a city on Earth to weather data from Mars.You will need
                                     to secelct a Season, year and a city to compare data from. A full list is cities and years are given
                                     for each respective argument.''')

    parser.add_argument("year",type = str, metavar = "<year>", help = "Please chose one of the following seasons Spring, Summer, Fall Winter.",
                        choices = ["2017","2018","2019","2020","2021"])

    parser.add_argument('-c',dest = 'e_location',metavar = '<Earth City>',
                        type = str, default = "LA",
                        help ='''Please choise one of the following cities LA ,DN, NY, TX, FL.If a city is not selected default will be LA''',
                        choices = ["LA","DN","NY","TX","FL"])

    parser.add_argument('-s',dest = 'season',metavar = '<Earth Season>',
                        type = str, default = "Spring",
                        help = "Please chose one of the following seasons Spring, Summer, Fall Winter. If a sesason is not selected defualt is Spring",
                        choices = ["Spring","Summer","Fall","Winter"])
    
    parser.add_argument('-e',dest= 'explore_graph',metavar = '<Explore graph>',action='store_true')

    parser.add_argument('-w',dest= 'write_csv',metavar = '<write_csv>', action='store_true')
    
    run( parser.parse_args())

def run(args):
    city_value = ""
    if args.e_location == "LA":
        #GHCND:USW00003167
        city_value = 'USW00003167'
    elif args.e_location == "DN":
        #GHCND:USC00052223
        city_value = "USC00052223"
    elif args.e_location == "NY":
        #GHCND:USW00094789
        city_value = "USW00094789"
    elif args.e_location == "TX":
        #GHCND:USW00013958
        city_value = "USW00013958"
    elif args.e_location == "FL":
        #GHCND:USW00012815
        city_value = "USW00012815"
    else:
        raise ValueError('City value not valied, please look into this.')
    
    #Pulling in data section
    earth_data = NOAA_Data(args.year,city_value,args.season)
    
    if args.explore_graph == True:
        earth_data.explor_graph()
        #method for mars data.



if __name__=="__main__":
    main()
