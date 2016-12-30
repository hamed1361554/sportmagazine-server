"""
Created on Oct 14, 2016

@author: Hamed Zekri
"""

import datetime
from decimal import Decimal
from dateutil import parser

from storm import Undef
from storm.expr import Select, Count, And, Like, In, Desc, Exists

from deltapy.core import DeltaObject, DeltaException, DynamicObject
from deltapy.security.session.services import get_current_user
from deltapy.transaction.services import get_current_transaction_store
from deltapy.utils.storm_aux import entity_to_dic
from server.model import UserEntity, ProductsEntity, ProductsColorsEntity, ProductsSizesEntity, ProductsBrandsEntity
from server.products.helper import generate_product_unique_name

import deltapy.unique_id.services as unique_id_services
import server.products.history.services as history_services
from werkzeug.wsgi import extract_path_info


class ProductsException(DeltaException):
    """
    Products Exception
    """


class ProductsManager(DeltaObject):
    """
    Products Manager
    """

    def _get(self, product_id):
        """
        Returns product entity.

        :param product_id:
        :return:
        """

        store = get_current_transaction_store()
        entity = store.get(ProductsEntity, unicode(product_id))

        if entity is None:
            raise ProductsException("Product [{0}] not found".format(product_id))

        return entity

    def get(self, product_id, **options):
        """
        Returns product info.

        :param product_id:
        :return:
        """

        entity = self._get(product_id)
        product = DynamicObject(entity_to_dic(entity))

        fetch_details = options.get('fetch_details')
        if fetch_details is None:
            fetch_details = True

        if fetch_details:
            store = get_current_transaction_store()

            product.colors = []
            colors = store.find(ProductsColorsEntity, ProductsColorsEntity.product_id == product_id)
            product.colors.extend([DynamicObject(entity_to_dic(e)) for e in colors])

            product.sizes = []
            sizes = store.find(ProductsSizesEntity, ProductsSizesEntity.product_id == product_id)
            product.sizes.extend([DynamicObject(entity_to_dic(e)) for e in sizes])

            product.brands = []
            brands = store.find(ProductsBrandsEntity, ProductsBrandsEntity.product_id == product_id)
            product.brands.extend([DynamicObject(entity_to_dic(e)) for e in brands])

        return product

    def get_by_name(self, name, category, **options):
        """
        Returns product info.

        :param category:
        :param name:
        :return:
        """

        unique_name = generate_product_unique_name(name, category)

        store = get_current_transaction_store()
        entity = store.find(ProductsEntity,
                            ProductsEntity.product_unique_name == unique_name).one()

        if entity is None:
            raise ProductsException("Product [{0}] not found".format(name))

        product = DynamicObject(entity_to_dic(entity))

        fetch_details = options.get('fetch_details')
        if fetch_details is None:
            fetch_details = True

        if fetch_details:
            store = get_current_transaction_store()

            product.colors = []
            colors = store.find(ProductsColorsEntity, ProductsColorsEntity.product_id == product.product_id)
            product.colors.extend([DynamicObject(entity_to_dic(e)) for e in colors])

            product.sizes = []
            sizes = store.find(ProductsSizesEntity, ProductsSizesEntity.product_id == product.product_id)
            product.sizes.extend([DynamicObject(entity_to_dic(e)) for e in sizes])

            product.brands = []
            brands = store.find(ProductsBrandsEntity, ProductsBrandsEntity.product_id == product.product_id)
            product.brands.extend([DynamicObject(entity_to_dic(e)) for e in brands])

        return product

    def _validate_product_unique_name(self, name, category):
        """
        Validates product name uniqueness.
        """

        unique_name = generate_product_unique_name(name, category)

        store = get_current_transaction_store()
        result = \
            store.execute(Select(columns=[Count(1)],
                                 where=And(ProductsEntity.product_unique_name == unicode(unique_name)),
                                 tables=[ProductsEntity])).get_one()

        if result is None:
            return

        result, = result
        if result > 0:
            raise ProductsException("Please select another name for product.")

    def create(self, name, price, category, colors, sizes, brands, **options):
        """
        Creates product.

        :param name:
        :param price:
        :param category:
        :param colors:
        :param sizes:
        :param brands:
        :param options:
        :return:
        """

        if name is None or name.strip() == "":
            raise ProductsException("Product name could not be nothing.")

        if price is None or price <= 1000:
            raise ProductsException("Product price could not be nothing or invalid.")

        if colors is None or len(colors) <= 0:
            raise ProductsException("At least one color for product should be selected.")

        if sizes is None or len(sizes) <= 0:
            raise ProductsException("At least one size for product should be selected.")

        if brands is None or len(brands) <= 0:
            raise ProductsException("At least one brand for product should be selected.")

        current_user = get_current_user()
        if current_user.user_production_type != UserEntity.UserProductionTypeEnum.PRODUCER:
            raise ProductsException("Consumer user can not create product.")

        self._validate_product_unique_name(name, category)

        product = ProductsEntity()
        product.product_id = unicode(unique_id_services.get_id('uuid'))
        product.product_name = name
        product.product_price = Decimal(price)
        product.product_category = category
        product.product_producer_user_id = current_user.id
        product.product_unique_name = unicode(generate_product_unique_name(name, category))
        product.product_creation_date = datetime.datetime.now()

        product_image = options.get('image')
        if product_image not in (None, ""):
            product.product_image = str(product_image)

        status = options.get('status')
        if status is None:
            status = ProductsEntity.ProductStatusEnum.IN_STOCK
        product.product_status = status

        counter = options.get('counter')
        if counter is None:
            counter = 0
        product.product_counter = counter

        age_category = options.get('age_category')
        if age_category is None:
            age_category = ProductsEntity.ProductAgeCategoryEnum.ADULT
        product.product_age_category = age_category

        gender = options.get('gender')
        if gender is None:
            gender = ProductsEntity.ProductGenderEnum.BOTH
        product.product_gender = gender

        wholesale_type = options.get('wholesale_type')
        if wholesale_type is None:
            wholesale_type = ProductsEntity.ProductWholesaleTypeEnum.RETAIL
        product.product_whole_sale_type = wholesale_type

        comment = options.get("comment")
        if comment is not None and len(comment) > 0:
            product.product_comment = comment

        store = get_current_transaction_store()
        store.add(product)

        for color in colors:
            if color == "":
                continue
            color_entity = ProductsColorsEntity()
            color_entity.product_color_id = unicode(unique_id_services.get_id('uuid'))
            color_entity.product_id = product.product_id
            color_entity.product_color_hex = unicode(color.strip())
            store.add(color_entity)

        for size in sizes:
            if size == "":
                continue
            size_entity = ProductsSizesEntity()
            size_entity.product_size_id = unicode(unique_id_services.get_id('uuid'))
            size_entity.product_id = product.product_id
            size_entity.product_size = unicode(size.strip())
            store.add(size_entity)

        for brand in brands:
            if brand == "":
                continue
            brand_entity = ProductsBrandsEntity()
            brand_entity.product_brand_id = unicode(unique_id_services.get_id('uuid'))
            brand_entity.product_id = product.product_id
            brand_entity.product_brand = unicode(brand.strip())
            store.add(brand_entity)

        history_services.write_history(product, colors, sizes, brands, **options)

        return DynamicObject(entity_to_dic(product))

    def update(self, id, **options):
        """
        Updates product.

        :param id:
        :param options:
        :return:
        """

        entity = self._get(id)
        store = get_current_transaction_store()

        new_name = options.get('name')
        if new_name is not None and new_name.strip() != "":
            self._validate_product_unique_name(new_name, entity.product_category)
            entity.product_name = new_name
            entity.product_unique_name = generate_product_unique_name(new_name, entity.product_category)

        new_price = options.get('price')
        if new_price is not None and new_price >= 0:
            entity.product_price = new_price

        new_image = options.get('image_data')
        if new_image is not None:
            entity.product_image = buffer(new_image)

        new_status = options.get('status')
        if new_status is None:
            entity.product_status = new_status

        colors = options.get('colors')
        if colors is not None and len('colors') > 0:
            already_colors = store.find(ProductsColorsEntity, ProductsColorsEntity.product_id == entity.product_id)

            to_delete = []
            for c in already_colors:
                if c.product_color_hex not in colors:
                    to_delete.append(c)

            to_insert = []
            for c in colors:
                if c not in [a.product_color_hex for a in already_colors]:
                    to_insert.append(c)

            for d in to_delete:
                store.remove(d)

            for i in to_insert:
                color_entity = ProductsColorsEntity()
                color_entity.product_color_id = unicode(unique_id_services.get('uuid'))
                color_entity.product_id = entity.product_id
                color_entity.product_color_hex = unicode(i)
                store.add(color_entity)

        sizes = options.get('sizes')
        if sizes is not None and len(sizes) > 0:
            already_sizes = store.find(ProductsSizesEntity, ProductsSizesEntity.product_id == entity.product_id)

            to_delete = []
            for s in already_sizes:
                if s.product_size not in sizes:
                    to_delete.append(s)

            to_insert = []
            for s in sizes:
                if s not in [a.product_size for a in already_sizes]:
                    to_insert.append(s)

            for d in to_delete:
                store.remove(d)

            for i in to_insert:
                size_entity = ProductsSizesEntity()
                size_entity.product_size_id = unicode(unique_id_services.get_id('uuid'))
                size_entity.product_id = entity.product_id
                size_entity.product_size = unicode(i)
                store.add(size_entity)

        brands = options.get('brands')
        if brands is not None and len(brands) > 0:
            already_brands = store.find(ProductsBrandsEntity, ProductsBrandsEntity.product_id == entity.product_id)

            to_delete = []
            for b in already_brands:
                if b.product_brand not in brands:
                    to_delete.append(b)

            to_insert = []
            for b in brands:
                if b not in [a.product_brand for a in already_brands]:
                    to_insert.append(b)

            for d in to_delete:
                store.remove(d)

            for i in to_insert:
                brand_entity = ProductsBrandsEntity()
                brand_entity.product_brand_id = unicode(unique_id_services.get_id('uuid'))
                brand_entity.product_id = entity.product_id
                brand_entity.product_brand = unicode(i)
                store.add(brand_entity)

        product = DynamicObject(entity_to_dic(entity))
        product.sizes = []
        product.colors = []
        product.brands = []

        history_services.write_history(entity, colors, sizes, brands, **options)

        return product

    def find(self, **options):
        """
        Searches products.

        :param optiosn:
        :return:
        """

        current_user = get_current_user()

        from_creation_date = options.get('from_creation_date')
        to_creation_date = options.get('to_creation_date')
        from_price = options.get('from_price')
        to_price = options.get('to_price')
        name = options.get('name')
        size = options.get('size')
        brand = options.get('brand')
        categories = options.get('categories')
        if not isinstance(categories, (list, tuple)):
            categories = [categories]
        age_categories = options.get('age_categories')
        if not isinstance(age_categories, (list, tuple)):
            age_categories = [age_categories]
        gender = options.get('gender')
        if not isinstance(gender, (list, tuple)):
            gender = [gender]
        include_out_of_stock = options.get('include_out_of_stock')
        if include_out_of_stock is None:
            include_out_of_stock = False
        wholesale_type = options.get('wholesale_type')
        if wholesale_type not in (None, -1):
            wholesale_type = ProductsEntity.ProductWholesaleTypeEnum.RETAIL
        if wholesale_type == ProductsEntity.ProductWholesaleTypeEnum.WHOLESALE:
            if current_user.user_production_type != UserEntity.UserProductionTypeEnum.PRODUCER:
                raise ProductsException("Consumer user can not search wholesale products.")
        just_current_user = options.get('just_current_user')
        if just_current_user is None:
            just_current_user = False
        if just_current_user and current_user.user_production_type != UserEntity.UserProductionTypeEnum.PRODUCER:
            raise ProductsException("Consumer user can not search its own products.")

        expressions = []
        if not include_out_of_stock:
            expressions.append(ProductsEntity.product_status == ProductsEntity.ProductStatusEnum.IN_STOCK)
        if from_creation_date is not None:
            if not isinstance(from_creation_date, datetime.datetime):
                from_creation_date = parser.parse(from_creation_date)
            expressions.append(ProductsEntity.product_creation_date >= from_creation_date)
        if to_creation_date is not None:
            if not isinstance(to_creation_date, datetime.datetime):
                to_creation_date = parser.parse(to_creation_date)
            expressions.append(ProductsEntity.product_creation_date <= to_creation_date)
        if from_price not in (None, 0, "", "0"):
            expressions.append(ProductsEntity.product_price >= Decimal(from_price))
        if to_price not in (None, 0, "", "0"):
            expressions.append(ProductsEntity.product_price <= Decimal(to_price))
        if name is not None and name.strip() != "":
            name = unicode(name)
            expressions.append(Like(ProductsEntity.product_name, "%{0}%".format(name.strip())))
        if size is not None and size.strip() != "":
            size = unicode(size)
            expressions.append(Exists(Select(columns=[1],
                                             where=And(ProductsSizesEntity.product_id == ProductsEntity.product_id,
                                                       Like(ProductsSizesEntity.product_size, "%{0}%".format(size.strip()))),
                                             tables=[ProductsSizesEntity])))
        if brand is not None and brand.strip() != "":
            brand = unicode(brand)
            expressions.append(Exists(Select(columns=[1],
                                             where=And(ProductsBrandsEntity.product_id == ProductsEntity.product_id,
                                                       Like(ProductsBrandsEntity.product_brand, "%{0}%".format(brand.strip()))))))
        if categories is not None and len(categories) > 0 and -1 not in categories:
            expressions.append(In(ProductsEntity.product_category, categories))
        if age_categories is not None and len(age_categories) > 0 and -1 not in age_categories:
            expressions.append(In(ProductsEntity.product_age_category, age_categories))
        if gender is not None and len(gender) > 0 and -1 not in gender:
            expressions.append(In(ProductsEntity.product_gender, gender))
        if just_current_user:
            expressions.append(ProductsEntity.product_producer_user_id == current_user.id)

        offset = options.get("__offset__")
        if offset is None:
            offset = 0
        else:
            offset = int(offset)
        limit = options.get("__limit__")
        if limit in (None, 0):
            limit = Undef
        else:
            limit = int(limit)

        statement = \
            Select(columns=[ProductsEntity.product_id,
                            ProductsEntity.product_name,
                            ProductsEntity.product_category,
                            ProductsEntity.product_image,
                            ProductsEntity.product_age_category,
                            ProductsEntity.product_comment,
                            ProductsEntity.product_creation_date,
                            ProductsEntity.product_price,
                            ProductsEntity.product_gender],
                   where=And(*expressions),
                   tables=[ProductsEntity],
                   order_by=[Desc(ProductsEntity.product_creation_date)],
                   offset=offset,
                   limit=limit)

        store = get_current_transaction_store()

        results = []
        for (product_id,
             product_name,
             product_category,
             product_image,
             product_age_category,
             product_comment,
             product_creation_date,
             product_price,
             product_gender) in store.execute(statement):
            results.append(DynamicObject(product_id=product_id,
                                         product_name=product_name,
                                         product_category=product_category,
                                         product_image=product_image,
                                         product_age_category=product_age_category,
                                         product_comment=product_comment,
                                         product_creation_date=product_creation_date,
                                         product_price=product_price,
                                         product_gender=product_gender,
                                         product_colors=self.get_product_colors(product_id, concat_results=True),
                                         product_sizes=self.get_product_sizes(product_id, concat_results=True),
                                         product_brands=self.get_product_brands(product_id, concat_results=True)))

        return results

    def decrease_product_counter(self, product_id, **options):
        """
        Decreases product counter.

        :param product_id:
        :return:
        """

        entity = self._get(product_id)

        counter = options.get('counter')
        decrease = options.get('decrease')

        if counter is not None:
            entity.product_counter = counter
        elif decrease is not None:
            entity.product_counter = entity.product_counter - decrease
        else:
            entity.product_counter = entity.product_counter - 1

        if entity.product_counter < 0:
            raise ProductsException("Not possible to decrease counter with value [{0}], already is [{1}]".format(counter or decrease and 1,
                                                                                                                 entity.product_counter))

        return entity.product_counter

    def get_product_colors(self, product_id, **options):
        '''
        Returns product colors.

        :param product_id:
        :return:
        '''

        store = get_current_transaction_store()

        statement = \
            Select(columns=[ProductsColorsEntity.product_color_hex,
                            ProductsColorsEntity.product_color_id],
                   where=And(ProductsColorsEntity.product_id == product_id),
                   tables=[ProductsColorsEntity])

        results = []
        for (product_color_hex,
             product_color_id) in store.execute(statement):
            results.append(DynamicObject(product_color_hex=product_color_hex,
                                         product_color_id=product_color_id))

        concat_results = options.get('concat_results')
        if concat_results is None:
            concat_results = False

        if concat_results:
            return ','.join([c.product_color_hex for c in results])

        return results

    def get_product_sizes(self, product_id, **options):
        '''
        Returns product sizes.

        :param product_id:
        :return:
        '''

        store = get_current_transaction_store()

        statement = \
            Select(columns=[ProductsSizesEntity.product_size,
                            ProductsSizesEntity.product_size_id],
                   where=And(ProductsSizesEntity.product_id == product_id),
                   tables=[ProductsSizesEntity])

        results = []
        for (product_size,
             product_size_id) in store.execute(statement):
            results.append(DynamicObject(product_size=product_size,
                                         product_size_id=product_size_id))

        concat_results = options.get('concat_results')
        if concat_results is None:
            concat_results = False

        if concat_results:
            return ','.join([s.product_size for s in results])

        return results

    def get_product_brands(self, product_id, **options):
        '''
        Returns product brands.

        :param product_id:
        :return:
        '''

        store = get_current_transaction_store()

        statement = \
            Select(columns=[ProductsBrandsEntity.product_brand,
                            ProductsBrandsEntity.product_brand_id],
                   where=And(ProductsBrandsEntity.product_id == product_id),
                   tables=[ProductsBrandsEntity])

        results = []
        for (product_brand,
             product_brand_id) in store.execute(statement):
            results.append(DynamicObject(product_brand=product_brand,
                                         product_brand_id=product_brand_id))

        concat_results = options.get('concat_results')
        if concat_results is None:
            concat_results = False

        if concat_results:
            return ','.join([b.product_brand for b in results])

        return results