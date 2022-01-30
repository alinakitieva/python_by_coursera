import csv
import os


class CarBase:
    def __init__(self, brand, photo_file_name, carrying):
        self.brand = brand
        self.photo_file_name = photo_file_name
        self.carrying = float(carrying)
        self.ext = self.get_photo_file_ext()

    def get_photo_file_ext(self):
        ext = os.path.splitext(self.photo_file_name)[-1]
        if ext in ['.jpg', '.jpeg', '.png', '.gif']:
            return ext


class Car(CarBase):

    car_type = 'car'

    def __init__(self, brand, photo_file_name, carrying, passenger_seats_count):
        super().__init__(brand, photo_file_name, carrying)
        self.passenger_seats_count = int(passenger_seats_count)


class Truck(CarBase):

    car_type = 'truck'

    def __init__(self, brand, photo_file_name, carrying, body_whl='0x0x0'):
        super().__init__(brand, photo_file_name, carrying)
        self.body_lwh = body_whl.split('x')
        try:
            length, width, height = (float(i) for i in body_whl.split('x', 2))
        except ValueError:
            length, width, height = .0, .0, .0
        self.body_length = length
        self.body_width = width
        self.body_height = height

    def get_body_volume(self):
        return self.body_length * self.body_width * self.body_height


class SpecMachine(CarBase):

    car_type = 'spec_machine'

    def __init__(self, brand, photo_file_name, carrying, extra):
        super().__init__(brand, photo_file_name, carrying)
        self.extra = extra


def get_car_list(csv_filename):
    digit_items = ['carrying', 'passenger_seats_count']
    car_types = ('car', 'truck', 'spec_machine')
    results = []
    car_list = []
    with open(csv_filename,  encoding='utf-8') as csv_fd:
        reader = csv.DictReader(csv_fd, delimiter=';')
        # убираем все, где нессответствие в carrying and passenger_seats_count
        for row in reader:
            if row['car_type'] in car_types and all((row[i] == '' or isfloat(row[i])) for i in digit_items):
                results.append(row)

    for obj in results:

        if obj['car_type'] == 'car':
            items = ('brand', 'photo_file_name', 'carrying', 'passenger_seats_count')
            if all(obj[i] for i in items):
                car = Car(obj['brand'], obj['photo_file_name'], obj['carrying'], obj['passenger_seats_count'])
                if car.ext:
                    car_list.append(car)

        if obj['car_type'] == 'truck':
            items = ('brand', 'photo_file_name', 'carrying')
            if all(obj[i] for i in items):
                if obj['body_whl']:
                    obj['split_body_whl'] = obj['body_whl'].split('x')
                    if len(obj['split_body_whl']) == 3 and all(isfloat(i) for i in obj['split_body_whl']):
                        truck = Truck(obj['brand'], obj['photo_file_name'], obj['carrying'], body_whl=obj['body_whl'])
                        if truck.ext:
                            car_list.append(truck)
                else:
                    truck = Truck(obj['brand'], obj['photo_file_name'], obj['carrying'])
                    if truck.ext:
                        car_list.append(truck)

        if obj['car_type'] == 'spec_machine':
            items = ('brand', 'photo_file_name', 'carrying', 'extra')
            if all(obj[i] for i in items):
                spec_machine = SpecMachine(obj['brand'], obj['photo_file_name'], obj['carrying'], obj['extra'])
                if spec_machine.ext:
                    car_list.append(spec_machine)

    return car_list


def isfloat(num):
    try:
        float(num)
        return True
    except (ValueError, TypeError):
        return False



if __name__ == "__main__":
    pass
