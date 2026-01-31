# -*- coding: utf-8 -*-
# from odoo import http


# class EngineeringSupervision(http.Controller):
#     @http.route('/engineering_supervision/engineering_supervision', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/engineering_supervision/engineering_supervision/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('engineering_supervision.listing', {
#             'root': '/engineering_supervision/engineering_supervision',
#             'objects': http.request.env['engineering_supervision.engineering_supervision'].search([]),
#         })

#     @http.route('/engineering_supervision/engineering_supervision/objects/<model("engineering_supervision.engineering_supervision"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('engineering_supervision.object', {
#             'object': obj
#         })

