#! /usr/bin/env python3

#H.armiger.NW_017734614.1 7105 6194     Beta    1.34e-39        321
#H.armiger.NW_017734614.1 7105 6194     Beta    2.99e-28        322
#H.armiger.NW_017734614.1 7105 6194     Beta    3.23e-41        321
#H.armiger.NW_017734614.1 7111 6194     Beta    2.20e-36        319
#H.armiger.NW_017734743.1 13651 12713   Beta    1.11e-29        323
#H.armiger.NW_017734743.1 13666 12611   Beta    2.67e-58        363
#H.armiger.NW_017734743.1 13693 12611   Beta    2.59e-75        380






import argparse






def make_parse():
    parse = argparse.ArgumentParser()
    parse.add_argument("-i", "--input", help = "input file")
    parse.add_argument("-f", "--flank", default = 100, help = "the flank length", type = int)
    args = parse.parse_args()

    return args

def remove(blast_result, flank):
    ID = ""
    result = {}
    START = 0
    END = 0
    flag = 0

    with open (blast_result, "r") as file:
        for line in file:
            
            flag = flag + 1
            line = line.strip()
            array = line.split("\t")
            _id = array[0].split(" ")[0]
            _start = int(array[0].split(" ")[1])
            _end = int(array[0].split(" ")[2])
            _family = array[1]
            _evalue = float(array[2])
            _length = int(array[3])
            if _start > _end:
                _direction = "-"
            else:
                _direction = "+"

            if _id != ID:
                if flag == 1:
                    ID = _id
                    START = _start 
                    END = _end 
                    result["family"] = []
                    result["evalue"] = []
                    result["length"] = []
                    result["family"].append(_family)
                    result["evalue"].append(_evalue)
                    result["length"].append(_length)
                    result["direction"] = _direction
                else:
#                    print(result)
                    family = sorted(result["family"])
                    if max(family, key=family.count) == max(family[::-1], key = family[::-1].count):
                        print("%s %s %s\t%s" %(ID, START, END, max(family, key=family.count)))
                    else:
                        fam = result["family"][result["evalue"].index(min(result["evalue"]))]
                        print("%s %s %s\t%s" %(ID, START, END, fam))
                    ID = _id
                    START = _start
                    END = _end 
                    result["family"] = []
                    result["evalue"] = []
                    result["length"] = []
                    result["family"].append(_family)
                    result["evalue"].append(_evalue)
                    result["length"].append(_length)
                    result["direction"] = _direction


            else:
                if _start in range(min([START, END])-flank, max([START, END])+1+flank) or _end in range(min([START, END])-flank, max([START, END])+1+flank) or ((START+flank) in range(min([_start, _end]), max([_start, _end])+1) and (END+flank) in range(min([_start, _end]), max([_start, _end])+1)):
                    if result["direction"] == "-":
                        if _start > START:
                            START = _start
                    else:
                        if _start < START:
                            START = _start

                    if result["direction"] == "-":
                        if _end < END:
                            END = _end
                    else:
                        if _end > END:
                            END = _end

                    result["family"].append(_family)
                    result["evalue"].append(_evalue)
                    result["length"].append(_length)
                else:
                    family = sorted(result["family"])
                    if max(family, key=family.count) == max(family[::-1], key = family[::-1].count):
                        print("%s %s %s\t%s" %(ID, START, END, max(family, key=family.count)))
                    else:
                        fam = result["family"][result["evalue"].index(min(result["evalue"]))]
                        print("%s %s %s\t%s" %(ID, START, END, fam))

                    START = _start
                    END = _end 
                    result["family"] = []
                    result["evalue"] = []
                    result["length"] = []
                    result["family"].append(_family)
                    result["evalue"].append(_evalue)
                    result["length"].append(_length)
                    result["direction"] = _direction
            

def main():
    args = make_parse()
    blast_result = args.input
    flank = args.flank
    remove(blast_result, flank)


if __name__ == "__main__":
    main()


