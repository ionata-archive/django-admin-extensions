from django import template

register = template.Library()

@register.tag
def object_tool(parser, token):
    return ObjectToolNode.handle(parser, token)

class ObjectToolNode(template.Node):

    @classmethod
    def handle(cls, parser, token):
        bits = token.split_contents()
        tool = bits[1]
        if len(bits) > 2:
            # Pass second argument, removing quote characters
            return cls(tool, bits[2][1:-1])
        return cls(tool)

    def __init__(self, tool, link_class=None):
        self.tool = tool
        self.link_class = link_class

    def render(self, context):
        tool = context[self.tool]
        if self.link_class:
            link = tool(context, self.link_class)
        else:
            link = tool(context)
        if link:
            return '%s' % link
        else:
            return ''
