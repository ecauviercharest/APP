# -*- coding: utf-8 -*-
"""
Create plots using GeoDeepLearning's training results.

- folder_path (string) : Path of the folder containing GeoDeepLearning's 
    training results. May contain multiple sub-folders, each representing one
    set of training results to plot.
- graph_type (array) : Type of plots to produce
    
Created by Stéphanie Lachance (2020-04-07).
"""

import argparse
import os.path

#import glob
import pandas as pd
import matplotlib.pyplot as plt

# 
def retrieve_param_value(path, GDLparam):
    '''
    Extract the learning rate of the GDL training session from a file path.
    
    file_path (string) : Path of the file containing the data.
    return (float): Learning rate used during the GDL training session.
        
    '''
    lr_str = (path.split('_'))[-1]
    
    try :
        lr = float(lr_str.replace(GDLparam, ''))
        return lr
    except : 
        print(f"File path not following required format. String required : {GDLparam}, path : {path}")
        return None
    

def loss_vs_learning_rate (folders):
    '''
    Plot the best loss value for each learning rate. 
    
    Require the results of multiple training sessions, with one learning rate used per session.
    
    param folders (array of string): Folders containing the results of the GDL training sessions.
    return (dataframe): Best loss values for the training and the validation
    '''
    data = []

    for folder in folders :
        # Retrieve the learning rate of the training session
        lr = retrieve_param_value(folder, 'lr')
        if lr is None :
            continue
        
        # Retrieve best loss value for the training
        with open(os.path.join(folder, "metric_trn_loss.log"), 'r') as f:
            log = f.readlines()
            
            best_trn_loss = None
            
            for line in log:
                cols = line.split('\t')
                stat = float(cols[1].replace('\n', ''))
                
                if (best_trn_loss is None) or (stat < best_trn_loss) :
                    best_trn_loss = stat
        
        # Retrieve best loss value for the validation
        with open(os.path.join(folder, "metric_val_loss.log"), 'r') as f:
            log = f.readlines()
            
            best_val_loss = None
            
            for line in log:
                cols = line.split('\t')
                stat = float(cols[1].replace('\n', ''))
                
                if (best_val_loss is None) or (stat < best_val_loss) :
                    best_val_loss = stat
        
        data.append([lr, best_trn_loss, best_val_loss])    
        
    # Save values in dataframe
    df = pd.DataFrame(data, columns=['learning_rate', 'trn_loss', 'val_loss'])
    df.sort_values(by='learning_rate', inplace=True)
              
    return df

def val_stat_vs_epoch (folder, files, stat_name):
    '''
    Plot the chosen statistic for each epoch. Include the statistic per class and
    the average.
    
    param folder (array of string): Folder containing the results of the GDL training session.
    param files (array of string): Name of the files containing the statistics.
    param stat_name (string): Name of the statistic to plot.
    return (dataframe): Statistics per epoch for the training and the validation
    '''
    
    # Retrieve average values
    data = []
    with open(os.path.join(folder, files[0]), 'r') as f:
        log = f.readlines()
                
        for line in log:
            cols = (line.replace('\n', '')).split('\t')
            data.append([int(cols[0]), float(cols[1])])
    
    # Save values in dataframe
    df1 = pd.DataFrame(data, columns=['epoch', 'average_' + stat_name])
    
    
    # Retrieve values per class (if exist)
    data = []
    if len(files) > 1 :
        with open(os.path.join(folder, files[1]), 'r') as f:
            log = f.readlines()
            current_epoch, classes = -1, []
            
            for line in log:
                cols = (line.replace('\n', '')).split('\t')
                
                if cols[1] not in classes :
                    classes.append(cols[1])
                
                # Group values associated with the same epoch
                if int(cols[0]) > current_epoch:
                    # Save last row 
                    if current_epoch >= 0 :
                        data.append(row)
                    
                    # Start new row
                    current_epoch = int(cols[0])
                    row = [int(cols[0]), float(cols[2])]
                
                else :
                    row.append(float(cols[2]))
                              
        # Save values in dataframe
        cols_name = ['epoch']
        for i in classes:
            cols_name.append('class_' + str(i))
        df2 = pd.DataFrame(data, columns=cols_name)
        
        # Merge dataframes
        df2 = df2.set_index('epoch')
        new_df = df1.join(df2, on='epoch')
        new_df.sort_values(by='epoch', inplace=True)
        
        return new_df
    
    df1.sort_values(by='epoch', inplace=True)          
    return df1

def plot_data(df, title, x_name, y_name, style):
    '''
    Plot data. 
    
    df (dataframe): Data set(s) to plot.
    title (string) : Title of the plot.
    x_name (string) : Name of the horizontal axis.
    y_name (string) : Name of the vertical axis.
    style (dictionnary) : Set of parameters related to the plot's appearence.
    return: None
    '''        
    nb_cols = len(df.columns)
    
    # Data extent
    if style['xextent'] is None:
        xmin = (df.iloc[:, 0]).min(axis=0)
        xmax = (df.iloc[:, 0]).max(axis=0)
        # extent = abs(xmax - xmin)
        # xmin, xmax = xmin - 0.05*extent, xmax + 0.05*extent
    else:
        xmin, xmax =  style['xextent'][0], style['xextent'][1]
        
    if style['yextent'] is None:      
        cols_mins = (df.iloc[:, 1:]).min(axis=0)
        cols_maxs = (df.iloc[:, 1:]).max(axis=0)
        ymin, ymax = min(cols_mins), max(cols_maxs)
        extent = abs(ymax - ymin)
        ymax = ymax + 0.1*extent
        ymin = ymin - 0.05*extent
        if ymin < 0:
            ymin = 0
    else:
        ymin, ymax =  style['yextent'][0], style['yextent'][1]
        
    # Plot data
    fig, ax = plt.subplots(1)    
    for col in range(1,nb_cols):
        ax.plot(df.iloc[:, 0], df.iloc[:, col], label=df.columns[col])
                        
    # Plot style
    ax.set_title(title)
    ax.legend(loc='best')
    ax.set_xlabel(x_name)
    ax.set_ylabel(y_name)
    plt.axis([xmin, xmax, ymin, ymax])
    if style['xscale'] is not None:
        plt.xscale(style['xscale'])
    plt.show()
        

def main(args):
    
    plot_style = {}
    plot_style['xextent'] = args.xextent
    plot_style['yextent'] = args.yextent
    plot_style['xscale'] = None
    
    # Create plots
    if 'loss_vs_learning_rate' in args.plots:
        plot_style['xscale'] = 'log'
        dataframe = loss_vs_learning_rate(args.inFolders)
        plot_data(dataframe, 'Best learning rate', 'Learning rate', 'Loss', plot_style)
        
        # Reset plot style
        plot_style['xscale'] = None
    
    if 'stat_vs_epoch' in args.plots:
        # Identify the files for the statistic to plot
        if args.stat == 'val_fscore':
            files = ['metric_val_fscore_averaged.log', 'metric_classwise_val_fscore.log']
            title, yname = 'F-score during the validation', 'F-score'   
 
        elif args.stat == 'val_loss':
            files = ['metric_val_loss.log']
            title, yname = 'Loss during the validation', 'Loss'
               
        elif args.stat == 'val_precision':
            files = ['metric_val_precision_averaged.log', 'metric_classwise_val_precision.log']
            title, yname = 'Precision during the validation', 'Precisions'
        
        elif args.stat == 'val_recall':
            files = ['metric_val_recall_averaged.log', 'metric_classwise_val_recall.log']
            title, yname = 'Recall during the validation', 'Recall'
        
        # Create plots
        for folder in args.inFolders :               
            dataframe = val_stat_vs_epoch(folder, files, args.stat)   
            plot_data(dataframe, title, 'Epochs', yname, plot_style)
            
            
if __name__ == '__main__':
    # Parser
    parser = argparse.ArgumentParser(description="Sample preparation")
    parser.add_argument("plots", 
                        choices=['loss_vs_learning_rate', 'val_stat_vs_epoch'],
                        help="Type of plot wanted.")
    parser.add_argument("inFolders", metavar="DIR", nargs='*',
                        help="Path(s) of the folder(s) containing GeoDeepLearning's training results.")
    parser.add_argument("-st", "--stat",
                        choices=['val_fscore', 'val_loss', 'val_precision', 'val_recall'],
                        help="Statistic to plot (for type of plots with stat in their name).")
    parser.add_argument("-x", "--xextent", metavar="XVALUE", nargs=2, type=float,
                        help="Minimum and maximum of the horizontal axis.")
    parser.add_argument("-y", "--yextent", metavar="YVALUE",nargs=2, type=float,
                        help="Minimum and maximum of the vertical axis.")
    parser.add_argument("-sv", "--save", action="store_true", 
                        help="If called, save plots in the folder(s).")
    args = parser.parse_args()
    
    # Checking validity of the folders
    for folder in args.inFolders:
        if not os.path.isdir(folder):
            raise FileNotFoundError(folder)
    
    main(args)
