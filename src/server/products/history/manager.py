"""
Created on Oct 18, 2016

@author: Hamed Zekri
"""

import datetime

from storm.expr import Like, In, And

from deltapy.core import DeltaObject, DeltaException, DynamicObject
from deltapy.transaction.services import get_current_transaction_store
from deltapy.utils.storm_aux import entity_to_dic
import deltapy.unique_id.services as unique_id_services

from server.model import ProductsHistoryEntity


class ProductsHistoryException(DeltaException):
    """
    Products History Exception
    """


class ProductsHistoryManager(DeltaObject):
    """
    Products History Manager
    """

    def _get(self, product_history_id):
        """
        Returns product history entity.

        :param product_history_id:
        :return:
        """

        store = get_current_transaction_store()
        entity = store.get(ProductsHistoryEntity, product_history_id)

        if entity is None:
            raise ProductsHistoryException("Product history [{0}] not found.".format(product_history_id))

        return entity

    def get(self, product_history_id):
        """
        Returns product history info.

        :param product_history_id:
        :return:
        """

        entity = self._get(product_history_id)
        return DynamicObject(entity_to_dic(entity))

    def find(self, **options):
        """
        Searches product histories.

        :param optiosn:
        :return:
        """

        from_edit_date = options.get('from_edit_date')
        to_edit_date = options.get('to_edit_date')
        from_price = options.get('from_price')
        to_price = options.get('to_price')
        name = options.get('name')
        categories = options.get('categories')
        include_out_of_stock = options.get('include_out_of_stock')
        if include_out_of_stock is None:
            include_out_of_stock = False

        expressions = []
        if not include_out_of_stock:
            expressions.append(ProductsHistoryEntity.product_history_status == ProductsHistoryEntity.ProductHistoryStatusEnum.IN_STOCK)
        if from_edit_date is not None:
            expressions.append(ProductsHistoryEntity.product_history_edit_date >= from_edit_date)
        if to_edit_date is not None:
            expressions.append(ProductsHistoryEntity.product_history_edit_date <= to_edit_date)
        if from_price is not None:
            expressions.append(ProductsHistoryEntity.product_history_price >= from_price)
        if to_price is not None:
            expressions.append(ProductsHistoryEntity.product_history_price >= to_price)
        if name is not None and name.strip() != "":
            expressions.append(Like(ProductsHistoryEntity.product_history_name, "%{0}%".format(name)))
        if categories is not None and len(categories) > 0:
            expressions.append(In(ProductsHistoryEntity.product_history_category, categories))

        store = get_current_transaction_store()
        entities = store.find(ProductsHistoryEntity, And(*expressions)).order_by(ProductsHistoryEntity.product_history_edit_date)

        results = []
        for entity in entities:
            results.append(DynamicObject(entity_to_dic(entity)))

        return results

    def write_history(self, product, colors, sizes, brands, **options):
        """
        Writes product history.

        :param product:
        :param colors:
        :param sizes:
        :param brands:
        :param options:
        :return:
        """

        history = ProductsHistoryEntity()
        history.product_history_edit_date = datetime.datetime.now()
        history.product_history_id = unicode(unique_id_services.get_id('uuid'))
        history.product_id = product.product_id
        history.product_history_name = product.product_name
        history.product_history_price = product.product_price
        history.product_history_category = product.product_category
        history.product_history_image = product.product_image
        history.product_history_status = product.product_status
        history.product_history_unique_name = product.product_unique_name
        if colors is not None and len(colors) > 0:
            history.product_history_colors = '-'.join(colors)
        if sizes is not None and len(sizes) > 0:
            history.product_history_sizes = '-'.join(sizes)
        if brands is not None and len(brands) > 0:
            history.product_history_brands = '-'.join(brands)
        history.product_history_counter = product.product_counter
        history.product_history_age_category = product.product_age_category
        history.product_history_gender = product.product_gender
        history.product_history_comment = product.product_comment

        store = get_current_transaction_store()
        store.add(history)
