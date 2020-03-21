
def fix_category(store_name, category):
    struct = {
        'matsuya': {
            'pre_gyuu' : 'gyudon',
            'gyumeshi' : 'gyudon',
            'curry'    : 'curry',
            'don'      : 'don',
            'teishoku' : 'special',
            'morning'  : 'special',
            'okosama'  : 'kids',
            'udoon'    : 'special',
            'yorumatsu': 'special',
            'sidemenu' : 'sidemenu',
            'topping'  : 'sidemenu',
            'drink'    : 'sidemenu',
        },
        'sukiya': {
            'gyudon'   : 'gyudon',
            'gyusuki'  : 'gyudon',
            'curry'    : 'curry',
            'don'      : 'don',
            'special'  : 'special',
            'kids'     : 'kids',
            'side'     : 'sidemenu',
            'drink'    : 'sidemenu',
        },
        'yoshinoya': {
            'gyudon'   : 'gyudon',
            'gyunonabeyaki': 'gyudon',
            'wset'     : 'special',
            'karaage'  : 'don',
            'mixfly'   : 'special',
            'gyukarubidon': 'gyudon',
            'set'      : 'special',
            'unajyu'   : 'special',
            'curry'    : 'curry',
            'morningset': 'special',
            'ichijyu-sansai-asazen': 'special',
            'butadon'  : 'don',
            'kids'     : 'kids',
            'yoshinomi': 'sidemenu',
            'sidemenu' : 'sidemenu',
        }
    }
    return struct[store_name][category]