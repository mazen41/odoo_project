# -*- coding: utf-8 -*-
# from odoo import http


# class EngineeringSales(http.Controller):
#     @http.route('/engineering_sales/engineering_sales', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/engineering_sales/engineering_sales/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('engineering_sales.listing', {
#             'root': '/engineering_sales/engineering_sales',
#             'objects': http.request.env['engineering_sales.engineering_sales'].search([]),
#         })

#     @http.route('/engineering_sales/engineering_sales/objects/<model("engineering_sales.engineering_sales"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('engineering_sales.object', {
#             'object': obj
#         })

