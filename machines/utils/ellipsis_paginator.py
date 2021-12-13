from django.core.paginator import Paginator
from django.utils.translation import gettext_lazy as _


class EllipsisPaginator(Paginator):
    ELLIPSIS = _('…')

    def get_elided_page_range(self, number=1, *, on_each_side=3, on_ends=2):
        """
        Удалить после обновления до django 3.2

        Return a 1-based range of pages with some values elided.
        If the page range is larger than a given size, the whole range is not
        provided and a compact form is returned instead, e.g. for a paginator
        with 50 pages, if page 43 were the current page, the output, with the
        default arguments, would be:
            1, 2, …, 40, 41, 42, 43, 44, 45, 46, …, 49, 50.
        """

        number = self.validate_number(number)

        if self.num_pages <= (on_each_side + on_ends) * 2:
            yield from self.page_range
            return

        if number > (1 + on_each_side + on_ends) + 1:
            yield from range(1, on_ends + 1)
            yield self.ELLIPSIS
            yield from range(number - on_each_side, number + 1)
        else:
            yield from range(1, number + 1)

        if number < (self.num_pages - on_each_side - on_ends) - 1:
            yield from range(number + 1, number + on_each_side + 1)
            yield self.ELLIPSIS
            yield from range(self.num_pages - on_ends + 1, self.num_pages + 1)
        else:
            yield from range(number + 1, self.num_pages + 1)