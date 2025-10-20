# {
#     'name': "Real Estate",
#     'summary': "Test module",
#     'version': "17.0.0.0.0",
#     'license': "OEEL-1",
#     'depends': ["crm"],
#     'data': [
#         # #Security
#         # "security/res_groups.xml",
#         'security/ir.model.access.csv',
#         #views
#         "views/estate_property_views.xml", # <-- KOMA INI WAJIB ADA
#         "views/estate_menus.xml"
#     ],
#     # "demo": [
#     #     "demo/demo.xml"
#     # ],
#     'application': True,
#     'installable': True,
# }

{
    'name': "Real Estate",
    'summary': "Test module",
    'version': "18.0.1.0.0",  
    'license': "OEEL-1",
    "author": "Ik",
    'depends': ["base"],  
    'data': [
        'security/ir.model.access.csv',
        'security/res_groups.xml',
        'views/estate_property_views.xml',
        'views/estate_property_offer_views.xml',
        'views/estate_property_type_views.xml',
        'views/estate_menus.xml',
        'views/res_users_views.xml', 
        ],
    'application': True,
    'installable': True,
}