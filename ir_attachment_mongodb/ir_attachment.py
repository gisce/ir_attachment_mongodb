# -*- coding: utf-8 -*-

from osv import osv, fields
from mongodb_backend import fields as mongodb_fields


def mongoize(vals):
    vals['datas_mongo'] = vals['datas']
    vals['datas'] = False


def unmongoize(vals):
    vals['datas'] = vals['datas_mongo']
    del vals['datas_mongo']


class IrAttachment(osv.osv):
    _name = 'ir.attachment'
    _inherit = 'ir.attachment'

    def create(self, cursor, uid, vals, context=None):
        if 'datas' in vals and vals['datas']:
            mongoize(vals)
        return super(IrAttachment, self).create(cursor, uid, vals, context)

    def write(self, cursor, uid, ids, vals, context=None):
        if 'datas' in vals:
            mongoize(vals)
        return super(IrAttachment, self).write(cursor, uid, ids, vals, context)

    def read(self, cursor, uid, ids, fields=None, context=None,
             load='_classic_read'):
        if fields and 'datas' in fields and 'datas_mongo' not in fields:
            fields.append('datas_mongo')
        res = super(IrAttachment, self).read(cursor, uid, ids, fields, context,
                                             load)
        if isinstance(ids, (list, tuple)):
            if res and 'datas' in res[0]:
                for attach in res:
                    if attach['datas_mongo']:
                        unmongoize(attach)
        else:
            if 'datas' in res and res['datas_mongo']:
                unmongoize(res)
        return res

    def unlink(self, cursor, uid, ids, context=None):
        # Remove the file from mongodb
        self.write(cursor, uid, ids, {'datas': False})
        return super(IrAttachment, self).unlink(cursor, uid, ids, context)

    _columns = {
        'datas_mongo': mongodb_fields.gridfs('Mongo Id')
    }

IrAttachment()
