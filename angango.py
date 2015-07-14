# coding: utf-8

"""
Convert Angular template to Django template
"""

import re
from pyquery import PyQuery as pq


class Angango(object):

    ATTR_BLACKLIST = ['ng-click', 'ng-class', 'ng-attr-class', 'edit-image', 'edit-text']

    def __init__(self, html):
        self.d = pq(html)

    def _extend_attr(self, attrs):
        for attr in attrs:
            yield attr
            if not attr.startswith('data-'):
                yield 'data-' + attr

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

    def parse_ng_href(self):
        PATTERN = re.compile(r'\{\{([^\{\}]*)\}\}')
        for attr in ['ng-href', 'data-ng-href']:
            for ele in self.d('[{}]'.format(attr)):
                pq_ele = pq(ele)
                attr_value = pq_ele.attr(attr)
                dj_if = ' and '.join([i.strip() for i in PATTERN.findall(attr_value)])
                print '{{% if {} %}}{}{{% endif %}}'.format(dj_if, 'href="{}"'.format(attr_value))


    def parse_ng_src(self):
        pass

    def parse_ng_attr_target(self):
        pass

    def remove_attr(self):
        for attr in self._extend_attr(self.ATTR_BLACKLIST):
            self.d('[{}]'.format(attr)).remove_attr(attr)

    def parse_all(self):
        self.parse_ng_repeat()
        self.parse_ng_style()
        self.parse_ng_href()
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
            <div class="s-image1">
                <a data-edit-image="slide.components.image1"
                    ng-href="http://{{ slide.components.image1.href }}/{{ pk }}" ng-attr-target="{{ slide.components.image1.target }}">
                    <img ng-src="{{ slide.components.image1.value|qiniu }}">
                </a>
            </div>
        </html>
        """
    d = Angango(angular_template)
    d.parse_all()
    # print d
