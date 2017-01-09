"""
Created on Oct 14, 2016

@author: Hamed Zekri
"""

import datetime
from decimal import Decimal
from dateutil import parser

from storm import Undef
from storm.expr import Select, In, And, Exists, Desc

from deltapy.core import DeltaObject, DeltaException, DynamicObject
from deltapy.transaction.services import get_current_transaction_store
from deltapy.security.session.services import get_current_user
from deltapy.utils.storm_aux import entity_to_dic
import deltapy.unique_id.services as unique_id_services

from server.model import InvoiceEntity, InvoiceItemEntity, ProductsEntity, UserEntity
import server.products.services as products_services


class InvoiceException(DeltaException):
    """
    Invoice Exception
    """


class InvoicesManager(DeltaObject):
    """
    Invoices Manager
    """

    def _get(self, invoice_id):
        """
        Returns invoice entity.

        :param invoice_id:
        :return:
        """

        store = get_current_transaction_store()
        entity = store.get(InvoiceEntity, invoice_id)

        if entity is None:
            raise InvoiceException("Invoice [{0}] not found.".format(invoice_id))

        return entity

    def get(self, invoice_id):
        '''
        Returns invoice info.

        :param invoice_id:
        :return:
        '''

        entity = self._get(invoice_id)

        invoice = DynamicObject(entity_to_dic(entity))

        store = get_current_transaction_store()
        item_entities = \
            store.find(InvoiceItemEntity, InvoiceItemEntity.invoice_id == invoice_id).order_by(InvoiceItemEntity.item_row)

        invoice.items = []
        for item in item_entities:
            invoice.items.append(DynamicObject(entity_to_dic(item)))

        return invoice

    def find(self, **options):
        '''
        Searches invoices.

        :param options:
        :return:
        '''

        from_invoice_date = options.get('from_invoice_date')
        to_invoice_date = options.get('to_invoice_date')
        statuses = options.get('statuses')
        consumer_user_id = options.get('consumer_user_id')

        expressions = []

        if from_invoice_date is not None:
            if not isinstance(from_invoice_date, datetime.datetime):
                from_invoice_date = parser.parse(from_invoice_date)
            expressions.append(InvoiceEntity.invoice_date >= from_invoice_date)
        if to_invoice_date is not None:
            if not isinstance(to_invoice_date, datetime.datetime):
                to_invoice_date = parser.parse(to_invoice_date)
            expressions.append(InvoiceEntity.invoice_date <= to_invoice_date)
        if statuses is not None and len(statuses) > 0:
            expressions.append(In(InvoiceEntity.invoice_status, statuses))
        if consumer_user_id is not None:
            expressions.append(InvoiceEntity.invoice_consumer_user_id == consumer_user_id)

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

        statement = Select(columns=[InvoiceEntity.invoice_id,
                                    InvoiceEntity.invoice_date,
                                    InvoiceEntity.invoice_status,
                                    InvoiceEntity.invoice_comment,
                                    InvoiceEntity.invoice_consumer_user_id,
                                    InvoiceItemEntity.item_id,
                                    InvoiceItemEntity.item_product_id,
                                    InvoiceItemEntity.item_price,
                                    InvoiceItemEntity.item_quantity,
                                    InvoiceItemEntity.item_row,
                                    InvoiceItemEntity.item_color,
                                    InvoiceItemEntity.item_size,
                                    InvoiceItemEntity.item_brand,
                                    ProductsEntity.product_name,
                                    ProductsEntity.product_creation_date,
                                    ProductsEntity.product_comment,
                                    ProductsEntity.product_image,
                                    ProductsEntity.product_age_category,
                                    ProductsEntity.product_gender],
                           where=And(Exists(Select(columns=[1],
                                                   where=And(*expressions),
                                                   order_by=[Desc(InvoiceEntity.invoice_date)],
                                                   offset=offset,
                                                   limit=limit)),
                                     InvoiceItemEntity.invoice_id == InvoiceEntity.invoice_id,
                                     InvoiceItemEntity.item_product_id == ProductsEntity.product_id),
                           tables=[InvoiceEntity,
                                   InvoiceItemEntity,
                                   ProductsEntity],
                           order_by=[Desc(InvoiceEntity.invoice_date),
                                     InvoiceItemEntity.item_row])

        results = {}
        store = get_current_transaction_store()
        for (invoice_id,
             invoice_date,
             invoice_status,
             invoice_comment,
             invoice_consumer_user_id,
             item_id,
             item_product_id,
             item_price,
             item_quantity,
             item_row,
             item_color,
             item_size,
             item_brand,
             product_name,
             product_creation_date,
             product_comment,
             product_image,
             product_age_category,
             product_gender) in store.execute(statement):
            invoice = results.get(invoice_id)
            if invoice is None:
                invoice = DynamicObject(invoice_id=invoice_id,
                                        invoice_date=invoice_date,
                                        invoice_status=invoice_status,
                                        invoice_comment=invoice_comment,
                                        invoice_consumer_user_id=invoice_consumer_user_id,
                                        total_invoce_price=0,
                                        invoice_items=[])
                results[invoice_id] = invoice

            invoice.invoice_items.append(DynamicObject(item_id=item_id,
                                                       item_product_id=item_product_id,
                                                       item_price=item_price,
                                                       item_quantity=item_quantity,
                                                       item_row=item_row,
                                                       item_color=item_color,
                                                       item_size=item_size,
                                                       item_brand=item_brand,
                                                       product=DynamicObject(product_id=item_product_id,
                                                                             product_name=product_name,
                                                                             product_creation_date=product_creation_date,
                                                                             product_comment=product_comment,
                                                                             product_image=product_image,
                                                                             product_age_category=product_age_category,
                                                                             product_gender=product_gender)))
            invoice.total_invoce_price += item_quantity * item_price

        return results.values()

    def register(self, invoice_items):
        '''
        Registers new invoice.

        :param invoice_items:
        :return:
        '''

        if invoice_items is None or len(invoice_items) <= 0:
            raise InvoiceException('At least one item should be included.')

        current_user = get_current_user()
        store = get_current_transaction_store()

        invoice = InvoiceEntity()
        invoice.invoice_consumer_user_id = current_user.id
        invoice.invoice_date = datetime.datetime.now()
        invoice.invoice_status = InvoiceEntity.InvoiceStatusEnum.ORDERED
        invoice.invoice_id = unicode(unique_id_services.get_id('uuid'))
        store.add(invoice)

        counter = 1
        result = DynamicObject(entity_to_dic(invoice))
        result.invoice_items = []
        for item in invoice_items:
            item_entity = InvoiceItemEntity()
            item_entity.invoice_id = invoice.invoice_id
            item_entity.item_color = unicode(item.get('color'))
            item_entity.item_size = unicode(item.get('size'))
            item_entity.item_brand = unicode(item.get('brand'))
            item_entity.item_id = unicode(unique_id_services.get_id('uuid'))
            item_entity.item_price = Decimal(str(item.get('price')))
            item_entity.item_quantity = int(item.get('quantity'))
            item_entity.item_row = counter
            item_entity.item_product_id = unicode(item.get('product_id'))

            products_services.decrease_product_counter(item_entity.item_product_id)
            product = products_services.get(item_entity.item_product_id,
                                            fetch_details=False)
            if (product.product_whole_sale_type == ProductsEntity.ProductWholesaleTypeEnum.WHOLESALE and
                current_user.user_production_type != UserEntity.UserProductionTypeEnum.PRODUCER):
                raise InvoiceException("User [{0} - {1}] is not producer one and can not register "
                                       "product [{2}] which is wholesale product type.".format(current_user.user_id,
                                                                                                     current_user.user_name,
                                                                                                     product.product_name))

            counter += 1

            store.add(item_entity)
            result.invoice_items.append(DynamicObject(entity_to_dic(item_entity)))

        return result

    def update(self, invoice_id, **options):
        '''
        updates invoices.

        :param options:
        :return:
        '''

        entity = self._get(invoice_id)

        status = options.get('status')
        if status is not None:
            entity.invoice_status = status

    def get_producer_registered_invoices(self, **options):
        '''
        Returns producer registered invoices.

        :return:
        '''

        current_user = get_current_user()
        if current_user.user_production_type != UserEntity.UserProductionTypeEnum.PRODUCER:
            return []

        from_invoice_date = options.get('from_invoice_date')
        to_invoice_date = options.get('to_invoice_date')
        wholesale_type = options.get('wholesale_type')
        if wholesale_type in (None, -1):
            wholesale_type = ProductsEntity.ProductWholesaleTypeEnum.RETAIL

        expressions = \
            [InvoiceEntity.invoice_status == InvoiceEntity.InvoiceStatusEnum.ORDERED,
             ProductsEntity.product_producer_user_id == current_user.id,
             ProductsEntity.product_whole_sale_type == wholesale_type]

        if from_invoice_date is not None:
            if not isinstance(from_invoice_date, datetime.datetime):
                from_invoice_date = parser.parse(from_invoice_date)
            expressions.append(InvoiceEntity.invoice_date >= from_invoice_date)
        if to_invoice_date is not None:
            if not isinstance(to_invoice_date, datetime.datetime):
                to_invoice_date = parser.parse(to_invoice_date)
            expressions.append(InvoiceEntity.invoice_date <= to_invoice_date)

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

        statement = Select(columns=[InvoiceEntity.invoice_id,
                                    InvoiceEntity.invoice_date,
                                    InvoiceEntity.invoice_status,
                                    InvoiceEntity.invoice_comment,
                                    InvoiceEntity.invoice_consumer_user_id,
                                    InvoiceItemEntity.item_id,
                                    InvoiceItemEntity.item_product_id,
                                    InvoiceItemEntity.item_price,
                                    InvoiceItemEntity.item_quantity,
                                    InvoiceItemEntity.item_row,
                                    InvoiceItemEntity.item_color,
                                    InvoiceItemEntity.item_size,
                                    InvoiceItemEntity.item_brand,
                                    ProductsEntity.product_name,
                                    ProductsEntity.product_creation_date,
                                    ProductsEntity.product_comment,
                                    ProductsEntity.product_image,
                                    ProductsEntity.product_age_category,
                                    ProductsEntity.product_gender],
                           where=And(Exists(Select(columns=[1],
                                                   where=And(*expressions),
                                                   order_by=[Desc(InvoiceEntity.invoice_date)],
                                                   offset=offset,
                                                   limit=limit)),
                                     InvoiceItemEntity.invoice_id == InvoiceEntity.invoice_id,
                                     InvoiceItemEntity.item_product_id == ProductsEntity.product_id),
                           tables=[InvoiceEntity,
                                   InvoiceItemEntity,
                                   ProductsEntity],
                           order_by=[Desc(InvoiceEntity.invoice_date),
                                     InvoiceItemEntity.item_row])

        results = []
        store = get_current_transaction_store()
        for (invoice_id,
             invoice_date,
             invoice_status,
             invoice_comment,
             invoice_consumer_user_id,
             item_id,
             item_product_id,
             item_price,
             item_quantity,
             item_row,
             item_color,
             item_size,
             item_brand,
             product_name,
             product_creation_date,
             product_comment,
             product_image,
             product_age_category,
             product_gender) in store.execute(statement):
            invoice_item = DynamicObject(invoice_id=invoice_id,
                                         invoice_date=invoice_date,
                                         invoice_status=invoice_status,
                                         invoice_comment=invoice_comment,
                                         invoice_consumer_user_id=invoice_consumer_user_id,
                                         item_id=item_id,
                                         item_product_id=item_product_id,
                                         item_price=item_price,
                                         item_quantity=item_quantity,
                                         item_row=item_row,
                                         item_color=item_color,
                                         item_size=item_size,
                                         item_brand=item_brand,
                                         product=DynamicObject(product_id=item_product_id,
                                                               product_name=product_name,
                                                               product_creation_date=product_creation_date,
                                                               product_comment=product_comment,
                                                               product_image=product_image,
                                                               product_age_category=product_age_category,
                                                               product_gender=product_gender))

            results.append(invoice_item)

        return results