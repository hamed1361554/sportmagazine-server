"""
Created on Oct 14, 2016

@author: Hamed Zekri
"""

import datetime
from decimal import Decimal

from deltapy.core import DeltaObject, DeltaException, DynamicObject
from deltapy.security.session.services import get_current_user
from deltapy.transaction.services import get_current_transaction_store
from deltapy.utils.storm_aux import entity_to_dic
from server.model import ProductsEntity, UserEntity, ProductsColorsEntity, ProductsSizesEntity
from server.products.helper import generate_product_unique_name
from storm.expr import Select, Count, And, Like, In

import deltapy.unique_id.services as unique_id_services


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
        entity = store.get(ProductsEntity, product_id)

        if entity is None:
            raise ProductsException("Product [{0}] not found".format(product_id))

        return entity

    def get(self, product_id):
        """
        Returns product info.

        :param product_id:
        :return:
        """

        entity = self._get(product_id)
        return DynamicObject(entity_to_dic(entity))

    def get_by_name(self, name, category):
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

        return DynamicObject(entity_to_dic(entity))

    def _validate_product_unique_name(self, name, category):
        """
        Validates product name uniqueness.
        """

        unique_name = generate_product_unique_name(name, category)

        store = get_current_transaction_store()
        result = \
            store.execute(Select(columns=[Count(1)],
                                 where=And(ProductsEntity.product_unique_name == unique_name),
                                 tables=[ProductsEntity])).get_one()

        if result is None:
            return

        result, = result
        if result > 0:
            raise ProductsException("Please select another name for product.")

    def create(self, name, price, category, colors, sizes, **options):
        """
        Creates product.

        :param name:
        :param price:
        :param category:
        :param sizes:
        :param colors:
        :param options:
        :return:
        """

        if name is None or name.strip() == "":
            raise ProductsException("Product name could not be nothing.")

        if price is None or price.strip() == "":
            raise ProductsException("Product price could not be nothing.")

        if colors is None or len(colors) <= 0:
            raise ProductsException("At least one color for product should be selected.")

        if sizes is None or len(sizes) <= 0:
            raise ProductsException("At least one size for product should be selected.")

        current_user = get_current_user()
        if current_user.user_production_type != UserEntity.UserProductionTypeEnum.PRODUCER:
            raise ProductsException("Consumer user can not create product.")

        self._validate_product_unique_name(name, category)

        product = ProductsEntity()
        product.product_id = unicode(unique_id_services.get('uuid'))
        product.product_name = name
        product.product_price = Decimal(price)
        product.product_category = category
        product.product_image = buffer(options.get('image_data'))
        product.product_producer_user_id = current_user.id
        status = options.get('status')
        if status is None:
            status = ProductsEntity.ProductStatusEnum.IN_STOCK
        product.product_status = status
        product.product_unique_name = generate_product_unique_name(name, category)
        product.product_creation_date = datetime.datetime.now()

        store = get_current_transaction_store()
        store.add(product)

        for color in colors:
            color_entity = ProductsColorsEntity()
            color_entity.product_color_id = unicode(unique_id_services.get('uuid'))
            color_entity.product_id = product.product_id
            color_entity.product_color_hex = unicode(color)
            store.add(color_entity)

        for size in sizes:
            size_entity = ProductsSizesEntity()
            size_entity.product_size_id = unicode(unique_id_services.get_id('uuid'))
            size_entity.product_id = product.product_id
            size_entity.product_size = unicode(size)
            store.add(size_entity)

        return DynamicObject(entity_to_dic(product))

    def update(self, id, **options):
        """
        Updates product.

        :param id:
        :param options:
        :return:
        """

        entity = self._get(id)

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

        return DynamicObject(entity_to_dic(entity))

    def find(self, **options):
        """
        Searches products.

        :param optiosn:
        :return:
        """

        from_creation_date = options.get('from_creation_date')
        to_creation_date = options.get('to_creation_date')
        from_price = options.get('from_price')
        to_price = options.get('to_price')
        name = options.get('name')
        categories = options.get('categories')
        include_out_of_stock = options.get('include_out_of_stock')
        if include_out_of_stock is None:
            include_out_of_stock = False

        expressions = []
        if not include_out_of_stock:
            expressions.append(ProductsEntity.product_status == ProductsEntity.ProductStatusEnum.IN_STOCK)
        if from_creation_date is not None:
            expressions.append(ProductsEntity.product_creation_date >= from_creation_date)
        if to_creation_date is not None:
            expressions.append(ProductsEntity.product_creation_date <= to_creation_date)
        if from_price is not None:
            expressions.append(ProductsEntity.product_price >= from_price)
        if to_price is not None:
            expressions.append(ProductsEntity.product_price >= to_price)
        if name is not None and name.strip() != "":
            expressions.append(Like(ProductsEntity.product_name, "%{0}%".format(name)))
        if categories is not None and len(categories) > 0:
            expressions.append(In(ProductsEntity.product_category, categories))

        store = get_current_transaction_store()
        entities = store.find(ProductsEntity, And(*expressions)).order_by(ProductsEntity.product_creation_date)

        results = []
        for entity in entities:
            results.append(DynamicObject(entity_to_dic(entity)))

        return results
