# -*- coding: utf-8 -*-

from osv import osv, fields
from mongodb_backend import fields as mongodb_fields


class IrAttachment(osv.osv):
    _name = 'ir.attachment'
    _inherit = 'ir.attachment'

    def create(self, cursor, uid, vals, context=None):
        if 'data' in vals and vals['data']:
            vals['datas_mongo'] = vals['data']
            vals['data'] = False
        return super(IrAttachment, self).create(cursor, uid, vals, context)

    def read(self, cursor, uid, ids, fields=None, context=None,
             load='_classic_read'):
        if fields and 'data' in fields and 'datas_mongo' not in fields:
            fields.append('datas_mongo')
        return super(IrAttachment, self).read(cursor, uid, ids, fields, context,
                                              load)


    _columns = {
        'datas_mongo': mongodb_fields.gridfs('Mongo Id')
    }

IrAttachment()
