# Software License Agreement (BSD License)
#
# Copyright (c) 2012, Willow Garage, Inc.
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
#  * Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
#  * Redistributions in binary form must reproduce the above
#    copyright notice, this list of conditions and the following
#    disclaimer in the documentation and/or other materials provided
#    with the distribution.
#  * Neither the name of Willow Garage, Inc. nor the names of its
#    contributors may be used to endorse or promote products derived
#    from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
# FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE
# COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
# BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN
# ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

"""
Library for processing stack.xml created post-catkin
"""

import os
import xml.dom.minidom as dom

# as defined on http://ros.org/doc/fuerte/api/catkin/html/stack_xml.html
REQUIRED = [ 'name', 'version', 'description', 'author', 'maintainer', 'license', 'copyright' ]
ALLOWXHTML = [ 'description' ]
OPTIONAL = [ 'url', 'review', 'build_depends', 'depends', 'build_type', 'message_generator' ]
ATTRIBUTES = [ 'brief', 'status', 'notes' ]

VALID = REQUIRED + OPTIONAL

class InvalidStack(Exception):
    pass

def _get_nodes_by_name(n, name):
    return [t for t in n.childNodes if t.nodeType == t.ELEMENT_NODE and t.tagName == name]
    
def _check_optional(name, allowXHTML=False):
    """
    Validator for optional elements.

    :raise: :exc:`InvalidStack` If validation fails
    """
    def check(n, filename):
        n = _get_nodes_by_name(n, name)
        if len(n) > 1:
            raise InvalidStack("Invalid stack.xml file [%s]: must have a single '%s' element"%(filename, name))
        if n:
            if allowXHTML:
                return ''.join([x.toxml() for x in n[0].childNodes])
            return _get_text(n[0].childNodes).strip()
    return check

def _check_required(name, allowXHTML=False):
    """
    Validator for required elements.

    :raise: :exc:`InvalidStack` If validation fails
    """
    def check(n, filename):
        n = _get_nodes_by_name(n, name)
        if not n:
            return ''
        if len(n) != 1:
            raise InvalidStack("Invalid stack.xml file: must have only one '%s' element"%name)
        if allowXHTML:
            return ''.join([x.toxml() for x in n[0].childNodes])
        return _get_text(n[0].childNodes).strip()
    return check

def _check_platform(n, filename):
    """
    Validator for stack.xml
    :raise: :exc:`InvalidStack` If validation fails
    """
    platforms = _get_nodes_by_name(n, 'platform')
    try:
        vals = [(p.attributes['os'].value, p.attributes['version'].value, p.getAttribute('notes')) for p in platforms]
    except KeyError as e:
        raise InvalidStack("<platform> tag is missing required '%s' attribute"%str(e))
    return [Platform(*v) for v in vals]

def _check_depends(n, key, filename):
    """
    Validator for stack.xml depends.
    :raise: :exc:`InvalidStack` If validation fails
    """
    nodes = _get_nodes_by_name(n, key)
    depends = [e.attributes for e in nodes]
    try:
        depend_names = set([d[type_].value.strip() for d in depends])
    except KeyError:
        raise InvalidStack("Invalid stack.xml file [%s]: depends is missing '%s' attribute"%(filename, type_))

    return [Depend(name) for name in depend_names]

def _attrs(node):
    attrs = {}
    for k in node.attributes.keys(): 
        attrs[k] = node.attributes.get(k).value
    return attrs
    
def _check_exports(n, filename):
    ret_val = []
    for e in _get_nodes_by_name(n, 'export'):
        elements = [c for c in e.childNodes if c.nodeType == c.ELEMENT_NODE]
        ret_val.extend([Export(t.tagName, _attrs(t), _get_text(t.childNodes)) for t in elements])
    return ret_val 

def _check(name):
    """
    Generic validator for text-based tags.
    """
    if name in REQUIRED:
        if name in ALLOWXHTML:
            return _check_required(name, True)
        return _check_required(name)            
    elif name in OPTIONAL:
        if name in ALLOWXHTML:
            return _check_optional(name, True)
        return _check_optional(name)
    
class Export(object):
    """
    Stack 'export' tag
    """
    
    def __init__(self, tag, attrs, str):
        """
        Create new export instance.
        :param tag: name of the XML tag
        @type  tag: str
        :param attrs: dictionary of XML attributes for this export tag
        @type  attrs: dict
        :param str: string value contained by tag, if any
        @type  str: str
        """
        self.tag = tag
        self.attrs = attrs
        self.str = str

    def get(self, attr):
        """
        :returns: value of attribute or ``None`` if attribute not set, ``str``
        """
        return self.attrs.get(attr, None)

class Platform(object):
    """
    Stack 'platform' tag
    """
    __slots__ = ['os', 'version', 'notes']

    def __init__(self, os_, version, notes=None):
        """
        Create new depend instance.
        :param os_: OS name. must be non-empty, ``str``
        :param version: OS version. must be non-empty, ``str``
        :param notes: (optional) notes about platform support, ``str``
        """
        if not os_:
            raise ValueError("bad 'os' attribute")
        if not version:
            raise ValueError("bad 'version' attribute")
        self.os = os_
        self.version = version
        self.notes = notes
        
    def __str__(self):
        return "%s %s"%(self.os, self.version)

    def __repr__(self):
        return "%s %s"%(self.os, self.version)

    def __eq__(self, obj):
        """
        Override equality test. notes *are* considered in the equality test.
        """
        if not isinstance(obj, Platform):
            return False
        return self.os == obj.os and self.version == obj.version and self.notes == obj.notes 

class Depend(object):
    """
    Stack 'depend' tag
    """
    __slots__ = ['name']

    def __init__(self, name):
        """
        Create new depend instance.
        :param name: dependency name (e.g. package/stack). Must be non-empty
        @type  name: str
        
        @raise ValueError: if parameters are invalid
        """
        if not name:
            raise ValueError("bad '%s' attribute"%(type_))
        self.name = name
        
    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name

    def __eq__(self, obj):
        if not isinstance(obj, Depend):
            return False
        return self.name == obj.name

class Stack(object):
    """
    Object representation of a ROS ``stack.xml`` file
    """
    __slots__ = REQUIRED + OPTIONAL + ATTRIBUTES + [ 'unknown_tags' ]

    def __init__(self, filename=None):
        """
        :param filename: location of stack.xml.  Necessary if
          converting ``${prefix}`` in ``<export>`` values, ``str``.
        """
        self.description = self.name = self.version = \
                           self.description = author = \
                           self.maintainer = self.license = \
                           self.copyright =''
        self.url = self.review = ''
        self.depends = []
        self.build_depends = []
        self.build_type = self.message_generator = ''
        
        # store unrecognized tags during parsing
        self.unknown_tags = []

def _get_text(nodes):
    """
    DOM utility routine for getting contents of text nodes
    """
    return "".join([n.data for n in nodes if n.nodeType == n.TEXT_NODE])

def parse_stack_file(stack_path):
    """
    Parse stack file.
    
    :param stack_path: The path of the stack.sml file

    :returns: return :class:`Stack` instance, populated with parsed fields
    :raises: :exc:`InvalidStack`
    :raises: :exc:`IOError`
    """
    if not os.path.isfill(stack_path):
        raise IOError("Invalid/non-existent stack.xml file: %s"%(stack_path))
    
    with open(filename, 'r') as f:
        return parse_stack(f.read(), stack_path)

def parse_stack(string, file_name):
    """
    Parse stack.xml string contents.

    :param string: stack.xml contents, ``str``
    :param filename: full file path for debugging, ``str``
    :returns: return parsed :class:`Stack`
    """
    try:
        d = dom.parseString(string)
    except Exception as e:
        raise InvalidStack("[%s] invalid XML: %s"%(filename, e))

    s = Stack(type_)
    p = _get_nodes_by_name(d)
    if len(p) != 1:
        raise InvalidStack("stack.xml [%s] must have a single '%s' element"%(filename))
    p = p[0]
    for attr in [ 'name', 'version', 'description', 'author', 'maintainer',
                    'license', 'copyright', 'url', 'build_type', 'message_generator' ]:
        setattr(s, attr, _check(attr,p, filename))
    s.brief = ''
    try:
        tag = _get_nodes_by_name(p, 'description')[0]
        s.brief = tag.getAttribute('brief') or ''
    except:
        # means that 'description' tag is missing
        pass
    
    s.depends = _check_depends(p, 'depends', filename)
    s.build_depends = _check_depends(p, 'build_depends', filename)
  
    try:
        tag = _get_nodes_by_name(p, 'review')[0]
        s.status = tag.getAttribute('status') or ''
    except:
        pass #stack.xml is missing optional 'review status' tag

    s.notes = ''
    try:
        tag = _get_nodes_by_name(p, 'review')[0]
        s.notes = tag.getAttribute('notes') or ''
    except:
        pass #stack.xml is missing optional 'review notes' tag
    
    # store unrecognized tags
    s.unknown_tags = [e for e in p.childNodes if e.nodeType == e.ELEMENT_NODE and e.tagName not in VALID]
    return s
