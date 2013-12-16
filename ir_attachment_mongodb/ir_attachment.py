# -*- coding: utf-8 -*-

from osv import osv, fields
from mongodb_backend import fields as mongodb_fields


class IrAttachment(osv.osv):
    _name = 'ir.attachment'
    _inherit = 'ir.attachment'

    def create(self, cursor, uid, vals, context=None):
        if 'datas' in vals and vals['datas']:
            vals['datas_mongo'] = vals['datas']
            vals['datas'] = False
        return super(IrAttachment, self).create(cursor, uid, vals, context)

    def write(self, cursor, uid, ids, vals, context=None):
        if 'datas' in vals:
            vals['datas_mongo'] = vals['datas']
            del vals['datas']
        return super(IrAttachment, self).write(cursor, uid, ids, vals, context)

    def read(self, cursor, uid, ids, fields=None, context=None,
             load='_classic_read'):
        if fields and 'datas' in fields and 'datas_mongo' not in fields:
            fields.append('datas_mongo')
        res = super(IrAttachment, self).read(cursor, uid, ids, fields, context,
                                             load)
        if isinstance(ids, (list, tuple)):
            if 'datas' in res[0]:
                for attach in res:
                    attach['datas'] = attach['datas_mongo']
                    del attach['datas_mongo']
        else:
            if 'datas' in res:
                res['datas'] = res['datas_mongo']
                del res['datas_mongo']
        return res


    _columns = {
        'datas_mongo': mongodb_fields.gridfs('Mongo Id')
    }

IrAttachment()
