import unittest
import yaml

from halucinator.config import Config

cortexm_memory = """---
memory_map:
  ram:  {base_addr:  0x20000000, size: 0x00400000, permissions: rwx}
  mmio: {base_addr:  0x40000000, size: 0x10000000, permissions: rw-}
  nvic: {base_addr:  0xe0000000, size: 0x10000000, permissions: rw-}
  irq_ret: {base_addr: 0xfffff000, size: 0x1000, permissions: rwx} 
initial_sp: 0x20014000
"""

mcuexpress = """---
memory_map:
  nxp_rom: {base_addr: 0x1fff0000, size: 0x10000, permissions: rwx}
handlers:
  CLOCK_InitOsc0:
    handler:
  CLOCK_SetInternalRefClkConfig:
    handler:
  CLOCK_BootToPeeMode:
    handler:
  UART_WriteBlocking:
    handler: hal_fuzz.handlers.mcuxpresso.UART_WriteBlocking
  UART_ReadBlocking:
    handler: hal_fuzz.handlers.mcuxpresso.UART_ReadBlocking
  PHY_Init:
    handler: hal_fuzz.handlers.generic.return_zero
  ENET_GetRxFrameSize:
    handler: hal_fuzz.handlers.mcuxpresso.ENET_GetRxFrameSize
  ENET_SendFrame:
    handler: hal_fuzz.handlers.mcuxpresso.ENET_SendFrame
  ENET_ReadFrame:
    handler: hal_fuzz.handlers.mcuxpresso.ENET_ReadFrame
  PHY_GetLinkStatus:
    handler: hal_fuzz.handlers.mcuxpresso.PHY_GetLinkStatus
  PHY_GetLinkSpeedDuplex:
    handler: hal_fuzz.handlers.mcuxpresso.PHY_GetLinkSpeedDuplex
  sys_now:
    handler: hal_fuzz.handlers.mcuxpresso.sys_now
"""

nxp_lwip_http_addrs = """---
architecture: ARMCortexM
base_address: 0
entry_point: 1221
symbols:
  1105: _start
  1733: strcmp
  1753: strlen
  2701: SysTick_Handler
  2713: main
  3213: BOARD_InitPins
  3521: BOARD_InitDebugConsole
  3673: BOARD_BootClockRUN
  3893: PHY_Init
  4193: PHY_Write
  4305: PHY_Read
  4425: PHY_GetLinkStatus
  4497: PHY_GetLinkSpeedDuplex
  7289: httpd_init
  8449: ethernetif_input
  8769: ethernetif0_init
  9525: CLOCK_GetOsc0ErClkFreq
  9565: CLOCK_GetEr32kClkFreq
  9657: CLOCK_GetPllFllSelClkFreq
  9741: CLOCK_GetCoreSysClkFreq
  9781: CLOCK_GetFreq
  10109: CLOCK_SetSimConfig
  10165: CLOCK_GetOutClkFreq
  10265: CLOCK_GetFllFreq
  10389: CLOCK_GetInternalRefClkFreq
  10425: CLOCK_GetFixedFreqClkFreq
  10473: CLOCK_GetPll0Freq
  10561: CLOCK_SetExternalRefClkConfig
  10669: CLOCK_SetInternalRefClkConfig
  10929: CLOCK_EnablePll0
  11049: CLOCK_InitOsc0
  11189: CLOCK_SetPbeMode
  11341: CLOCK_BootToPeeMode
  11729: ENET_GetInstance
  11785: ENET_GetDefaultConfig
  11845: ENET_Init
  13247: ENET_SetMacAddr
  13341: ENET_SetSMI
  13465: ENET_StartSMIWrite
  13543: ENET_StartSMIRead
  13615: ENET_GetRxFrameSize
  13795: ENET_ReadFrame
  14261: ENET_SendFrame
  14653: ENET_TransmitIRQHandler
  14721: ENET_ReceiveIRQHandler
  14789: ENET_ErrorIRQHandler
  14913: ENET_Transmit_IRQHandler
  14953: ENET_Receive_IRQHandler
  14993: ENET_Error_IRQHandler
  15033: ENET_1588_Timer_IRQHandler
  15557: StrFormatPrintf
  17449: DbgConsole_SendData
  17605: DbgConsole_Init
  17805: DbgConsole_Printf
  17957: UART_GetInstance
  18025: UART_Init
  18537: UART_GetDefaultConfig
  18625: UART_WriteBlocking
  18685: UART0_DriverIRQHandler
  18725: UART0_RX_TX_DriverIRQHandler
  18741: UART1_DriverIRQHandler
  18781: UART1_RX_TX_DriverIRQHandler
  18797: UART2_DriverIRQHandler
  18837: UART2_RX_TX_DriverIRQHandler
  18853: UART3_DriverIRQHandler
  18893: UART3_RX_TX_DriverIRQHandler
  18909: UART4_DriverIRQHandler
  18949: UART4_RX_TX_DriverIRQHandler
  18965: UART5_DriverIRQHandler
  19005: UART5_RX_TX_DriverIRQHandler
  19021: SystemInit
  19105: HAL_UartInit
  19293: HAL_UartSendBlocking
  19457: SerialManager_Init
  19539: SerialManager_OpenWriteHandle
  19593: SerialManager_OpenReadHandle
  19657: SerialManager_WriteBlocking
  19689: Serial_UartInit
  19785: Serial_UartWrite
  19825: fs_open
  19949: fs_close
  19967: fs_bytes_left
  20209: sys_assert
  20237: time_isr
  20265: time_init
  20393: sys_now
  20413: sys_arch_protect
  20435: sys_arch_unprotect
  20457: lwip_htons
  20483: lwip_htonl
  20531: lwip_strnstr
  20639: lwip_standard_chksum
  21039: inet_chksum_pseudo
  21151: ip_chksum_pseudo
  21195: inet_chksum
  21231: inet_chksum_pbuf
  21379: lwip_init
  21685: mem_init
  21805: mem_free
  21977: mem_trim
  22405: mem_malloc
  22829: memp_init_pool
  22921: memp_init
  23057: memp_malloc
  23189: memp_free
  23257: netif_init
  23269: netif_add
  23437: netif_set_addr
  23525: netif_set_ipaddr
  23637: netif_set_gw
  23675: netif_set_netmask
  23713: netif_set_default
  23741: netif_set_up
  23877: pbuf_alloc
  24601: pbuf_alloced_custom
  24797: pbuf_realloc
  25389: pbuf_header
  25425: pbuf_header_force
  25461: pbuf_free
  25729: pbuf_clen
  25773: pbuf_ref
  25837: pbuf_cat
  25977: pbuf_chain
  26009: pbuf_copy
  26361: pbuf_copy_partial
  26581: tcp_init
  26593: tcp_tmr
  26785: tcp_backlog_accepted
  27529: tcp_close
  27577: tcp_abandon
  27905: tcp_abort
  27929: tcp_bind
  28237: tcp_listen_with_backlog
  28273: tcp_listen_with_backlog_and_err
  28601: tcp_update_rcv_ann_wnd
  28741: tcp_recved
  29037: tcp_slowtmr
  30297: tcp_fasttmr
  30497: tcp_process_refused_data
  30701: tcp_segs_free
  30741: tcp_seg_free
  30789: tcp_setprio
  30817: tcp_recv_null
  31245: tcp_alloc
  31501: tcp_new_ip_type
  31529: tcp_arg
  31561: tcp_recv
  31609: tcp_sent
  31657: tcp_err
  31709: tcp_accept
  31753: tcp_poll
  31809: tcp_pcb_purge
  31929: tcp_pcb_remove
  32125: tcp_next_iss
  32169: tcp_eff_send_mss_impl
  32309: tcp_netif_ip_addr_changed
  32437: tcp_input
  39693: tcp_trigger_input_pcb_close
  39957: tcp_send_fin
  40741: tcp_write
  42473: tcp_enqueue_flags
  42929: tcp_send_empty_ack
  43149: tcp_output
  44469: tcp_rst
  44717: tcp_rexmit_rto
  44843: tcp_rexmit
  45003: tcp_rexmit_fast
  45177: tcp_keepalive
  45335: tcp_zero_window_probe
  45753: tcp_timer_needed
  45861: sys_timeouts_init
  45941: sys_timeout
  46253: sys_check_timeouts
  46401: udp_init
  46641: udp_input
  47133: udp_sendto_if
  47257: udp_sendto_if_src
  47601: udp_bind
  47825: udp_netif_ip_addr_changed
  48353: dhcp_coarse_tmr
  48521: dhcp_fine_tmr
  48961: dhcp_arp_reply
  49937: dhcp_renew
  50769: dhcp_release
  52417: dhcp_supplied_address
  52685: etharp_tmr
  53949: etharp_input
  54529: etharp_output
  54973: etharp_query
  55925: etharp_request
  55961: icmp_input
  56549: icmp_dest_unreach
  56581: icmp_time_exceeded
  56825: ip4_route
  57037: ip4_input
  57765: ip4_output_if
  57849: ip4_output_if_src
  58345: ip4_addr_isbroadcast_u32
  58473: ip_reass_tmr
  59913: ip4_reass
  60745: ip4_frag
  61301: ethernet_input
  61601: ethernet_output
  61729: exit
  61769: __libc_init_array
  61841: memcmp
  61871: memcpy
  61893: memset
  61909: strchr
  61935: strncmp
  74021: _init
  74033: _fini
"""

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
    handler: hal_fuzz.handlers.generic.return_zero
"""

test_outcome = """---
architecture: ARMCortexM
base_address: 0
entry_point: 1221
handlers:
  ip_chksum_pseudo:
    handler: hal_fuzz.handlers.generic.return_zero
  inet_chksum:
    handler: hal_fuzz.handlers.generic.return_zero
  tcp_next_iss:
    handler: hal_fuzz.handlers.generic.return_zero
  CLOCK_InitOsc0:
    handler:
  CLOCK_SetInternalRefClkConfig:
    handler:
  CLOCK_BootToPeeMode:
    handler:
  UART_WriteBlocking:
    handler: hal_fuzz.handlers.mcuxpresso.UART_WriteBlocking
  UART_ReadBlocking:
    handler: hal_fuzz.handlers.mcuxpresso.UART_ReadBlocking
  PHY_Init:
    handler: hal_fuzz.handlers.generic.return_zero
  ENET_GetRxFrameSize:
    handler: hal_fuzz.handlers.mcuxpresso.ENET_GetRxFrameSize
  ENET_SendFrame:
    handler: hal_fuzz.handlers.mcuxpresso.ENET_SendFrame
  ENET_ReadFrame:
    handler: hal_fuzz.handlers.mcuxpresso.ENET_ReadFrame
  PHY_GetLinkStatus:
    handler: hal_fuzz.handlers.mcuxpresso.PHY_GetLinkStatus
  PHY_GetLinkSpeedDuplex:
    handler: hal_fuzz.handlers.mcuxpresso.PHY_GetLinkSpeedDuplex
  sys_now:
    handler: hal_fuzz.handlers.mcuxpresso.sys_now
memory_map:
  irq_ret: {base_addr: 0xfffff000, size: 0x1000, permissions: rwx} 
  mmio: {base_addr:  0x40000000, size: 0x10000000, permissions: rw-}
  nvic: {base_addr:  0xe0000000, size: 0x10000000, permissions: rw-}
  nxp_rom: {base_addr: 0x1fff0000, size: 0x10000, permissions: rwx}
  ram:  {base_addr:  0x20000000, size: 0x00400000, permissions: rwx}
initial_sp: 0x20014000
symbols:
  1105: _start
  1733: strcmp
  1753: strlen
  2701: SysTick_Handler
  2713: main
  3213: BOARD_InitPins
  3521: BOARD_InitDebugConsole
  3673: BOARD_BootClockRUN
  3893: PHY_Init
  4193: PHY_Write
  4305: PHY_Read
  4425: PHY_GetLinkStatus
  4497: PHY_GetLinkSpeedDuplex
  7289: httpd_init
  8449: ethernetif_input
  8769: ethernetif0_init
  9525: CLOCK_GetOsc0ErClkFreq
  9565: CLOCK_GetEr32kClkFreq
  9657: CLOCK_GetPllFllSelClkFreq
  9741: CLOCK_GetCoreSysClkFreq
  9781: CLOCK_GetFreq
  10109: CLOCK_SetSimConfig
  10165: CLOCK_GetOutClkFreq
  10265: CLOCK_GetFllFreq
  10389: CLOCK_GetInternalRefClkFreq
  10425: CLOCK_GetFixedFreqClkFreq
  10473: CLOCK_GetPll0Freq
  10561: CLOCK_SetExternalRefClkConfig
  10669: CLOCK_SetInternalRefClkConfig
  10929: CLOCK_EnablePll0
  11049: CLOCK_InitOsc0
  11189: CLOCK_SetPbeMode
  11341: CLOCK_BootToPeeMode
  11729: ENET_GetInstance
  11785: ENET_GetDefaultConfig
  11845: ENET_Init
  13247: ENET_SetMacAddr
  13341: ENET_SetSMI
  13465: ENET_StartSMIWrite
  13543: ENET_StartSMIRead
  13615: ENET_GetRxFrameSize
  13795: ENET_ReadFrame
  14261: ENET_SendFrame
  14653: ENET_TransmitIRQHandler
  14721: ENET_ReceiveIRQHandler
  14789: ENET_ErrorIRQHandler
  14913: ENET_Transmit_IRQHandler
  14953: ENET_Receive_IRQHandler
  14993: ENET_Error_IRQHandler
  15033: ENET_1588_Timer_IRQHandler
  15557: StrFormatPrintf
  17449: DbgConsole_SendData
  17605: DbgConsole_Init
  17805: DbgConsole_Printf
  17957: UART_GetInstance
  18025: UART_Init
  18537: UART_GetDefaultConfig
  18625: UART_WriteBlocking
  18685: UART0_DriverIRQHandler
  18725: UART0_RX_TX_DriverIRQHandler
  18741: UART1_DriverIRQHandler
  18781: UART1_RX_TX_DriverIRQHandler
  18797: UART2_DriverIRQHandler
  18837: UART2_RX_TX_DriverIRQHandler
  18853: UART3_DriverIRQHandler
  18893: UART3_RX_TX_DriverIRQHandler
  18909: UART4_DriverIRQHandler
  18949: UART4_RX_TX_DriverIRQHandler
  18965: UART5_DriverIRQHandler
  19005: UART5_RX_TX_DriverIRQHandler
  19021: SystemInit
  19105: HAL_UartInit
  19293: HAL_UartSendBlocking
  19457: SerialManager_Init
  19539: SerialManager_OpenWriteHandle
  19593: SerialManager_OpenReadHandle
  19657: SerialManager_WriteBlocking
  19689: Serial_UartInit
  19785: Serial_UartWrite
  19825: fs_open
  19949: fs_close
  19967: fs_bytes_left
  20209: sys_assert
  20237: time_isr
  20265: time_init
  20393: sys_now
  20413: sys_arch_protect
  20435: sys_arch_unprotect
  20457: lwip_htons
  20483: lwip_htonlcortexm
  20531: lwip_strnstr
  20639: lwip_standard_chksum
  21039: inet_chksum_pseudo
  21151: ip_chksum_pseudo
  21195: inet_chksum
  21231: inet_chksum_pbuf
  21379: lwip_init
  21685: mem_init
  21805: mem_free
  21977: mem_trim
  22405: mem_malloc
  22829: memp_init_pool
  22921: memp_init
  23057: memp_malloc
  23189: memp_free
  23257: netif_init
  23269: netif_add
  23437: netif_set_addr
  23525: netif_set_ipaddr
  23637: netif_set_gw
  23675: netif_set_netmask
  23713: netif_set_default
  23741: netif_set_up
  23877: pbuf_alloc
  24601: pbuf_alloced_custom
  24797: pbuf_realloc
  25389: pbuf_header
  25425: pbuf_header_force
  25461: pbuf_free
  25729: pbuf_clen
  25773: pbuf_ref
  25837: pbuf_cat
  25977: pbuf_chain
  26009: pbuf_copy
  26361: pbuf_copy_partial
  26581: tcp_init
  26593: tcp_tmr
  26785: tcp_backlog_accepted
  27529: tcp_close
  27577: tcp_abandon
  27905: tcp_abort
  27929: tcp_bind
  28237: tcp_listen_with_backlog
  28273: tcp_listen_with_backlog_and_err
  28601: tcp_update_rcv_ann_wnd
  28741: tcp_recved
  29037: tcp_slowtmr
  30297: tcp_fasttmr
  30497: tcp_process_refused_data
  30701: tcp_segs_free
  30741: tcp_seg_free
  30789: tcp_setprio
  30817: tcp_recv_null
  31245: tcp_alloc
  31501: tcp_new_ip_type
  31529: tcp_arg
  31561: tcp_recv
  31609: tcp_sent
  31657: tcp_err
  31709: tcp_accept
  31753: tcp_poll
  31809: tcp_pcb_purge
  31929: tcp_pcb_remove
  32125: tcp_next_iss
  32169: tcp_eff_send_mss_impl
  32309: tcp_netif_ip_addr_changed
  32437: tcp_input
  39693: tcp_trigger_input_pcb_close
  39957: tcp_send_fin
  40741: tcp_write
  42473: tcp_enqueue_flags
  42929: tcp_send_empty_ack
  43149: tcp_output
  44469: tcp_rst
  44717: tcp_rexmit_rto
  44843: tcp_rexmit
  45003: tcp_rexmit_fast
  45177: tcp_keepalive
  45335: tcp_zero_window_probe
  45753: tcp_timer_needed
  45861: sys_timeouts_init
  45941: sys_timeout
  46253: sys_check_timeouts
  46401: udp_init
  46641: udp_input
  47133: udp_sendto_if
  47257: udp_sendto_if_src
  47601: udp_bind
  47825: udp_netif_ip_addr_changed
  48353: dhcp_coarse_tmr
  48521: dhcp_fine_tmr
  48961: dhcp_arp_reply
  49937: dhcp_renew
  50769: dhcp_release
  52417: dhcp_supplied_address
  52685: etharp_tmr
  53949: etharp_input
  54529: etharp_output
  54973: etharp_query
  55925: etharp_request
  55961: icmp_input
  56549: icmp_dest_unreach
  56581: icmp_time_exceeded
  56825: ip4_route
  57037: ip4_input
  57765: ip4_output_if
  57849: ip4_output_if_src
  58345: ip4_addr_isbroadcast_u32
  58473: ip_reass_tmr
  59913: ip4_reass
  60745: ip4_frag
  61301: ethernet_input
  61601: ethernet_output
  61729: exit
  61769: __libc_init_array
  61841: memcmp
  61871: memcpy
  61893: memset
  61909: strchr
  61935: strncmp
  74021: _init
  74033: _fini
use_nvic: False
use_timers: True
"""

def filepathresolver(path):
    if path.endswith("hw/cortexm_memory.yml"):
        return cortexm_memory
    elif path.endswith("hals/mcuxpresso.yml"):
        return mcuexpress
    elif path.endswith("nxp_lwip_http_addrs.yml"):
        return nxp_lwip_http_addrs
    elif path.endswith("example.yaml"):
        return example_file
    else:
        raise ValueError("Invalid file %s", path)

class TestConfigParser(unittest.TestCase):

    def testLoad(self):
        cfg = Config.load_from_yaml_file("example.yaml", filepathresolver)
        cfg.resolve_includes(filepathresolver)

        testcase = Config(yaml.load(test_outcome, Loader=yaml.FullLoader))

        diff = { k : testcase[k] for k in set(testcase) - set(cfg) }
        self.assertFalse(diff)

        

