import io
import csv
import math
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import itertools

def get_header_list(filename, delimiter):
    csv_file = open(filename,'r')
    reader = csv.reader(csv_file)
    csv_line = csv_file.readline()
    list1 = csv_line.split(delimiter)
    csv_file.close()
    
def read_columns(filename, columns, delimiter):
    csv_file = open(filename,'r')
    result = []
    for line in csv_file:
        lines = (line.replace("\n", "")).split(delimiter)
        if lines[0].isdigit():
            temp = []
            for index in columns:
                temp.append(float(lines[index]))
            result.append(temp)
    return np.array(result)

def get_avg_all_rows(data, columns):
    result = []
    for col in columns:
        print(col)
        result.append(np.mean(data[:,col]))
    return np.array(result)

def get_data_in_range(data, col, low_bnd, up_bnd):
    result = []
    for element in data:
        if up_bnd >= element[col] >= low_bnd:
            result.append(element)
    return np.array(result)

def get_axis_sizes(data, x_axis, y_axis):
    factor = (np.max(data[:,x_axis]) - np.min(data[:,x_axis])) * 0.1
    max_x = math.ceil(np.max(data[:,x_axis]) + factor)
    min_x = math.floor(np.min(data[:,x_axis]) - factor)
    max_y = []
    min_y = []
    for y in y_axis:
        factor = (np.max(data[:,y]) - np.min(data[:,y])) * 0.1
        max_y.append(math.ceil(np.max(data[:,y]) + factor))
        min_y.append(math.floor(np.min(data[:,y]) - factor))
    return [min_x, max_x, min(min_y), max(max_y)]

def mulit_plot(data, x_axis, y_axis, filename, title, x_lable, y_lable):
    print (data[:,x_axis])
    x_value = data[:,x_axis]
    colors = iter(cm.rainbow(np.linspace(0, 1, len(y_axis))))
    for y in y_axis:
        y_value = data[:,y]
        plt.scatter(x_value, y_value, color=next(colors))
    plt.xlabel(x_lable, fontsize=15)
    plt.ylabel(y_lable, fontsize=15) 
    plt.suptitle(title, fontsize=15)
    plt.axis(get_axis_sizes(data, x_axis, y_axis))
    plt.show()
    plt.savefig(filename)
    
if __name__ == "__main__":
    #Plot 1
    data = read_columns("toronto_monthly_temps.csv", [0,1,2,3,4],",")
    print (data)
    #print (data[])
    #data = get_data_in_range(data, 0, 1960, 2011)
    #data = get_data_in_range(data, 1, 8, 8)
    #mulit_plot(data, 0, [2,3,4], "plot1.png", "August High, Average and Low temperatures vs Year", "Year", "High, Average and Low in C")
    