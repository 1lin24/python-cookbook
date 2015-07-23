# coding: utf-8

"""
Convert Angular template to Django template
"""

import re
import uuid
from pyquery import PyQuery as pq
import lxml.html as lh
import lxml.etree as le

class Angango(object):

    ATTR_BLACKLIST = ['ng-click', 'ng-class',
                      'click-text', 'click-link', 'click-image', 'click-richtext', 'click-button']
    REPLACE_MAP = {}

    def __init__(self, html):
        self.d = pq(html)

    def _extend_attr(self, attrs):
        for attr in attrs:
            yield attr
            if not attr.startswith('data-'):
                yield 'data-' + attr

    def parse_ng_repeat(self):
        PATTERN = re.compile(r'^\s*([\S]+)\s+in\s+([\S]+)\s*$')
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
                dj_str = '{{% if {} %}}{}{{% endif %}}'.format(dj_if, 'href="{}"'.format(attr_value))
                code = uuid.uuid4().hex
                self.REPLACE_MAP[code] = dj_str
                ele.attrib[code] = ''
                pq_ele.remove_attr(attr)

    def replace_attr(self, ele, attr, new_attr):
        PATTERN = re.compile(r'\{\{([^\{\}]*)\}\}')
        pq_ele = pq(ele)
        attr_value = pq_ele.attr(attr)
        dj_if = ' and '.join([i.strip() for i in PATTERN.findall(attr_value)])
        dj_str = '{{% if {} %}}{}{{% endif %}}'.format(dj_if, '{}="{}"'.format(new_attr, attr_value))
        code = uuid.uuid4().hex
        self.REPLACE_MAP[code] = dj_str
        ele.attrib[code] = ''
        pq_ele.remove_attr(attr)

    def parse_ng_attr(self):
        for ele in self.d('*'):
            for attr in ele.attrib.keys():
                for i in self._extend_attr(['ng-attr-']):
                    if attr.startswith(i):
                        new_attr = attr.replace('ng-attr-', '')
                        self.replace_attr(ele, attr, new_attr)

    def parse_ng_src(self):
        for attr in ['ng-src', 'data-ng-src']:
            for ele in self.d('[{}]'.format(attr)):
                pq_ele = pq(ele)
                attr_value = pq_ele.attr(attr)
                ele.attrib['src'] = attr_value
                pq_ele.remove_attr(attr)

    def parse_ng_bind(self):
        for attr in self._extend_attr(['ng-bind', 'ng-bind-html']):
            for ele in self.d('[{}]'.format(attr)):
                pq_ele = pq(ele)
                attr_value = pq_ele.attr(attr)
                dj_tpl = '{{{{ {} }}}}'.format(attr_value)
                pq_ele.html(dj_tpl)
                pq_ele.remove_attr(attr)


    def parse_ng_class(self):
        for attr in self._extend_attr(['ng-class']):
            for ele in self.d('[{}]'.format(attr)):
                pq_ele = pq(ele)
                attr_value = pq_ele.attr(attr)
                class_str = ele.attrib.get('class', '').split()
                class_str = (',').join(class_str)
                dj_tpl = """{{{{ {}|ngclass:'{}' }}}}""".format(attr_value, class_str)
                ele.attrib['class'] = dj_tpl

    def remove_attr(self):
        for attr in self._extend_attr(self.ATTR_BLACKLIST):
            self.d('[{}]'.format(attr)).remove_attr(attr)

    def remove_dom(self):
        for attr in ['ag-remove']:
            self.d('[{}]'.format(attr)).remove()

    def replace_code(self):
        html = unicode(self)
        for k, v in self.REPLACE_MAP.items():
            html = re.sub(k + r'=""', v, html)
        # Fix <div/> -> <div></div>
        # html = re.sub(r'<(\w+)([^/>]*)/>', r'<\1\2></\1>', html)
        return html

    def parse_all(self):
        self.remove_dom()
        self.parse_ng_repeat()
        self.parse_ng_style()
        self.parse_ng_href()
        self.parse_ng_src()
        self.parse_ng_bind()
        self.parse_ng_attr()
        self.parse_ng_class()
        self.remove_attr()
        return self.replace_code()

    def __str__(self):
        print le.tostring(self.d[0], encoding='utf-8', method='html')
        print lh.tostring(self.d[0], encoding='utf-8', pretty_print=True, method="html")
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
                    ng-href="http://{{ slide.components.image1.href }}/{{ pk }}"
                    ng-attr-target="{{ slide.components.image1.target }}">
                    <img ng-src="{{ slide.components.image1.value|qiniu }}">
                </a>
            </div>
            <div ng-bind-html="item.text2.value|safe" class="simditor-typo2" ng-style="item.text2.style"></div>
            <div class="s-root s-layout-a" ng-style="slide.style.root" ng-class="slide.class">
                test ng-class
            </div>

            <div class="todo"></div>
            <b></b>

            <div class="serBoxOn" style="display: none;"/>

        </html>
        """
    d = Angango(angular_template)
    print d.parse_all()
