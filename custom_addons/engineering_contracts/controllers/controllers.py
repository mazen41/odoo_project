# -*- coding: utf-8 -*-
# from odoo import http


# class EngineeringContracts(http.Controller):
#     @http.route('/engineering_contracts/engineering_contracts', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/engineering_contracts/engineering_contracts/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('engineering_contracts.listing', {
#             'root': '/engineering_contracts/engineering_contracts',
#             'objects': http.request.env['engineering_contracts.engineering_contracts'].search([]),
#         })

#     @http.route('/engineering_contracts/engineering_contracts/objects/<model("engineering_contracts.engineering_contracts"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('engineering_contracts.object', {
#             'object': obj
#         })

