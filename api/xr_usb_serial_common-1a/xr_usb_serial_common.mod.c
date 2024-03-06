#include <linux/module.h>
#define INCLUDE_VERMAGIC
#include <linux/build-salt.h>
#include <linux/elfnote-lto.h>
#include <linux/export-internal.h>
#include <linux/vermagic.h>
#include <linux/compiler.h>

BUILD_SALT;
BUILD_LTO_INFO;

MODULE_INFO(vermagic, VERMAGIC_STRING);
MODULE_INFO(name, KBUILD_MODNAME);

__visible struct module __this_module
__section(".gnu.linkonce.this_module") = {
	.name = KBUILD_MODNAME,
	.init = init_module,
#ifdef CONFIG_MODULE_UNLOAD
	.exit = cleanup_module,
#endif
	.arch = MODULE_ARCH_INIT,
};

#ifdef CONFIG_RETPOLINE
MODULE_INFO(retpoline, "Y");
#endif


static const struct modversion_info ____versions[]
__used __section("__versions") = {
	{ 0x34db050b, "_raw_spin_lock_irqsave" },
	{ 0xd35cce70, "_raw_spin_unlock_irqrestore" },
	{ 0x8427cc7b, "_raw_spin_lock_irq" },
	{ 0x4b750f53, "_raw_spin_unlock_irq" },
	{ 0x4829a47e, "memcpy" },
	{ 0x8631c9ba, "alt_cb_patch_nops" },
	{ 0x4c954b9f, "usb_submit_urb" },
	{ 0x290795f9, "_dev_err" },
	{ 0x87b15245, "usb_autopm_put_interface_async" },
	{ 0xa6e28ee5, "tty_port_tty_hangup" },
	{ 0xe03a66c0, "usb_kill_urb" },
	{ 0x3c12dfe, "cancel_work_sync" },
	{ 0xba8fbd64, "_raw_spin_lock" },
	{ 0xb5b54b34, "_raw_spin_unlock" },
	{ 0xde0cd55b, "tty_port_put" },
	{ 0x3c3ff9fd, "sprintf" },
	{ 0x6ebe366f, "ktime_get_mono_fast_ns" },
	{ 0xfbfd1ba8, "tty_insert_flip_string_fixed_flag" },
	{ 0xd81bfb7a, "tty_flip_buffer_push" },
	{ 0xba287df7, "tty_port_tty_wakeup" },
	{ 0xaeab8a57, "__tty_alloc_driver" },
	{ 0x67b27ec1, "tty_std_termios" },
	{ 0x5ffa6907, "tty_register_driver" },
	{ 0x6f268802, "usb_register_driver" },
	{ 0xc63ef7e9, "tty_unregister_driver" },
	{ 0x715de97a, "tty_driver_kref_put" },
	{ 0x92997ed8, "_printk" },
	{ 0x34421169, "tty_port_hangup" },
	{ 0xb57a5c58, "usb_autopm_get_interface_async" },
	{ 0xf1210753, "tty_port_close" },
	{ 0x1b811b1f, "tty_port_open" },
	{ 0xceb3e64, "usb_deregister" },
	{ 0x4dfa8d4b, "mutex_lock" },
	{ 0x3213f038, "mutex_unlock" },
	{ 0x91887293, "tty_standard_install" },
	{ 0x296695f, "refcount_warn_saturate" },
	{ 0x2d3385d3, "system_wq" },
	{ 0xc5b6f236, "queue_work_on" },
	{ 0xa78df0a4, "usb_put_intf" },
	{ 0x37a0cba, "kfree" },
	{ 0xaebf832b, "device_remove_file" },
	{ 0x96839734, "tty_port_tty_get" },
	{ 0xc32876ca, "tty_vhangup" },
	{ 0x80ff1c3c, "tty_kref_put" },
	{ 0xa4d13199, "tty_unregister_device" },
	{ 0xd43c03a6, "usb_free_urb" },
	{ 0xbd6b09c, "usb_free_coherent" },
	{ 0xc8aeb2fd, "usb_driver_release_interface" },
	{ 0x76ea281a, "usb_control_msg" },
	{ 0x8da6585d, "__stack_chk_fail" },
	{ 0x667a6819, "usb_autopm_get_interface" },
	{ 0xed1cd21d, "usb_autopm_put_interface" },
	{ 0xbd394d8, "tty_termios_baud_rate" },
	{ 0xdcb764ad, "memset" },
	{ 0x12a4e128, "__arch_copy_from_user" },
	{ 0xc6cbbc89, "capable" },
	{ 0x6cbbfc54, "__arch_copy_to_user" },
	{ 0x630ccd0d, "kmalloc_caches" },
	{ 0x9a3da3dc, "kmalloc_trace" },
	{ 0x7587bce8, "usb_ifnum_to_if" },
	{ 0xcefb0c9f, "__mutex_init" },
	{ 0x5d1fbcfb, "tty_port_init" },
	{ 0xa696e804, "usb_alloc_coherent" },
	{ 0xaa9a8ee, "usb_alloc_urb" },
	{ 0xa352c4d3, "device_create_file" },
	{ 0xeb233a45, "__kmalloc" },
	{ 0x32d269e3, "_dev_info" },
	{ 0x53574c64, "usb_driver_claim_interface" },
	{ 0x68e579a3, "usb_get_intf" },
	{ 0x52806369, "tty_port_register_device" },
	{ 0xb7fa7f3a, "_dev_warn" },
	{ 0xc6308436, "module_layout" },
};

MODULE_INFO(depends, "");

MODULE_ALIAS("usb:v04E2p1410d*dc*dsc*dp*ic*isc*ip*in*");
MODULE_ALIAS("usb:v04E2p1411d*dc*dsc*dp*ic*isc*ip*in*");
MODULE_ALIAS("usb:v04E2p1412d*dc*dsc*dp*ic*isc*ip*in*");
MODULE_ALIAS("usb:v04E2p1414d*dc*dsc*dp*ic*isc*ip*in*");
MODULE_ALIAS("usb:v04E2p1420d*dc*dsc*dp*ic*isc*ip*in*");
MODULE_ALIAS("usb:v04E2p1421d*dc*dsc*dp*ic*isc*ip*in*");
MODULE_ALIAS("usb:v04E2p1422d*dc*dsc*dp*ic*isc*ip*in*");
MODULE_ALIAS("usb:v04E2p1424d*dc*dsc*dp*ic*isc*ip*in*");
MODULE_ALIAS("usb:v04E2p1400d*dc*dsc*dp*ic*isc*ip*in*");
MODULE_ALIAS("usb:v04E2p1401d*dc*dsc*dp*ic*isc*ip*in*");
MODULE_ALIAS("usb:v04E2p1402d*dc*dsc*dp*ic*isc*ip*in*");
MODULE_ALIAS("usb:v04E2p1403d*dc*dsc*dp*ic*isc*ip*in*");

MODULE_INFO(srcversion, "CC26107864EA0F737957BDC");
