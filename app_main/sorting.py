
class Sorting:

    sorting_types = {
        "with_no_categories_first": lambda x: x.order_by('-category__is_null'),
        "by_date": lambda x: x.order_by('date'),
        "by_link": lambda x: x.order_by('link')
    }

    @classmethod
    def get_sorting_types(cls) -> list:
        """ Returns list of sorting types"""
        return list(cls.sorting_types.keys())

    @classmethod
    def sort(cls, links, sorting_type: str):
        """ Sort links according to given sorting type """
        return cls.sorting_types[sorting_type](links)
