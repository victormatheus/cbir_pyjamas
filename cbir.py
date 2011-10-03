import pyjd # this is dummy in pyjs.
from pyjamas import DOM

from pyjamas.ui.RootPanel import RootPanel, RootPanelCls, manageRootPanel
from pyjamas.ui.HTML import HTML
from pyjamas.ui.Label import Label
from pyjamas.ui.Hyperlink import Hyperlink
from pyjamas.ui.HTML import HTML
from pyjamas.ui.Image import Image
from pyjamas.ui.Button import Button
from pyjamas.ui.DockPanel import DockPanel
from pyjamas.ui.VerticalPanel import VerticalPanel
from pyjamas.ui.HorizontalPanel import HorizontalPanel
from pyjamas.ui import HasAlignment
from pyjamas.ui.DockPanel import DockPanel
from pyjamas.ui.Composite import Composite
from pyjamas.ui.FlexTable import FlexTable

from pyjamas.HTTPRequest import HTTPRequest
from pyjamas.JSONParser import JSONParser
import urllib


import math
import pygwt
import random

from __pyjamas__ import JS

class CBIR(Composite):
  def __init__(self):
    Composite.__init__(self)

    panel = DockPanel(HorizontalAlignment=HasAlignment.ALIGN_CENTER,
                      VerticalAlignment=HasAlignment.ALIGN_MIDDLE)
    panel.setWidth("100%")

    vp = VerticalPanel()

    grid = FlexTable(CellPadding=4, CellSpacing=4)

    hp = HorizontalPanel()

    self.next   = Button("Next",    self, StyleName='button')
    self.finish = Button("Finish!", self, StyleName='button')
    self.clear  = Button("Clear",   self, StyleName='button')

    hp.add(self.clear)
    hp.add(self.finish)
    hp.add(self.next)
    hp.setWidth("70%")

    vp.add(Label("Content-Based Image Retrieval Using OPF", StyleName='label'))
    vp.add(grid)

    vp.setHorizontalAlignment(HasAlignment.ALIGN_RIGHT)
    vp.add(hp)

    cols = 4
    for i in range(100):
      im = Image('images/cbir/%d.jpg' % random.randint(0, 1000),  Size=("200px", "150px"), StyleName='image-cool')
      grid.setWidget(int(i/cols), i%cols, im)

    panel.add(vp, DockPanel.CENTER)

    self.initWidget(panel)

    self.status = Label()
    vp.add(self.status)

  def onCompletion(self, response):
    self.status.setText(response)

  def onModuleLoad(self):
    self.TEXT_WAITING = "Waiting for response..."
    self.TEXT_ERROR = "Server Error"

  def onClick(self, sender):
    self.status.setText(self.TEXT_WAITING)

    msg = JSONParser().encode( {'spam':1, 'eggs':2} )
    print msg

    params = urllib.quote(msg, safe="")

    header = {'Content-type': 'application/x-www-form-urlencoded', 'Accept':'application/json'}
    HTTPRequest().asyncPost(url="http://localhost:8000", postData=params, handler=self, headers=header)

class CBIRWeb:
  def onModuleLoad(self):
    self.cbir = CBIR()
    self.cbir.onModuleLoad()
    RootPanel().add(self.cbir)

if __name__ == '__main__':
    # for pyjd, set up a web server and load the HTML from there:
    # this convinces the browser engine that the AJAX will be loaded
    # from the same URI base as the URL, it's all a bit messy...
    pyjd.setup("public/index.html")
    app = CBIRWeb()
    app.onModuleLoad()
    pyjd.run()
