# adapted from http://djangosnippets.org/snippets/2236/
import math
from itertools import chain
from django.forms.utils import flatatt

from django import forms
from django.forms import widgets
from django.utils.encoding import force_unicode
from django.utils.html import conditional_escape
from django.utils.safestring import mark_safe

class ColumnCheckboxSelectMultiple(forms.CheckboxSelectMultiple):
    """
    Widget that renders multiple-select checkboxes in columns.
    Constructor takes number of columns and css class to apply
    to the <ul> elements that make up the columns.
    """
    def __init__(self, columns=2, css_class=None, **kwargs):
        super(self.__class__, self).__init__(**kwargs)
        self.columns = columns
        self.css_class = css_class

    def render(self, name, value, attrs=None, choices=()):
        if value is None: value = []
        has_id = attrs and 'id' in attrs
        final_attrs = self.build_attrs(attrs, name=name)
        choices_enum = list(enumerate(chain(self.choices, choices)))

        # This is the part that splits the choices into columns.
        # Slices vertically.  Could be changed to slice horizontally, etc.
        column_sizes = columnize(len(choices_enum), self.columns)
        columns = []
        for column_size in column_sizes:
            columns.append(choices_enum[:column_size])
            choices_enum = choices_enum[column_size:]
        output = []
        for column in columns:
            if self.css_class:
                output.append(u'<ul class="%s"' % self.css_class)
            else:
                output.append(u'<ul>')
            # Normalize to strings
            str_values = set([force_unicode(v) for v in value])
            for i, (option_value, option_label) in column:
                # If an ID attribute was given, add a numeric index as a suffix,
                # so that the checkboxes don't all have the same ID attribute.
                if has_id:
                    final_attrs = dict(final_attrs, id='%s_%s' % (
                            attrs['id'], i))
                    label_for = u' for="%s"' % final_attrs['id']
                else:
                    label_for = ''

                cb = forms.CheckboxInput(
                    final_attrs, check_test=lambda value: value in str_values)
                option_value = force_unicode(option_value)
                rendered_cb = cb.render(name, option_value)
                option_label = conditional_escape(force_unicode(option_label))
                output.append(u'<li><label%s>%s %s</label></li>' % (
                        label_for, rendered_cb, option_label))
            output.append(u'</ul>')
        return mark_safe(u'\n'.join(output))


def columnize(items, columns):
    """
    Return a list containing numbers of elements per column if `items` items
    are to be divided into `columns` columns.

    >>> columnize(10, 1)
    [10]
    >>> columnize(10, 2)
    [5, 5]
    >>> columnize(10, 3)
    [4, 3, 3]
    >>> columnize(3, 4)
    [1, 1, 1, 0]
    """
    elts_per_column = []
    for col in range(columns):
        col_size = int(math.ceil(float(items) / columns))
        elts_per_column.append(col_size)
        items -= col_size
        columns -= 1
    return elts_per_column

class RoomSelectionWidget(widgets.MultiWidget):
    def __init__(self, buildings=None, attrs=None):
        rswidgets = (widgets.Select(choices=buildings), widgets.TextInput)
        super(RoomSelectionWidget, self).__init__(rswidgets, attrs=attrs)

    def decompress(self, value):
        if value:
            print value
        return [None, None]

class RadioInputHTML(widgets.RadioChoiceInput):
    """
    subclassed for 1 character fix... no <input /> in valid html4
    """
    def tag(self):
        if 'id' in self.attrs:
            self.attrs['id'] = '%s_%s' % (self.attrs['id'], self.index)
        final_attrs = dict(self.attrs, type='radio', name=self.name, value=self.choice_value)
        if self.is_checked():
            final_attrs['checked'] = 'checked'
        return mark_safe(u'<input%s>' % flatatt(final_attrs))

class RatingRadioFieldRenderer(widgets.RadioFieldRenderer):
    """
    Custom version of the RadioFieldRenderer that only labels the
    first and last items in the list.
    """
    def __iter__(self):
        for i, choice in enumerate(self.choices):
            yield RadioInputHTML(self.name, self.value, self.attrs.copy(), choice, i)

    def __getitem__(self, idx):
        choice = self.choices[idx] # Let the IndexError propogate
        return RadioInputHTML(self.name, self.value, self.attrs.copy(), choice, idx)

    def render(self):
        """Outputs a <ul> for this set of radio fields."""
        input_tags = list(self)
        last = input_tags.pop()
        first = input_tags.pop(0)

        output = u'<label class="low">{0}</label><label class="mobile_high">{1}</label> <span class="rating_control">{2}\n'.format(
            conditional_escape(force_unicode(first.choice_label)),
            conditional_escape(force_unicode(last.choice_label)),
            first.tag())
        for choice in input_tags:
            output += u'{0}\n'.format(choice.tag())
        output += u'{1}</span> <label class="high">{0}</label>\n'.format(conditional_escape(force_unicode(last.choice_label)), last.tag())
        return mark_safe(output)