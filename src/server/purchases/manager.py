"""
Created on Oct 14, 2016

@author: Hamed Zekri
"""

import datetime
from decimal import Decimal
from dateutil import parser

from storm import Undef
from storm.expr import Select, In, And, Exists, Desc, Or

from deltapy.core import DeltaObject, DeltaException, DynamicObject
from deltapy.transaction.services import get_current_transaction_store
from deltapy.security.session.services import get_current_user
from deltapy.utils.storm_aux import entity_to_dic
import deltapy.unique_id.services as unique_id_services

from server.model import PurchasesEntity, PurchasesCommentEntity, ProductsEntity, UserEntity
import server.products.services as products_services


class PurchaseException(DeltaException):
    """
    Purchase Exception
    """


class PurchasesManager(DeltaObject):
    """
    Purchases Manager
    """

    def _get(self, purchase_id):
        """
        Returns Purchase entity.

        :param Purchase_id:
        :return:
        """

        store = get_current_transaction_store()
        entity = store.get(PurchasesEntity, purchase_id)

        if entity is None:
            raise PurchaseException("Purchase [{0}] not found.".format(purchase_id))

        return entity

    def get(self, purchase_id):
        '''
        Returns Purchase info.

        :param Purchase_id:
        :return:
        '''

        entity = self._get(purchase_id)

        purchase = DynamicObject(entity_to_dic(entity))

        store = get_current_transaction_store()
        item_entities = \
            store.find(PurchasesCommentEntity, PurchasesCommentEntity.purchase_id == purchase_id).order_by(PurchasesCommentEntity.purchase_comment_date)

        purchase.items = []
        for item in item_entities:
            purchase.items.append(DynamicObject(entity_to_dic(item)))

        return purchase

    def find(self, **options):
        '''
        Searches Purchases.

        :param options:
        :return:
        '''

        from_purchase_date = options.get('from_purchase_date')
        to_purchase_date = options.get('to_purchase_date')
        statuses = options.get('statuses')
        consumer_user_id = options.get('consumer_user_id')
        producer_user_id = options.get('producer_user_id')
        show_only_current_user = options.get('show_only_current_user')
        if show_only_current_user is None:
            show_only_current_user = True

        expressions = []
        current_user_id = get_current_user().id

        if from_purchase_date is not None:
            if not isinstance(from_purchase_date, datetime.datetime):
                from_purchase_date = parser.parse(from_purchase_date)
            expressions.append(PurchasesEntity.purchase_date >= from_purchase_date)
        if to_purchase_date is not None:
            if not isinstance(to_purchase_date, datetime.datetime):
                to_purchase_date = parser.parse(to_purchase_date)
            expressions.append(PurchasesEntity.purchase_date <= to_purchase_date)
        if statuses is not None and len(statuses) > 0:
            expressions.append(In(PurchasesEntity.purchase_status, statuses))
        if consumer_user_id is not None:
            expressions.append(PurchasesEntity.purchase_consumer_user_id == consumer_user_id)
        if producer_user_id is not None:
            expressions.append(PurchasesEntity.purchase_producer_user_id == producer_user_id)
        if show_only_current_user:
            expressions.append(Or(PurchasesEntity.purchase_consumer_user_id == current_user_id,
                                  PurchasesEntity.purchase_producer_user_id == current_user_id))

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

        statement = Select(columns=[PurchasesEntity.purchase_id,
                                    PurchasesEntity.purchase_date,
                                    PurchasesEntity.purchase_status,
                                    PurchasesEntity.purchase_comment,
                                    PurchasesEntity.purchase_consumer_user_id,
                                    PurchasesEntity.purchase_producer_user_id,
                                    PurchasesEntity.purchase_product_id,
                                    PurchasesCommentEntity.comment_id,
                                    PurchasesCommentEntity.purchase_comment,
                                    PurchasesCommentEntity.purchase_comment_date,
                                    PurchasesCommentEntity.purchase_comment_user_id,
                                    PurchasesCommentEntity.purchase_comment_consumer_last_check,
                                    PurchasesCommentEntity.purchase_comment_producer_last_check,
                                    ProductsEntity.product_name,
                                    ProductsEntity.product_creation_date,
                                    ProductsEntity.product_comment,
                                    ProductsEntity.product_image,
                                    ProductsEntity.product_age_category,
                                    ProductsEntity.product_gender],
                           where=And(Exists(Select(columns=[1],
                                                   where=And(*expressions),
                                                   order_by=[Desc(PurchasesEntity.purchase_date)],
                                                   offset=offset,
                                                   limit=limit)),
                                     PurchasesCommentEntity.purchase_id == PurchasesEntity.purchase_id,
                                     PurchasesEntity.purchase_product_id == ProductsEntity.product_id),
                           tables=[PurchasesEntity,
                                   PurchasesCommentEntity,
                                   ProductsEntity],
                           order_by=[Desc(PurchasesEntity.purchase_date)])

        results = {}
        store = get_current_transaction_store()
        for (purchase_id,
             purchase_date,
             purchase_status,
             comment,
             purchase_consumer_user_id,
             purchase_producer_user_id,
             purchase_product_id,
             comment_id,
             purchase_comment,
             purchase_comment_date,
             purchase_comment_user_id,
             purchase_comment_consumer_last_check,
             purchase_comment_producer_last_check,
             product_name,
             product_creation_date,
             product_comment,
             product_image,
             product_age_category,
             product_gender) in store.execute(statement):
            Purchase = results.get(purchase_id)
            if Purchase is None:
                purchase = DynamicObject(purchase_id=purchase_id,
                                         purchase_date=purchase_date,
                                         purchase_status=purchase_status,
                                         purchase_comment=comment,
                                         purchase_consumer_user_id=purchase_consumer_user_id,
                                         purchase_producer_user_id=purchase_producer_user_id,
                                         purchase_product_id=purchase_product_id,
                                         purchase_comments=[],
                                         product=DynamicObject(product_id=purchase_product_id,
                                                               product_name=product_name,
                                                               product_creation_date=product_creation_date,
                                                               product_comment=product_comment,
                                                               product_image=product_image,
                                                               product_age_category=product_age_category,
                                                               product_gender=product_gender))
                results[purchase_id] = purchase

                purchase.purchase_items.append(DynamicObject(comment_id=comment_id,
                                                             purchase_comment=purchase_comment,
                                                             purchase_comment_date=purchase_comment_date,
                                                             purchase_comment_user_id=purchase_comment_user_id,
                                                             purchase_comment_consumer_last_check=purchase_comment_consumer_last_check,
                                                             purchase_comment_producer_last_check=purchase_comment_producer_last_check))

        return list(reversed(sorted(results.values(), key=lambda k: k['purchase_date'])))
