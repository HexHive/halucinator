import unittest
import yaml

example_file = """---
include:
  - library:hw/cortexm_memory.yml
  - library:hals/mcuxpresso.yml
  - nxp_lwip_http_addrs.yml

memory_map:
  flash: {base_addr: 0x0, file: ./nxp_lwip_http.bin,
    permissions: r-x, size: 0x800000}

use_nvic: False
use_timers: True

handlers:
  ip_chksum_pseudo:
    handler: hal_fuzz.handlers.generic.return_zero
  inet_chksum:
    handler: hal_fuzz.handlers.generic.return_zero
  tcp_next_iss:
    handler: hal_fuzz.handlers.generic.return_zero"""


class TestConfigParser(unittest.TestCase):

    def test_load(self):
        self.assertTrue(True)
