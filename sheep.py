def counting_sheep (numbr_int, mult, tracker):
   to_check = numbr_int * mult
   to_check = str(to_check)
   for char in to_check:
       if char not in tracker:
           tracker.append(char)
           
   if len(tracker) == 10:  
       return to_check
   
   return counting_sheep(numbr_int, mult + 1, tracker)

def main ():
    with open('result.txt', 'w') as f:
     with open('A-large-practice.in.txt', 'r') as fr:
        for line in f.readlines():
            numbr_int = int(line.replace('\n', '').strip())

            if numbr_int == 0:
                fr.write(str('INSOMNIA'))

            mult = 1
            tracker = []
            result =counting_sheep(numbr_int, mult, tracker)

            fr.write(str(result))   

if  __name__ == "__main__":
    main()