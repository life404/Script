#! /usr/bin/env python3

import argparse
import os
from collections import Counter
import multiprocessing

def make_args():
    parse = argparse.ArgumentParser()
    parse.add_argument("--input", "-i", help = "Input directory")
    parse.add_argument("--order", "-o", default = "none", help = "The gene you interst")
    args = parse.parse_args()
    return args

def manage_file(input_dir, order):
    if order == "none":
        files = sorted([SQLtable for SQLtable in os.listdir(input_dir) if "SQLtable" in SQLtable])
    else:
        files = []
        for i in range(0, (len(order.split(" "))-1)):
            for j in range(i+1, len(order.split(" "))):
                files.append("SQLtable."+order.split(" ")[i]+"-"+order.split(" ")[j])

    tmp = open(os.path.join(input_dir, "all.orthologous"), "w")
    for SQLtable in files: 
        flag = ""
        target = ""
        with open (os.path.join(input_dir, SQLtable), "r") as file:
            for line in file:
                array = line.strip().split("\t")
                if flag != array[0]:
                    target = array[-1]
                    flag = array[0]
                else:
                    tmp.write(target+"\t"+array[-1]+"\n")
    tmp.close()
    print("Finish manage file")
    print("****************************************************")


def copy_num(input_dir):
    all_inparanoid = []
    for tmp in [i for i in os.listdir(input_dir) if ".tmp" in i]:
        with open (os.path.join(input_dir, tmp), "r") as file:
            for line in file:
                all_inparanoid.append(line.strip())

    orthologous = {}
    orthologous["group1"] = []
    orthologous["group1"].append(all_inparanoid[0].split("\t")[0])
    orthologous["group1"].append(all_inparanoid[0].split("\t")[1])

    group_num = 1
    num = 0
    for ortho in all_inparanoid[1:]:
        array = ortho.split("\t")

        flag_in = 0
        for key in orthologous.keys():
            if array[1] in orthologous[key] or array[0] in orthologous[key]:
                flag_in = 1
                orthologous[key].append(array[0])
                orthologous[key].append(array[1])
                continue
            else:
                flag_in = 0
            

        if flag_in == 0:
            group_num = group_num + 1
            orthologous["group"+str(group_num)] = []
            orthologous["group"+str(group_num)].append(array[0])
            orthologous["group"+str(group_num)].append(array[1])
        
        num = num +1 
        print("%d\r" %num, end = "")

    print(orthologous)
           
def copy_num_thread(input_dir, threads):
    threads = 100
    all_inparanoid = []
    for tmp in [i for i in os.listdir(input_dir) if ".tmp" in i]:
        with open (os.path.join(input_dir, tmp), "r") as file:
            for line in file:
                all_inparanoid.append(line.strip())

    group_num = 1
    tmp = open(os.path.join(input_dir, "group1"), "w")
    tmp.write(all_inparanoid[0].split("\t")[0])
    tmp.write("\n")
    tmp.write(all_inparanoid[0].split("\t")[1])
    tmp.write("\n")
    tmp.close()
    
    ortho_num = 0
    for ortho in all_inparanoid[1:]:
        group_files = [group for group in os.listdir(input_dir) if "group" in group]
        array = ortho.split("\t")

        return_r = []
        if len(group_files) > threads:
            pool = multiprocessing.Pool(threads)
            for group_file in group_files:
                r = pool.apply_async(copy_num_thread_process, args = (input_dir, group_file, array))
                return_r.append(r.get())
            pool.close()
            pool.join()
        else:
            for group_file in group_files:
                r = copy_num_thread_process(input_dir, group_file, array)
                return_r.append(r)

        if sum(return_r) == 0:
            group_num  = group_num + 1
            copy_num_write(input_dir, group_num, array)
    
        ortho_num += 1
        print("Analysising: %s             ortho: %d      group file %s\r" %(ortho, ortho_num, len(group_files)), end="")

    
def copy_num_thread_process(input_dir, group_file, array):
    content = open(os.path.join(input_dir, group_file), "r").read()
    tmp = open (os.path.join(input_dir, group_file), "a")
    if array[0] in content or array[1] in content:
        tmp.write(array[0])
        tmp.write("\n")
        tmp.write(array[1])
        tmp.write("\n")
        return 1
    else:
        return 0
    tmp.close()

def copy_num_write(input_dir, group_num, array):
    tmp = open(os.path.join(input_dir, "group"+str(group_num)), "w")
    tmp.write(array[0])
    tmp.write("\n")
    tmp.write(array[1])
    tmp.write("\n")
    tmp.close()

def copy_num_2(input_dir):
    all_inparanoid = []
    with open (os.path.join(input_dir, "all.orthologous"), "r") as file:
        for line in file:
            all_inparanoid.append(line.strip())
    print("Finish merge all orthologous")
    print("****************************************************")
    print("Begin grouping orthologous")
    group_num = 1
    orthologous = {}
    ortho_num = 0
    for ortho in all_inparanoid:
        array = ortho.split("\t")
        if array[1] in orthologous.keys():
            orthologous[array[0]] = orthologous[array[1]]
        elif array[0] in orthologous.keys():
            orthologous[array[1]] = orthologous[array[0]]
        elif array[1] not in orthologous.keys() and array[0] not in orthologous.keys():
            orthologous[array[0]] = "group"+str(group_num)
            orthologous[array[1]] = "group"+str(group_num)
            group_num += 1
        else:
            continue
        ortho_num +=1
        print("the %dth orthologous\r" %(ortho_num), end="")
    print("Finish grouping")
    print("****************************************************")
    print("Begin write group information into file `group`")

#    for key, value in orthologous.items():
#        print("%s:%s"%(key, value))

    
    group = open(os.path.join(input_dir, "groups"), "w")
    num = 0
    for i in set(list(orthologous.values())):
        num += 1
        group.write("%s: " %i)
        for key in orthologous.keys():
            if orthologous[key] == i:
                group.write("%s " %(key))
        group.write("\n")
        print("writing group: %s (%d)\r" %(i, num), end="")
    group.close()
    
    print("Begin write group copy number into file `copy.num`")
    species = sorted(set([i.split("|")[0] for i in orthologous.keys()]))

    group_num = open(os.path.join(input_dir, "copy.number"), "w")
    group_num.write("groups ")
    for i in species:
        group_num.write("%s " %i)
    group_num.write("\n")

    num = 0
    for i in set(list(orthologous.values())):
        num += 1
        num_list = []
        group_num.write("%s: " %i)
        for key in orthologous.keys():
            if orthologous[key] == i:
                num_list.append(key.split("|")[0])
        for specie in species:
            group_num.write("%d " %(num_list.count(specie)))
        group_num.write("\n")
        print("writing group: %s (%d)\r" %(i, num), end="")
    group_num.close()




def main():
    args = make_args()
    input_dir = args.input
    order = args.order
#    os.remove(os.path.join(input_dir, "*.tmp"))
#   gene = args.gene
#   threads = 10
    manage_file(input_dir, order)
    copy_num_2(input_dir)

if __name__ == "__main__":
    main()
