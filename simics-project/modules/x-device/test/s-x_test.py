import stest
import conf
import dev_util as du

dev = pre_conf_object('dev','x_device')
target_mem_space_test = SIM_create_object ('memory-space','target_mem_space',[])
dev.target_mem_space = target_mem_space_test

SIM_add_configuration([dev],None)
dev = conf.dev

buffer_size  = 5_000_000

def Log():
	pass

def Test():
	cmd = du.Register_LE(dev.bank.regs, 0x14, size=4)
	stest.expect_equal(cmd.read(),0)
	
	cmd.write(0x1)
	stest.expect_log_mgr(log_type = 'info')
	
	buff_size = du.Register_LE(dev.bank.regs, 0x4, size=4)
	stest.expect_equal(buff_size.read(),buffer_size)
	
	#buff = du.Register_LE(dev.bank.regs, 0x18, size=1)
	for i in range(0,buffer_size,100):
		buff = du.Register_LE(dev.bank.regs, 0x18+i, size=1)
		stest.expect_equal(buff.read(),0)
		print("Tested dir: "+str(0x18+i))


Test()
print("All tests passed");
