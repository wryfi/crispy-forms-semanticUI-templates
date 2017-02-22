from django.template import Template
from django.template.loader import render_to_string

from crispy_forms.layout import Field
from crispy_forms.utils import flatatt
from crispy_forms.utils import render_field, TEMPLATE_PACK
from crispy_forms.compatibility import text_type


class IconField(Field):
    template = '%s/layout/icon_field.html'

    def __init__(self, field, icon_class, align='left', *args, **kwargs):
        self.field = field
        self.icon_class = icon_class
        self.align = align
        super(IconField, self).__init__(*args, **kwargs)

    def render(self, form, form_style, context, template_pack=TEMPLATE_PACK, extra_context=None, **kwargs):
        extra_context = {
            'icon_class': self.icon_class,
            'align': self.align
        }
        if hasattr(self, 'wrapper_class'):
            extra_context['wrapper_class'] = self.wrapper_class
        template = self.get_template_name(template_pack)
        return render_field(
            self.field, form, form_style, context,
            template=template, attrs=self.attrs,
            template_pack=template_pack, extra_context=extra_context, **kwargs
        )


class IconButton(object):
    """
    Layout object for rendering an HTML button::

        Button("button content", css_class="extra")
    """
    template = '%s/layout/button.html'
    field_classes = 'ui submit {} labeled icon button'

    def __init__(self, content, icon_class, align='left', **kwargs):
        self.content = content
        self.template = kwargs.pop('template', self.template)
        self.icon_class = icon_class
        self.align = align
        self.field_classes = self.field_classes.format(self.align)

        # We turn css_id and css_class into id and class
        if 'css_id' in kwargs:
            kwargs['id'] = kwargs.pop('css_id')
        kwargs['class'] = self.field_classes
        if 'css_class' in kwargs:
            kwargs['class'] += " %s" % kwargs.pop('css_class')

        self.flat_attrs = flatatt(kwargs)

    def render(self, form, form_style, context, template_pack=TEMPLATE_PACK, **kwargs):
        self.content = Template(text_type(self.content)).render(context)
        template = self.template % template_pack
        context.update({'button': self})

        return render_to_string(template, context.flatten())


class BooleanToggle(Field):
    template = '%s/layout/boolean_toggle.html'
    field_classes = 'ui toggle checkbox'

    def __init__(self, field, icon_class, align='left', *args, **kwargs):
        pass