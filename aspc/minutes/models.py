from django.db import models

class MeetingMinutes(models.Model):
    """The minutes for a meeting of the ASPC Senate"""
    
    date = models.DateField(
        help_text="Date of the meeting"
    )
    summary = models.TextField(
        blank=True,
        help_text="Summarize this meeting in a sentence or two of "
                  "unformatted text. (Used for search results and overview.)",
    )
    body = models.TextField(
        blank=True,
        help_text="The minutes of this meeting in <a href=\"http://daringfireball.net/projects/markdown/dingus\">Markdown</a>",
    )
    
    class Meta:
        ordering = ['date']
        verbose_name, verbose_name_plural = "meeting minutes", "meeting minutes"

    def __unicode__(self):
        return u"MeetingMinutes: {0}".format(self.date)

    @models.permalink
    def get_absolute_url(self):
        month, day, year = self.date.strftime("%b %d %Y").split(" ")
        return ('minutes_detail', [], {"year": year, "month": month, "day": day})
    
    @property
    def title(self):
        return "Senate Minutes for {0}".format(self.date.strftime("%b. %d %Y"))