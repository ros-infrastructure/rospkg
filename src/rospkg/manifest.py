#! /usr/bin/env python
# Software License Agreement (BSD License)
#
# Copyright (c) 2008, Willow Garage, Inc.
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
#
# Revision $Id: manifestlib.py 14522 2011-08-02 23:02:48Z kwc $
# $Author: kwc $

"""
Library for processing 'manifest' files, i.e. manifest.xml and
stack.xml.  
"""

import sys
import os
import xml.dom
import xml.dom.minidom as dom

from .common import RosPkgException

# stack.xml and manifest.xml have the same internal tags right now
REQUIRED = ['author', 'license']
ALLOWXHTML = ['description']
OPTIONAL = ['logo', 'url', 'brief', 'description', 'status',
            'notes', 'depend', 'rosdep', 'export', 'review',
            'versioncontrol', 'platform', 'version', 'rosbuild2']
VALID = REQUIRED + OPTIONAL

class InvalidManifest(RosPkgException): pass

def get_nodes_by_name(n, name):
    return [t for t in n.childNodes if t.nodeType == t.ELEMENT_NODE and t.tagName == name]
    
def check_optional(name, allowXHTML=False):
    """
    Validator for optional elements.
    @raise InvalidManifest: if validation fails
    """
    def check(n, filename):
        n = get_nodes_by_name(n, name)
        if len(n) > 1:
            raise InvalidManifest("Invalid manifest file: must have a single '%s' element"%name)
        if n:
            if allowXHTML:
                return ''.join([x.toxml() for x in n[0].childNodes])
            return _get_text(n[0].childNodes).strip()
    return check

def check_required(name, allowXHTML=False):
    """
    Validator for required elements.
    @raise InvalidManifest: if validation fails
    """
    def check(n, filename):
        n = get_nodes_by_name(n, name)
        if not n:
            #print >> sys.stderr, "Invalid manifest file[%s]: missing required '%s' element"%(filename, name)
            return ''
        if len(n) != 1:
            raise InvalidManifest("Invalid manifest file: must have only one '%s' element"%name)
        if allowXHTML:
            return ''.join([x.toxml() for x in n[0].childNodes])
        return _get_text(n[0].childNodes).strip()
    return check

def check_platform(n, filename):
    """
    Validator for manifest platform.
    @raise InvalidManifest: if validation fails
    """
    platforms = get_nodes_by_name(n, 'platform')
    try:
        vals = [(p.attributes['os'].value, p.attributes['version'].value, p.getAttribute('notes')) for p in platforms]
    except KeyError as e:
        raise InvalidManifest("<platform> tag is missing required '%s' attribute"%str(e))
    return [Platform(*v) for v in vals]

def check_depends(type_, n, filename):
    """
    Validator for manifest depends.
    @raise InvalidManifest: if validation fails
    """
    nodes = get_nodes_by_name(n, name)
    # TDS 20110419:  this is a hack.
    # rosbuild2 has a <depend thirdparty="depname"/> tag,
    # which is confusing this subroutine with 
    # KeyError: 'package'
    # for now, explicitly don't consider thirdparty depends
    depends = [e.attributes for e in nodes if 'thirdparty' not in e.attributes.keys()]
    try:
        depend_names = [d[type_].value for d in depends]
    except KeyError:
        raise InvalidManifest("Invalid manifest file: depends is missing '%s' attribute"%(type_))

    return [Depend(name, type_) for name in depend_names]

def check_rosdeps(name):
    """
    Validator for stack rosdeps.    
    @raise InvalidManifest: if validation fails
    """
    nodes = get_nodes_by_name(n, 'rosdep')
    rosdeps = [e.attributes for e in nodes]
    names = [d['name'].value for d in rosdeps]
    return [RosDep(n) for n in names]

def _attrs(node):
    attrs = {}
    for k in node.attributes.keys(): 
        attrs[k] = node.attributes.get(k).value
    return attrs
    
def check_exports(name):
    ret_val = []
    for e in get_nodes_by_name(n, 'export'):
        elements = [c for c in e.childNodes if c.nodeType == c.ELEMENT_NODE]
        ret_val.extend([Export(t.tagName, _attrs(t), _get_text(t.childNodes)) for t in elements])
    return ret_val 

def check(name, type_):
    """
    Generic validator for text-based tags.
    """
    if name in REQUIRED:
        if name in ALLOWXHTML:
            return check_required(name, True)
        return check_required(name)            
    elif name in OPTIONAL:
        if name in ALLOWXHTML:
            return check_optional(name, True)
        return check_optional(name)
    
class Export(object):
    """
    Manifest 'export' tag
    """
    
    def __init__(self, tag, attrs, str):
        """
        Create new export instance.
        @param tag: name of the XML tag
        @type  tag: str
        @param attrs: dictionary of XML attributes for this export tag
        @type  attrs: dict
        @param str: string value contained by tag, if any
        @type  str: str
        """
        self.tag = tag
        self.attrs = attrs
        self.str = str

    def get(self, attr):
        """
        @return: value of attribute or None if attribute not set
        @rtype:  str
        """
        return self.attrs.get(attr, None)

    def xml(self):
        """
        @return: export instance represented as manifest XML
        @rtype: str
        """        
        attrs = ' '.join([' %s="%s"'%(k,v) for k,v in self.attrs.iteritems()])
        if self.str:
            return '<%s%s>%s</%s>'%(self.tag, attrs, self.str, self.tag)
        else:
            return '<%s%s />'%(self.tag, attrs)
        
class Platform(object):
    """
    Manifest 'platform' tag
    """
    __slots__ = ['os', 'version', 'notes']

    def __init__(self, os, version, notes=None):
        """
        Create new depend instance.
        @param os: OS name. must be non-empty
        @type  os: str
        @param version: OS version. must be non-empty
        @type  version: str
        @param notes: (optional) notes about platform support
        @type  notes: str
        """
        if not os or not isinstance(os, basestring):
            raise ValueError("bad 'os' attribute")
        if not version or not isinstance(version, basestring):
            raise ValueError("bad 'version' attribute")
        if notes and not isinstance(notes, basestring):
            raise ValueError("bad 'notes' attribute")            
        self.os = os
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

    def xml(self):
        """
        @return: instance represented as manifest XML
        @rtype: str
        """
        if self.notes is not None:
            return '<platform os="%s" version="%s" notes="%s"/>'%(self.os, self.version, self.notes)
        else:
            return '<platform os="%s" version="%s"/>'%(self.os, self.version)

class Depend(object):
    """
    Manifest 'depend' tag
    """
    __slots__ = ['name', 'type']

    def __init__(self, name, type_):
        """
        Create new depend instance.
        @param package: package name. must be non-empty
        @type  package: str
        """
        if not name:
            raise ValueError("bad '%s' attribute"%(type_))
        self.name = name
        self.type = type_
        
    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name

    def __eq__(self, obj):
        if not isinstance(obj, Depend):
            return False
        return self.name == obj.name and self.type == obj.type

    def xml(self):
        """
        @return: depend instance represented as manifest XML
        @rtype: str
        """
        return '<depend %s="%s" />'%(self.type, self.name)
        
class RosDep(object):
    """
    Manifest 'rosdep' tag    
    """
    __slots__ = ['name',]

    def __init__(self, name):
        """
        Create new rosdep instance.
        @param name: dependency name. Must be non-empty.
        @type  name: str
        """
        if not name or not isinstance(name, basestring):
            raise ValueError("bad 'name' attribute")
        self.name = name
    def xml(self):
        """
        @return: rosdep instance represented as manifest XML
        @rtype: str
        """        
        return '<rosdep name="%s" />'%self.name

class Manifest(object):
    """
    Object representation of a ROS manifest file (manifest.xml and stack.xml)
    """
    __slots__ = ['description', 'brief', \
                 'author', 'license', 'license_url', 'url', \
                 'depends', 'rosdeps','platforms',\
                 'exports', 'version',\
                 'status', 'notes',\
                 'unknown_tags',\
                 '_type']
    def __init__(self, _type='package'):
        self.description = self.brief = self.author = \
                           self.license = self.license_url = \
                           self.url = self.status = \
                           self.version = self.notes = ''
        self.depends = []
        self.rosdeps = []
        self.exports = []
        self.platforms = []
        self._type = _type
        
        # store unrecognized tags during parsing
        self.unknown_tags = []
        
    def __str__(self):
        return self.xml()

    def get_export(self, tag, attr):
        """
        @return: exports that match the specified tag and attribute, e.g. 'python', 'path'
        @rtype: [L{Export}]
        """
        return [e.get(attr) for e in self.exports if e.tag == tag if e.get(attr) is not None]

    def xml(self):
        """
        @return: Manifest instance as ROS XML manifest
        @rtype: str
        """
        if not self.brief:
            desc = "  <description>%s</description>"%self.description
        else:
            desc = '  <description brief="%s">%s</description>'%(self.brief, self.description) 
        author  = "  <author>%s</author>"%self.author
        if self.license_url:
            license = '  <license url="%s">%s</license>'%(self.license_url, self.license)
        else:
            license = "  <license>%s</license>"%self.license
        url = logo = exports = version = ""
        if self.url:
            url     = "  <url>%s</url>"%self.url
        if self.version:
            version = "  <version>%s</version>"%self.version
        if self.logo:
            logo    = "  <logo>%s</logo>"%self.logo
        depends = '\n'.join(["  %s"%d.xml() for d in self.depends])
        rosdeps = '\n'.join(["  %s"%rd.xml() for rd in self.rosdeps])
        platforms = '\n'.join(["  %s"%p.xml() for p in self.platforms])
        if self.exports:
            exports = '  <export>\n' + '\n'.join(["  %s"%e.xml() for e in self.exports]) + '  </export>'
        if self.status or self.notes:
            review = '  <review status="%s" notes="%s" />'%(self.status, self.notes)

        fields = filter(lambda x: x,
                        [desc, author, license, review, url, logo, depends,
                         rosdeps, platforms, exports, version])
        return "<%s>\n"%self._type + "\n".join(fields) + "\n</%s>"%self._type

def _get_text(nodes):
    """
    DOM utility routine for getting contents of text nodes
    """
    return "".join([n.data for n in nodes if n.nodeType == n.TEXT_NODE])

def parse_manifest_file(dirpath, filename):
    """
    Parse manifest file (package, stack).  Type will be inferred from filename.
    
    @param dirpath: directory of manifest file
    @type  dirpath: str
    @param filename: MANIFEST_FILE or STACK_FILE
    @type  filename: str
    
    @return: return m, populated with parsed fields
    @rtype: L{Manifest}

    @raise InvalidManifest
    @raise IOError
    """
    filepath = os.path.join(dirpath, filename)
    if not os.path.isfile(filepath):
        raise IOError("Invalid/non-existent manifest file: %s"%(filepath))
    
    with open(filepath, 'r') as f:
        return parse(filename, text, f.read())

def parse_manifest(type_, string, filename='string'):
    """
    Parse manifest string contents.

    @param filename: MANIFEST_FILE or STACK_FILE
    @type  filename: str
    @param string: manifest.xml contents
    @type  string: str
    @return: return parsed Manifest
    @rtype: L{Manifest}
    """
    if filename == MANIFEST_FILE:
        type_ = 'package'
    elif filename == STACK_FILE:
        type_ = 'stack'
        
    try:
        d = dom.parseString(string)
    except Exception as e:
        raise InvalidManifest("[%s] invalid XML: %s"%(filename, e))
    
    m = Manifest(type_)
    p = get_nodes_by_name(d, type_)
    if len(p) != 1:
        raise InvalidManifest("manifest [%s] must have a single '%s' element"%(filename, type_))
    p = p[0]
    m.description = check('description')(p, filename)
    m.brief = ''
    try:
        tag = get_nodes_by_name(p, 'description')[0]
        m.brief = tag.getAttribute('brief') or ''
    except:
        # means that 'description' tag is missing
        pass
    
    m.depends = check_depends(type_, p, filename)
    m.rosdeps = check_rosdeps(p, filename)    
    m.platforms = check_platform(p, filename)    
    m.exports = check_exports(p, filename)
    m.license = check('license')(p, filename)
    m.license_url = ''
    try:
        tag = get_nodes_by_name(p, 'license')[0]
        m.license_url = tag.getAttribute('url') or ''
    except:
        pass #manifest is missing required 'license' tag
  
    m.status='unreviewed'
    try:
        tag = get_nodes_by_name(p, 'review')[0]
        m.status = tag.getAttribute('status') or ''
    except:
        pass #manifest is missing optional 'review status' tag

    m.notes = ''
    try:
        tag = get_nodes_by_name(p, 'review')[0]
        m.notes = tag.getAttribute('notes') or ''
    except:
        pass #manifest is missing optional 'review notes' tag

    m.author = check('author')(p, filename)
    m.url = check('url')(p, filename)
    m.version = check('version')(p, filename)
    m.logo = check('logo')(p, filename)

    # do some validation on what we just parsed
    if type_ == 'stack':
        if m.exports:
            raise InvalidManifest("stack manifests are not allowed to have exports")
        if m.rosdeps:
            raise InvalidManifest("stack manifests are not allowed to have rosdeps") 

    # store unrecognized tags
    m.unknown_tags = [e for e in p.childNodes if e.nodeType == e.ELEMENT_NODE and e.tagName not in VALID]
    return m
