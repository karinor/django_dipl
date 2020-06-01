from django.conf import settings
from .models import Product, Field, FieldType
from account.models import Compare as CompModel
from pprint import pprint


class Compare:
    def __init__(self, request):
        self.session = request.session
        compare = self.session.get(settings.COMPARE_SESSION_ID)
        if not compare:
            compare = self.session[settings.COMPARE_SESSION_ID] = []
        self.compare = compare

    def get(self):
        return Product.objects.filter(id__in=self.compare)

    def add(self, product_id):
        if not product_id in self.compare:
            self.compare.append(product_id)
            self._save()
    
    def remove(self, product_id):
        if product_id in self.compare:
            self.compare.remove(product_id)
            self._save()

    def get_formatted_data(self):
        formatted_data = dict()
        fields = Field.objects.filter(product__id__in=self.compare)
        field_len_indexes = {}
        for index, field in enumerate(fields):
            field_type = field.field_type.title
            if field_type not in formatted_data:
                formatted_data[field_type] = [' ' for e in range(0, index - 1)] + [field.value, ]
                field_len_indexes[field_type] = index
            else:
                formatted_data[field_type] += [' ' for e in range(field_len_indexes[field_type], index - 2)]
                formatted_data[field_type].append(field.value)
                field_len_indexes[field_type] = index
        return formatted_data
    
    def _save(self):
        self.session[settings.COMPARE_SESSION_ID] = self.compare
        self.session.modified = True

    def _clear(self):
        self.session[settings.COMPARE_SESSION_ID] = []
        self.session.modified = True
    
    def __iter__(self):
        for item in self.compare:
            yield int(item)
    
    def __len__(self):
        return len(self.compare)


class CompareAuth:
    def __init__(self, request):
        self.request = request
        self.session = request.session
        session_comp = Compare(request)
        if len(session_comp) > 0:
            model_objects = CompModel.objects.filter(user=request.user)
            model_ids = [
                compare.product.pk for compare in model_objects
            ]
            session_ids = tuple(iter(session_comp))
            session_comp._clear()
            session_ids_set = set(session_ids)
            model_ids_set = set(model_ids)
            compare_intersection = model_ids_set | session_ids_set
            ids_for_add = list(compare_intersection - model_ids_set)
            products_for_add = Product.objects.filter(id__in=ids_for_add)
            create_compares = CompModel.objects.bulk_create(
                CompModel(user=request.user, pruduct=pruduct) for pruduct in products_for_add
            )
        self.compare = [
            compare.product.pk for compare in CompModel.objects.filter(user=request.user)
        ]
        print(self.compare)
        self._save()

    def get(self):
        return Product.objects.filter(id__in=self.compare)

    def add(self, product_id):
        if not CompModel.objects.filter(user=self.request.user, product_id=product_id).exists():
            added = CompModel.objects.create(user=self.request.user, product_id=product_id)
            added.save()
            if product_id not in self.compare:
                self.compare.append(added.id)
                self._save()

    def remove(self, product_id):
        if CompModel.objects.filter(user=self.request.user, product_id=product_id).exists():
            removed = CompModel.objects.filter(user=self.request.user, product_id=product_id)
            self.compare.remove(removed[0].product.id)
            removed.delete()
            self._save()

    def _clear(self):
        self.compare = []
        CompModel.objects.filter(user=self.request.user).delete()

    def get_formatted_data(self):
        formatted_data = dict()
        fields = Field.objects.filter(product_id__in=self.compare)
        field_len_indexes = {}
        for index, field in enumerate(fields):
            field_type = field.field_type.title
            if field_type not in formatted_data:
                formatted_data[field_type] = [' ' for e in range(0, index - 1)] + [field.value, ]
                field_len_indexes[field_type] = index
            else:
                formatted_data[field_type] += [' ' for e in range(field_len_indexes[field_type], index - 2)]
                formatted_data[field_type].append(field.value)
                field_len_indexes[field_type] = index
        pprint(formatted_data)
        return formatted_data

    def _save(self):
        self.session[settings.COMPARE_SESSION_ID] = self.compare
        self.session.modified = True

    def __iter__(self):
        for item in self.compare:
            yield item

    def __len__(self):
        return len(self.compare)




