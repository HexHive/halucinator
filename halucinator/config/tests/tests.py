import unittest
import yaml

halfuzz_yaml = """include:
  - ./../../configs/hw/cortexm_memory.yml
  - ./../../configs/hals/mcuxpresso.yml
  - ./nxp_lwip_http_addrs.yml

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

extended_yaml = """include:
  - ./../../configs/hw/cortexm_memory.yml
  - ./../../configs/hals/mcuxpresso.yml
  - ./nxp_lwip_http_addrs.yml

memory_map:
  flash: {base_addr: 0x0, file: ./nxp_lwip_http.bin,
    permissions: r-x, size: 0x800000}
  include: "{{ library }}/file.yml"

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

        
        halfuzz = yaml.load('halfuzz_yaml', Loader=yaml.FullLoader)


        self.assertTrue(True)
