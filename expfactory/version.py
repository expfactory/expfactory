"""

Copyright (c) 2017-2022, Vanessa Sochat
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

* Redistributions of source code must retain the above copyright notice, this
  list of conditions and the following disclaimer.

* Redistributions in binary form must reproduce the above copyright notice,
  this list of conditions and the following disclaimer in the documentation
  and/or other materials provided with the distribution.

* Neither the name of the copyright holder nor the names of its
  contributors may be used to endorse or promote products derived from
  this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

"""

__version__ = "3.2.15"
AUTHOR = "Vanessa Sochat"
AUTHOR_EMAIL = "vsoch@users.noreply.github.com"
NAME = "expfactory"
PACKAGE_URL = "http://github.com/expfactory/expfactory"
KEYWORDS = "docker container reproducible behavior neuroscience experiment factory"
DESCRIPTION = "software to generate a reproducible container battery of experiments."
LICENSE = "LICENSE"

INSTALL_REQUIRES = (
    ("flask", {"min_version": "2.0"}),
    ("flask-restful", {"min_version": "0.3.6"}),
    ("flask-blueprint", {"exact_version": "1.2.2"}),
    ("Flask-WTF", {"min_version": "0.14.2"}),
    ("Flask-SQLAlchemy", {"min_version": "2.3.2"}),
    ("flask-cors", {"min_version": "3.0.6"}),
    ("markupsafe", {"min_version": "2.0.1"}),
    ("requests", {"min_version": "2.12.4"}),
    ("retrying", {"min_version": "1.3.3"}),
)

# Original working versions, in case needed
# flask 1.0.2
# Flask-Cors==3.0.6
# Flask-RESTful==0.3.6
# Flask-SQLAlchemy==2.3.2
# Flask-WTF==0.14.2
# flask-blueprint==1.2.2
