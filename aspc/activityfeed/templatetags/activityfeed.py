from django import template
from django.template.loader import render_to_string

register = template.Library()

@register.tag
def insert_activity(parser, token):
    try:
        tag_name, activity = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError("%r tag requires exactly one argument" % token.contents.split()[0])
    return InsertActivityNode(activity)

class InsertActivityNode(template.Node):
    def __init__(self, activity):
        self.activity = template.Variable(activity)

    def render(self, context):
        activity = self.activity.resolve(context)
        filename = "activityfeed/%s.txt" % activity.category
        object = activity.object
        message= render_to_string(filename, {'object':object})
        return render_to_string("activityfeed/activity.html", {'activity':activity, 'message': message})

@register.simple_tag
def parse_tweet(tweet):
    import re

    #compile regexes as objects
    hash_regex = re.compile(r'#[0-9a-zA-Z+_]*',re.IGNORECASE)
    user_regex = re.compile(r'@[0-9a-zA-Z+_]*',re.IGNORECASE)

    #first deal with links. Any http://... string change to a proper link
    tweet = re.sub('http://[^ ,]*', lambda t: '<a href="%s" target="_blank">%s</a>' % (t.group(0), t.group(0)), tweet)

    #for all elements matching our pattern...
    for usr in user_regex.finditer(tweet):

        #for each whole match replace '@' with ''
        url_tweet = usr.group(0).replace('@','')

        #in tweet's text replace text with proper link, now without '@'
        tweet = tweet.replace(usr.group(0),
            '<a href="https://twitter.com/'+url_tweet+'" title="'+usr.group(0)+'">'+usr.group(0)+'</a>')

    #do the same for hash tags
    for hash in hash_regex.finditer(tweet):
        url_hash = hash.group(0).replace('#','%23')
        if len ( hash.group(0) ) > 2:
            tweet = tweet.replace(hash.group(0),
                '<a href="https://twitter.com/search?q='+url_hash+'" title="'+hash.group(0)+'">'+hash.group(0)+'</a>');

    return tweet