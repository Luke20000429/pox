# Copyright 2013 <Your Name Here>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at:
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
A skeleton POX component

You can customize this to do whatever you like.  Don't forget to
adjust the Copyright above, and to delete the Apache license if you
don't want to release under Apache (but consider doing so!).

Rename this file to whatever you like, .e.g., mycomponent.py.  You can
then invoke it with "./pox.py mycomponent" if you leave it in the
ext/ directory.

Implement a launch() function (as shown below) which accepts commandline
arguments and starts off your component (e.g., by listening to events).

Edit this docstring and your launch function's docstring.  These will
show up when used with the help component ("./pox.py help --mycomponent").
"""

# Import some POX stuff
from pox.core import core                     # Main POX object
import pox.openflow.libopenflow_01 as of      # OpenFlow 1.0 library
import pox.lib.packet as pkt                  # Packet parsing/construction
from pox.lib.addresses import EthAddr, IPAddr # Address types
import pox.lib.util as poxutil                # Various util functions
import pox.lib.revent as revent               # Event library
import pox.lib.recoco as recoco               # Multitasking library
from pox.lib.util import dpidToStr
from pox.core import POXCore

# Create a logger for this component
log = core.getLogger()
_verbose = None
_max_length = None
_types = None
_show_by_default = None

def _handle_ConnectionUp(event):
    log.info("Switch %s connected", event.connection.dpid)

    msg = of.ofp_flow_mod()
    msg.actions.append(of.ofp_action_output(port = of.OFPP_FLOOD))
    # event.connection.send(msg)
    # log.info("Hubifying %s", dpidToStr(event.dpid))
  
    # Add a flow entry that sends all packets to the controller
    # msg = of.ofp_flow_mod()
    # msg.match = of.ofp_match()
    msg.actions.append(of.ofp_action_output(port = of.OFPP_CONTROLLER)) # always send to controller
    event.connection.send(msg)

def _handle_PacketIn (event):
  packet = event.parsed
  print("Trigger Packet in at ", event.connection)
  # msg = of.ofp_packet_out()
  # msg.data = event.ofp
  # msg.actions.append(of.ofp_action_output(port = of.OFPP_FLOOD))
  # event.connection.send(msg)
  # show = _show_by_default
  # p = packet
  # while p:
  #   if p.__class__.__name__.lower() in _types:
  #     if _show_by_default:
  #       # This packet is hidden
  #       return
  #     else:
  #       # This packet should be shown
  #       show = True
  #       break
  #     return
  #   if not hasattr(p, 'next'): break
  #   p = p.next

  # if not show: return

  # msg = dpidToStr(event.dpid) + ": "
  # msg = ""
  # if _verbose:
  #   msg += packet.dump()
  # else:
  #   p = packet
  #   while p:
  #     if isinstance(p, bytes):
  #       msg += "[%s bytes]" % (len(p),)
  #       break
  #     elif isinstance(p, str):
  #       msg += "[%s chars]" % (len(p),)
  #       break
  #     msg += "[%s]" % (p.__class__.__name__,)
  #     p = p.next

  # if _max_length:
  #   if len(msg) > _max_length:
  #     msg = msg[:_max_length-3]
  #     msg += "..."
  # core.getLogger("stalking:" + dpidToStr(event.dpid)).debug(msg)


def _go_up (event):
  # Event handler called when POX goes into up state
  # (we actually listen to the event in launch() below)
  log.info("Skeleton application ready (to do nothing).")


@poxutil.eval_args
def launch (verbose = False, max_length = 110, full_packets = True,
            hide = False, show = False):
  """
  The default launcher just logs its arguments
  """

  # global _verbose, _max_length, _types, _show_by_default
  # _verbose = verbose
  # _max_length = max_length
  # force_show = (show is True) or (hide is False and show is False)
  # if isinstance(hide, str):
  #   hide = hide.replace(',', ' ').replace('|', ' ')
  #   hide = set([p.lower() for p in hide.split()])
  # else:
  #   hide = set()
  # if isinstance(show, str):
  #   show = show.replace(',', ' ').replace('|', ' ')
  #   show = set([p.lower() for p in show.split()])
  # else:
  #   show = set()

  # if hide and show:
  #   raise RuntimeError("Can't both show and hide packet types")

  # if show:
  #   _types = show
  # else:
  #   _types = hide
  # _show_by_default = not not hide
  # if force_show:
  #   _show_by_default = force_show

  # if full_packets:
  #   # Send full packets to controller
  #   core.openflow.miss_send_len = 0xffff

  core.addListenerByName("UpEvent", _go_up)
  core.openflow.addListenerByName("PacketIn", _handle_PacketIn)
  core.openflow.addListenerByName("ConnectionUp", _handle_ConnectionUp)
  # core.openflow.addListenerByName("QueueStatsReceived", _handle_PacketIn)

  log.info("Packet stalker running")
