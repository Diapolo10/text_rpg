import os
import time

#last_stats = ""
#print("Hai")
def main():
    while True:
        with open('temp.gui') as f:
            #if f.read() != last_stats:
            last_stats = f.read()
            os.system('cls')
            print(last_stats)
        time.sleep(.1)

if __name__ == "__main__":
    main()
