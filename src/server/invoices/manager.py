"""
Created on Oct 14, 2016

@author: Hamed Zekri
"""

from deltapy.core import DeltaObject, DeltaException
from deltapy.transaction.services import get_current_transaction_store
from server.model import InvoiceEntity


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