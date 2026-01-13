# -*- coding: utf-8 -*-
# from odoo import http


# class EngineeringCrm(http.Controller):
#     @http.route('/engineering_crm/engineering_crm', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/engineering_crm/engineering_crm/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('engineering_crm.listing', {
#             'root': '/engineering_crm/engineering_crm',
#             'objects': http.request.env['engineering_crm.engineering_crm'].search([]),
#         })

#     @http.route('/engineering_crm/engineering_crm/objects/<model("engineering_crm.engineering_crm"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('engineering_crm.object', {
#             'object': obj
#         })

