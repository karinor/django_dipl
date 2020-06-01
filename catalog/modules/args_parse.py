
class Parse:
    def __init__(self, get_args):
        self.get = get_args.items()
        self.price_min = 0
        self.price_max = 0
        self.brand = []
        self.country = []
        self.field_type = []
        self.field_value = []
        self.sort = ''

    def parse_args(self):
        for key, value in self.get:
            if key == 'price-min':
                self.price_min = value
            elif key == 'price-max':
                self.price_max = value
            elif key.startswith('brand'):
                self.brand.append(key[5:])
            elif key.startswith('country'):
                self.country.append(key[7:])
            elif key.startswith('field'):
                self.field_type.append(key[5:])
                self.field_value.append(value)
            if key == 'sort':
                self.sort = value
    
        
    