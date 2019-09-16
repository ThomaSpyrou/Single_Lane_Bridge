''' This programm simulate a Single Lane Bridge in which cars come from both sides and want to cross to the other
side. Every car is a thread. There are 4 scenarios.'''
import threading
import time
import random


class Car(threading.Thread):
    # constructor of each car (Thread)
    def __init__(self, car_id, car_dir, car_colour, bridge):
        threading.Thread.__init__(self)
        self.car_id = car_id
        self.car_dir = car_dir
        self.car_colour = car_colour
        self.bridge = bridge

    def run(self):
        # method "run", is executed for every car
        self.bridge.cross(self)


class Bridge:
    def __init__(self, selection):
        self.selection = selection
        self.flag = False
        self.blue_count = 0
        self.red_count = 0
        self.lock = threading.Lock()
        self.cond = threading.Condition(self.lock)

    def cross(self, Car):
        # in cross method the user has given their choice(which scenario they want)
        # cross run for every car-thread
        if self.selection == 1:
            # first scenario, cars cross the bridge without restrictions
            # it's possible to crush ( all threads are running)
            print("The car with {} id is on {} side of the bridge\n".format(Car.car_id, Car.car_dir))
            print("The car with {} id and colour {} is crossing the bridge\n".format(Car.car_id, Car.car_colour))
            time.sleep(random.randint(0, 5))
            print("The car with {} id and colour {} crossed the bridge\n".format(Car.car_id, Car.car_colour))
        elif self.selection == 2:
            # one car-thread come to run, it locks the memory and none can run on the same time
            self.lock.acquire()
            print("The car with {} id is on {} side of the bridge\n".format(Car.car_id, Car.car_dir))
            time.sleep(random.randint(0, 5))
            print("The car with {} id and colour {} crossed the bridge\n".format(Car.car_id, Car.car_colour))
            self.lock.release()
        elif self.selection == 3:
            # as the second choice but the cars switching blue -> red -> blue
            self.cond.acquire()
            print("The car with {} id is in {} side of the bridge\n".format(Car.car_id, Car.car_dir))
            try:
                while self.flag is False and Car.car_colour == "blue":
                    self.cond.wait()
                self.flag = True
                self.cond.notify_all()
            finally:
                print("The car with {} id and colour {} crossed the bridge\n".format(Car.car_id, Car.car_colour))
                self.cond.release()
        elif self.selection == 4:
            # safe choise like 3 but if the number of the cars of a team
            # is quite bigger they have an advantage on crossing
            if Car.car_colour == "blue":
                self.blue_count += 1
            else:
                self.red_count += 1

            print("The car with {} id is in {} side of the bridge\n".format(Car.car_id, Car.car_dir))
            time.sleep(random.randint(0, 5))

            if self.red_count - self.blue_count >= 2:
                self.cond.acquire()
                print("1")
                try:
                    while self.flag is True and Car.car_colour == "red":
                        self.cond.wait()
                    self.flag = False
                    self.cond.notify_all()
                finally:
                    print("The car with {} id and colour {} crossed the bridge\n".format(Car.car_id, Car.car_colour))
                    self.cond.release()
                    self.red_count -= 1
            elif self.blue_count - self.red_count >= 2:
                self.cond.acquire()
                print("2")
                try:
                    while self.flag is True and Car.car_colour == "blue":
                        self.cond.wait()
                    self.flag = True
                    self.cond.notify_all()
                finally:
                    print("The car with {} id and colour {} crossed the bridge\n".format(Car.car_id, Car.car_colour))
                    self.cond.release()
                    self.blue_count -= 1
            else:
                self.lock.acquire()
                print("The car with {} id is on {} side of the bridge\n".format(Car.car_id, Car.car_dir))
                time.sleep(random.randint(0, 5))
                print("The car with {} id and colour {} crossed the bridge\n".format(Car.car_id, Car.car_colour))
                self.lock.release()


if __name__ == "__main__":
    # user give their choice and the number of the cars they want
    num = int(input("How many cars do you want ?\n"))
    sc = int(input("Choose a scenario\n1)Unsafe\n2)Safe\n3)Safe and one car from each side at the time\n"
                   "4)Safe and one car from each side at the time more fair\n5)Exit\n"))
    bridge = Bridge(sc)
    cars = []
    # cars is a list of threads
    if sc == 5:
        print("EXIT")
    else:
        if num == 0:
            print("Zero car on the bridge.")
        else:
            for i in range(1, num + 1):
                x = random.randint(0, 1)
                if x == 0:
                    c1 = Car(car_id=i, car_colour="blue", car_dir=1, bridge=bridge)
                else:
                    c1 = Car(car_id=i, car_colour="red", car_dir=0, bridge=bridge)
                c1.start()
                cars.append(c1)

            for c in cars:
                if c is threading.current_thread():
                    continue
                c.join()

            print("Finished with the creation of the cars\n")
