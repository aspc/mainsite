from django.db import models
from aspc.folio.fields import MarkdownTextField

class Page(models.Model):
    """A glorified static page with Markdown content"""
    
    SECTION_LOOKUP = {
        'Information': 0,
        'Senate': 1,
    }
    
    SECTIONS = ((a[1], a[0]) for a in SECTION_LOOKUP.items())
    
    title = models.CharField(max_length=255, help_text="The page's full title")
    short_title = models.CharField(blank=True, max_length=80, help_text="An optional abbreviated title (for sidebar display)")
    slug = models.CharField(help_text="The slug (URL identifier) for the page", max_length=80)
    parent = models.ForeignKey('self', blank=True, null=True, help_text="Optional parent page for this one. If none, it is listed as a top level page in its section.")
    summary = models.TextField(help_text="Page summary for display in parent page's subpage list (plain text)")
    body = models.TextField(help_text="Page body text written in Markdown")
    section = models.IntegerField(choices=SECTIONS, help_text="The section in which this page appears")
    sort_order = models.PositiveSmallIntegerField(blank=True, help_text="Sort ordering")
    
    class Meta:
        ordering = ['section', 'sort_order',]
        verbose_name, verbose_name_plural = "page", "pages"

    def __unicode__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.sort_order:
            pages = Page.objects.filter(section=self.section).order_by('-sort_order')
            if not pages.count():
                self.sort_order = 1
            else:
                self.sort_order = pages[0].sort_order + 1
        super(Page, self).save(*args, **kwargs)
    
    @models.permalink
    def get_absolute_url(self):
        return ('page_view', [], {'section': self.section, 'slug': self.slug,})