# coding: utf-8

"""
Convert Angular template to Django template
"""

import re
from pyquery import PyQuery as pq


class Angango(object):

    def __init__(self, html):
        self.d = pq(html)

    def parse_ng_repeat(self):
        PATTERN = re.compile(r'^\s*([a-zA-Z][a-zA-Z0-9_]*)\s+in\s+([a-zA-Z][a-zA-Z0-9_]*)\s*$')
        for attr in ['ng-repeat', 'data-ng-repeat']:
            for ele in self.d('[{}]'.format(attr)):
                ele = pq(ele)
                attr_value = ele.attr(attr)
                match = PATTERN.search(attr_value)
                if not match:
                    continue
                dj_start = '{{% for {} in {} %}}\n'.format(match.group(1),  match.group(2))
                dj_end = '{% endfor %}\n'
                ele.before(dj_start).after(dj_end)
                ele.remove_attr(attr)
        return self.d

    def parse_ng_style(self):
        for attr in ['ng-style', 'data-ng-style']:
            for ele in self.d('[{}]'.format(attr)):
                pq_ele = pq(ele)
                attr_value = pq_ele.attr(attr)
                dj = '{{{{ {}|ngstyle }}}}'.format(attr_value)
                ele.attrib['style'] = dj
                pq_ele.remove_attr(attr)
        return self.d

    def remove_attr(self):
        attrs = ['ng-click', 'ng-class', 'ng-attr-class']
        for attr in attrs:
            self.d('[{}]'.format(attr)).remove_attr(attr)

    def parse_all(self):
        self.parse_ng_repeat()
        self.parse_ng_style()
        self.remove_attr()
        return self.d

    def __str__(self):
        return unicode(self.d)


if __name__ == '__main__':
    angular_template = """
        <html>
            <div class="items" ng-style="root.style">
                <div ng-repeat="item in items">
                    <span>{{ item.name }}</span>
                </div>
            </div>
            <button ng-click="save()">save</button>
        </html>
        """
    d = Angango(angular_template)
    d.parse_all()
    print d
