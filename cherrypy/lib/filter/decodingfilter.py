"""
Copyright (c) 2004, CherryPy Team (team@cherrypy.org)
All rights reserved.

Redistribution and use in source and binary forms, with or without modification, 
are permitted provided that the following conditions are met:

    * Redistributions of source code must retain the above copyright notice, 
      this list of conditions and the following disclaimer.
    * Redistributions in binary form must reproduce the above copyright notice, 
      this list of conditions and the following disclaimer in the documentation 
      and/or other materials provided with the distribution.
    * Neither the name of the CherryPy Team nor the names of its contributors 
      may be used to endorse or promote products derived from this software 
      without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND 
ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED 
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE 
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE 
FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL 
DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR 
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER 
CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, 
OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE 
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
"""

from basefilter import BaseFilter

class DecodingFilter(BaseFilter):
    """Automatically decodes request parameters (except uploads)."""
    
    def onStartResource(self):
        # We have to dynamically import cpg because Python can't handle
        #   circular module imports :-(
        global cpg
        from cherrypy import cpg
        cpg.threadData.decodingFilterOn = cpg.config.get('decodingFilter.on', False)
        cpg.threadData.decodingFilterEncoding = cpg.config.get('decodingFilter.encoding', 'utf-8')
    
    def beforeMain(self):
        if not cpg.threadData.decodingFilterOn:
            return
        
        enc = cpg.threadData.decodingFilterEncoding
        for key, value in cpg.request.paramMap.items():
            if cpg.request.filenameMap.get(key):
                # This is a file being uploaded: skip it
                continue
            if isinstance(value, list):
                # value is a list: decode each element
                newValue = [v.decode(enc) for v in value]
            else:
                # value is a regular string: decode it
                newValue = value.decode(enc)
            cpg.request.paramMap[key] = newValue

