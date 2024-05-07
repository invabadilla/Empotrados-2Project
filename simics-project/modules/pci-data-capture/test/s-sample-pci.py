# This Software is part of Simics. The rights to copy, distribute,
# modify, or otherwise make use of this Software may be licensed only
# pursuant to the terms of an applicable license agreement.
# 
# Copyright 2012-2021 Intel Corporation

# Tests for the sample PCI device.

import stest
import conf
import dev_util as du

# Set up a PCI bus and a sample PCI device
pci_bridge = du.Dev([du.PciBridge])  # Non-used PCI bridge, required by bus
pci_conf = SIM_create_object('memory-space', 'pci_conf', [])
pci_io = SIM_create_object('memory-space', 'pci_io', [])
pci_mem = SIM_create_object('memory-space', 'pci_mem', [])

pci_bus = SIM_create_object('pci-bus', 'pci_bus', [['conf_space', pci_conf],
                                                   ['io_space', pci_io],
                                                   ['memory_space', pci_mem],
                                                   ['bridge', pci_bridge.obj]])

pci = SIM_create_object('pci_data_capture', 'pci_data_capture',
                        [['pci_bus', pci_bus]])
                        
#regs = du.bank_regs(conf.dev.bank.regs)

# Test the PCI vendor and device IDs
def test_ids():
    stest.expect_equal(pci.attr.pci_config_vendor_id, 0x104c, "Bad vendor ID")
    stest.expect_equal(pci.attr.pci_config_device_id, 0xac10, "Bad device ID")

# Test the registers of the device
def test_regs():
    test_register = du.Register_LE((pci, 1, 0x0))
    stest.expect_different(test_register.read(), 32)
    print("test_register diff passed")
    
    test_register = du.Register_LE((pci, 1, 0x0))
    stest.expect_equal(test_register.read(), 0)
    print("test_register base 0 passed")
    
    BAR_1 = du.Register_LE((pci, 'pci_config', 0x10))
    stest.expect_different(BAR_1.read(), 4)
    print("BAR_1 Checked")
    
    BAR_2 = du.Register_LE((pci, 'pci_config', 0x14))
    stest.expect_equal(BAR_2.read(), 0)
    print("BAR_2 Checked")
    
    BAR_2 = du.Register_LE((pci, 'pci_config', 0x18))
    stest.expect_equal(BAR_2.read(), 0)
    print("BAR_2 Checked")
    
    BAR_3 = du.Register_LE((pci, 'pci_config', 0x1C))
    stest.expect_equal(BAR_3.read(), 0)
    print("BAR_3 Checked")
    
    BAR_4 = du.Register_LE((pci, 'pci_config', 0x20))
    stest.expect_equal(BAR_4.read(), 0)
    print("BAR_4 Checked")
    
    BAR_5 = du.Register_LE((pci, 'pci_config', 0x24))
    stest.expect_equal(BAR_5.read(), 0)
    print("BAR_5 Checked")

# Test setting BAR to map the device in memory
def test_mapping():
    cmd_reg = du.Register((pci, 'pci_config', 0x4), 0x2)  # PCI command register
    bar_reg = du.Register((pci, 'pci_config', 0x10), 0x4) # PCI BAR register

    addr = 0x100
    cmd_reg.write(2)     # Enable memory access
    bar_reg.write(addr)  # Map bank at addr
    
    base_add = 0x0
    mapped = du.Register_LE(pci.bank.regs, base_add)
    stest.expect_equal(mapped.read(), 0)
    print("Mapped reg test 1 pass")
   
    

test_ids()
test_regs()
test_mapping()

print("\nAll tests passed.\n")
