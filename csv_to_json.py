import csv as tsv
import pathlib
import json

# constants
tsv_path = str(pathlib.Path(__file__).parent.absolute()) + '/partners.tsv'
numbers = list(map(lambda x: str(x), range(1, 10)))
plural = {
    'main_service': 'services',
    'photo_service': 'images',
    'ddd_phone': 'phones',
    'phone': 'phones',
    'occupation': 'professions',
    'city': 'cities',
    'state': 'cities'
}
singular = {
    'services': 'service',
    'images': 'image',
    'phones': 'phone',
    'professions': 'profession',
    'cities': 'city'
}


class User:
    def __init__(self):
        self.cities = []
        self.services = []
        self.professions = []
        self.images = []
        self.categories = []
        self.keywords = []
        self.comments = []
        self.phones = []

    def get_singular_name(self, plural_name):
        if(plural_name in singular.keys()):
            return singular[plural_name]
        return plural_name

    def handle_object(self, array, data, name):
        last_item = array[-1]
        singular_name = self.get_singular_name(name)
        if(name not in last_item.keys()):
            array.pop()
            last_item[singular_name] = data
            array.append(last_item)
        else:
            array.append({singular_name: data})

    def set_city(self, data, name):
        if(len(self.cities) > 0):
            self.handle_object(self.cities, data, name)
        else:
            singular_name = self.get_singular_name(name)
            self.cities.append({singular_name: data})

    def set_service(self, data):
        self.services.append({'service': data})

    def set_profession(self, data):
        self.professions.append({'profession': data})

    def set_image(self, data):
        self.images.append(data)

    def set_phone(self, data, name):
        if(len(self.phones) > 0):
            self.handle_object(self.phones, data, name)
        else:
            singular_name = self.get_singular_name(name)
            self.phones.append({singular_name: data})

    def set_plurals(self, data, name):
        if(name == 'services'):
            self.set_service(data)
        elif(name == 'images'):
            self.set_image(data)
        elif(name == 'phones'):
            self.set_phone(data, name)
        elif(name == 'professions'):
            self.set_profession(data)
        elif(name == 'cities'):
            self.set_city(data, name)

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)


# main function
with open(tsv_path, newline='') as tsv_file:
    reader = tsv.reader(tsv_file, delimiter='\t', quotechar='|')
    tsv = list(reader)
    header = tsv.pop(0)
    data = []
    for row in tsv:
        user = User()
        response = {}
        if len(row) == len(header):
            for i, cell in enumerate(row):
                if(header[i][:-1] in plural.keys()):
                    user.set_plurals(cell, plural[header[i][:-1]])
                elif(header[i] in plural.keys()):
                    user.set_plurals(cell, plural[header[i]])
                else:
                    response[header[i]] = cell
            response.update(eval(user.to_json()))
        data.append(response)
    with open('response.json', 'w') as file:
        json.dump(data, file, ensure_ascii=False)
